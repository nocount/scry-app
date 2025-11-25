# Scry App 🔮

A desktop application for searching Magic: The Gathering cards using the [Scryfall API](https://scryfall.com/docs/api).

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

## Features

- 🔍 **Fuzzy Search** - Search for cards by name with flexible matching
- 🖼️ **Card Images** - View high-quality card artwork
- 📋 **Detailed Info** - See oracle text, mana cost, type, power/toughness, and more
- 💰 **Pricing** - View current market prices (USD)
- ⚖️ **Legality** - Check format legality across Standard, Pioneer, Modern, Legacy, Vintage, and Commander
- 🎨 **Modern Dark UI** - Clean, easy-to-use interface

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone or download this repository:
   ```bash
   git clone https://github.com/yourusername/scry-app.git
   cd scry-app
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Activate your virtual environment (if using one):
   ```bash
   venv\Scripts\activate
   ```

2. Run the application:
   ```bash
   python scry_app.py
   ```

3. Enter a card name in the search box and press Enter or click "Search"

### Example Searches

- `Lightning Bolt` - Classic red instant
- `Black Lotus` - The legendary Power Nine card
- `Jace, the Mind Sculptor` - Iconic planeswalker
- `Sol Ring` - Commander staple

## Dependencies

- **customtkinter** - Modern UI framework for Python
- **requests** - HTTP library for API calls
- **Pillow** - Image processing library

## API Information

This application uses the [Scryfall API](https://scryfall.com/docs/api) to fetch card data. Scryfall provides free access to Magic: The Gathering card data and images.

### Rate Limiting

The app respects Scryfall's rate limiting guidelines. For heavy usage, consider caching results locally.

## License

This project is for personal/educational use. Card data and images are provided by Scryfall under the Wizards of the Coast Fan Content Policy.

## Acknowledgments

- [Scryfall](https://scryfall.com) for their excellent API and card database
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern UI framework
