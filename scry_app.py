"""
Scry App - A Magic: The Gathering Card Search Application
Uses the Scryfall API to search and display card information.
"""

import customtkinter as ctk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading
from typing import Optional, Dict, Any

# Configure CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Scryfall API configuration
SCRYFALL_API_BASE = "https://api.scryfall.com"
HEADERS = {
    "User-Agent": "ScryApp/1.0",
    "Accept": "application/json"
}


class ScryApp(ctk.CTk):
    """Main application window for the Scryfall card search app."""

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Scry App - MTG Card Search")
        self.geometry("900x700")
        self.minsize(800, 600)

        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Store current card image reference
        self.current_image: Optional[ImageTk.PhotoImage] = None
        self.current_card_data: Optional[Dict[str, Any]] = None

        # Create UI components
        self._create_header()
        self._create_main_content()
        self._create_status_bar()

        # Bind Enter key to search
        self.bind("<Return>", lambda e: self._perform_search())

    def _create_header(self):
        """Create the header section with search controls."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(1, weight=1)

        # App title
        title_label = ctk.CTkLabel(
            header_frame,
            text="🔮 Scry App",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))

        # Search label
        search_label = ctk.CTkLabel(
            header_frame,
            text="Card Name:",
            font=ctk.CTkFont(size=14)
        )
        search_label.grid(row=1, column=0, padx=(0, 10))

        # Search entry
        self.search_entry = ctk.CTkEntry(
            header_frame,
            placeholder_text="Enter a Magic card name (e.g., 'Lightning Bolt')",
            font=ctk.CTkFont(size=14),
            height=40
        )
        self.search_entry.grid(row=1, column=1, padx=(0, 10), sticky="ew")

        # Search button
        self.search_button = ctk.CTkButton(
            header_frame,
            text="Search",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=100,
            command=self._perform_search
        )
        self.search_button.grid(row=1, column=2)

    def _create_main_content(self):
        """Create the main content area with card display."""
        content_frame = ctk.CTkFrame(self)
        content_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)

        # Left side - Card image
        image_frame = ctk.CTkFrame(content_frame, fg_color="#1a1a2e")
        image_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")
        image_frame.grid_rowconfigure(0, weight=1)
        image_frame.grid_columnconfigure(0, weight=1)

        self.card_image_label = ctk.CTkLabel(
            image_frame,
            text="Search for a card\nto display its image",
            font=ctk.CTkFont(size=14),
            text_color="#666666"
        )
        self.card_image_label.grid(row=0, column=0, padx=20, pady=20)

        # Right side - Card details
        details_frame = ctk.CTkFrame(content_frame, fg_color="#1a1a2e")
        details_frame.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="nsew")
        details_frame.grid_columnconfigure(0, weight=1)
        details_frame.grid_rowconfigure(0, weight=1)

        # Scrollable text box for card details
        self.details_textbox = ctk.CTkTextbox(
            details_frame,
            font=ctk.CTkFont(family="Consolas", size=13),
            wrap="word",
            fg_color="#0f0f1a",
            text_color="#e0e0e0"
        )
        self.details_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.details_textbox.insert("1.0", "Enter a card name and click Search to see card details.")
        self.details_textbox.configure(state="disabled")

    def _create_status_bar(self):
        """Create the status bar at the bottom."""
        self.status_label = ctk.CTkLabel(
            self,
            text="Ready - Enter a card name to search",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        self.status_label.grid(row=2, column=0, padx=20, pady=(5, 10), sticky="w")

    def _set_status(self, message: str, is_error: bool = False):
        """Update the status bar message."""
        color = "#ff6b6b" if is_error else "#888888"
        self.status_label.configure(text=message, text_color=color)

    def _perform_search(self):
        """Initiate the card search in a background thread."""
        card_name = self.search_entry.get().strip()
        if not card_name:
            self._set_status("Please enter a card name", is_error=True)
            return

        # Disable search button and update status
        self.search_button.configure(state="disabled")
        self._set_status(f"Searching for '{card_name}'...")

        # Run search in background thread
        thread = threading.Thread(target=self._search_card, args=(card_name,))
        thread.daemon = True
        thread.start()

    def _search_card(self, card_name: str):
        """Search for a card using the Scryfall API."""
        try:
            # Use fuzzy search for flexible matching
            url = f"{SCRYFALL_API_BASE}/cards/named"
            params = {"fuzzy": card_name}

            response = requests.get(url, params=params, headers=HEADERS, timeout=10)

            if response.status_code == 200:
                card_data = response.json()
                self.current_card_data = card_data
                self.after(0, lambda: self._display_card(card_data))
            elif response.status_code == 404:
                error_data = response.json()
                error_msg = error_data.get("details", "Card not found")
                self.after(0, lambda: self._show_error(error_msg))
            else:
                self.after(0, lambda: self._show_error(f"API error: {response.status_code}"))

        except requests.exceptions.Timeout:
            self.after(0, lambda: self._show_error("Request timed out. Please try again."))
        except requests.exceptions.ConnectionError:
            self.after(0, lambda: self._show_error("Connection error. Check your internet connection."))
        except Exception as e:
            self.after(0, lambda: self._show_error(f"Error: {str(e)}"))

    def _display_card(self, card_data: Dict[str, Any]):
        """Display the card information and image."""
        # Re-enable search button
        self.search_button.configure(state="normal")

        # Update status
        self._set_status(f"Found: {card_data.get('name', 'Unknown')}")

        # Display card details
        self._display_card_details(card_data)

        # Load and display card image
        self._load_card_image(card_data)

    def _display_card_details(self, card_data: Dict[str, Any]):
        """Format and display card details in the text box."""
        details = []

        # Card name and mana cost
        name = card_data.get("name", "Unknown")
        mana_cost = card_data.get("mana_cost", "")
        details.append(f"{'═' * 50}")
        details.append(f"  {name}  {mana_cost}")
        details.append(f"{'═' * 50}\n")

        # Type line
        type_line = card_data.get("type_line", "")
        if type_line:
            details.append(f"Type: {type_line}\n")

        # Mana value (CMC)
        cmc = card_data.get("cmc", 0)
        details.append(f"Mana Value: {int(cmc)}\n")

        # Colors
        colors = card_data.get("colors", [])
        color_map = {"W": "White", "U": "Blue", "B": "Black", "R": "Red", "G": "Green"}
        if colors:
            color_names = [color_map.get(c, c) for c in colors]
            details.append(f"Colors: {', '.join(color_names)}\n")
        else:
            details.append("Colors: Colorless\n")

        # Oracle text
        oracle_text = card_data.get("oracle_text", "")
        if oracle_text:
            details.append(f"{'─' * 50}")
            details.append(f"\nOracle Text:\n{oracle_text}\n")

        # Flavor text
        flavor_text = card_data.get("flavor_text", "")
        if flavor_text:
            details.append(f"\n{'─' * 50}")
            details.append(f"\nFlavor Text:\n\"{flavor_text}\"\n")

        # Power/Toughness for creatures
        power = card_data.get("power")
        toughness = card_data.get("toughness")
        if power and toughness:
            details.append(f"\nPower/Toughness: {power}/{toughness}")

        # Loyalty for planeswalkers
        loyalty = card_data.get("loyalty")
        if loyalty:
            details.append(f"\nStarting Loyalty: {loyalty}")

        # Rarity and set
        details.append(f"\n{'─' * 50}\n")
        rarity = card_data.get("rarity", "").capitalize()
        set_name = card_data.get("set_name", "Unknown Set")
        details.append(f"Rarity: {rarity}")
        details.append(f"Set: {set_name}")

        # Prices
        prices = card_data.get("prices", {})
        usd_price = prices.get("usd")
        usd_foil = prices.get("usd_foil")
        if usd_price or usd_foil:
            details.append(f"\n{'─' * 50}")
            details.append("\nPrices:")
            if usd_price:
                details.append(f"  Regular: ${usd_price}")
            if usd_foil:
                details.append(f"  Foil: ${usd_foil}")

        # Legalities
        legalities = card_data.get("legalities", {})
        if legalities:
            details.append(f"\n{'─' * 50}")
            details.append("\nFormat Legality:")
            for format_name in ["standard", "pioneer", "modern", "legacy", "vintage", "commander"]:
                status = legalities.get(format_name, "unknown")
                status_symbol = "✓" if status == "legal" else "✗" if status == "not_legal" else "○"
                details.append(f"  {status_symbol} {format_name.capitalize()}: {status.replace('_', ' ').title()}")

        # Artist
        artist = card_data.get("artist", "")
        if artist:
            details.append(f"\n{'─' * 50}")
            details.append(f"\nArtist: {artist}")

        # Scryfall URI
        scryfall_uri = card_data.get("scryfall_uri", "")
        if scryfall_uri:
            details.append(f"\nScryfall: {scryfall_uri}")

        # Update textbox
        self.details_textbox.configure(state="normal")
        self.details_textbox.delete("1.0", "end")
        self.details_textbox.insert("1.0", "\n".join(details))
        self.details_textbox.configure(state="disabled")

    def _load_card_image(self, card_data: Dict[str, Any]):
        """Load and display the card image."""
        # Get image URL - handle different card layouts
        image_uris = card_data.get("image_uris")

        # For double-faced cards, get the front face
        if not image_uris and "card_faces" in card_data:
            faces = card_data["card_faces"]
            if faces and "image_uris" in faces[0]:
                image_uris = faces[0]["image_uris"]

        if not image_uris:
            self.card_image_label.configure(image=None, text="No image available")
            return

        # Use 'normal' size for good quality without being too large
        image_url = image_uris.get("normal") or image_uris.get("large") or image_uris.get("small")

        if not image_url:
            self.card_image_label.configure(image=None, text="No image available")
            return

        # Load image in background
        thread = threading.Thread(target=self._fetch_and_display_image, args=(image_url,))
        thread.daemon = True
        thread.start()

    def _fetch_and_display_image(self, image_url: str):
        """Fetch image from URL and display it."""
        try:
            response = requests.get(image_url, headers=HEADERS, timeout=15)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                pil_image = Image.open(image_data)

                # Resize to fit the display area while maintaining aspect ratio
                max_height = 450
                max_width = 320
                pil_image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

                # Convert to CTkImage for display
                ctk_image = ctk.CTkImage(
                    light_image=pil_image,
                    dark_image=pil_image,
                    size=pil_image.size
                )

                # Update in main thread
                self.after(0, lambda: self._set_card_image(ctk_image))
        except Exception as e:
            self.after(0, lambda: self.card_image_label.configure(
                image=None,
                text=f"Failed to load image:\n{str(e)}"
            ))

    def _set_card_image(self, image: ctk.CTkImage):
        """Set the card image in the UI."""
        self.current_image = image
        self.card_image_label.configure(image=image, text="")

    def _show_error(self, message: str):
        """Display an error message."""
        self.search_button.configure(state="normal")
        self._set_status(message, is_error=True)

        # Update details textbox with error
        self.details_textbox.configure(state="normal")
        self.details_textbox.delete("1.0", "end")
        self.details_textbox.insert("1.0", f"Error: {message}\n\nPlease try another search.")
        self.details_textbox.configure(state="disabled")

        # Clear the image
        self.card_image_label.configure(image=None, text="No card to display")


def main():
    """Main entry point for the application."""
    app = ScryApp()
    app.mainloop()


if __name__ == "__main__":
    main()

