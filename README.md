# Proxy Prints

Proxy Prints is a Python-based tool for Magic: The Gathering (MTG) players who want to create physical proxies of their decks. By providing a URL to an MTG deck list from [Archidekt](https://archidekt.com/), Proxy Prints retrieves card information and generates a printable PDF file containing images of all the cards. This makes it easy to print out proxies with minimal setup.

## Features

- **Deck List Parsing**: Automatically fetches and parses card data from an Archidekt deck URL.
- **Image Retrieval**: Downloads high-quality images of each card in the deck from Scryfall.
- **PDF Generation**: Compiles card images into a 3x3 grid format for easy cutting and printing.
- **Custom Grids**: Generates additional grid layouts to fit custom needs, such as single columns or multi-page formats.
- **Executable Ready**: Simply run the included `proxy_prints.exe` file—no Python setup required.

## Getting Started

1. **Download the Project**: Clone or download this repository.
2. **Run the Executable**:
   - Navigate to `dist/` and run `proxy_prints.exe`.
3. **Input Deck URL**: Enter the URL of the Archidekt deck you wish to print proxies for. Example URL: `https://archidekt.com/decks/12345678/my_deck`.
4. **Output**:
   - The program creates a printable PDF containing images of all the cards in the deck. Each PDF page has a grid of card images, sized for easy cutting and sleeving.

## Requirements

This project requires no additional setup if you’re using the provided executable (`proxy_prints.exe`). If you wish to run the Python code directly, you’ll need:

### Python and Libraries

- **Python 3.x**
- **Required Libraries**:
  ```bash
  pip install argparse requests beautifulsoup4 pillow reportlab
  ```

## File Structure

- **proxy_prints.exe** - Standalone executable to run the tool.
- **TEMP Files** - Temporary files for intermediate data storage (e.g., raw content, formatted data).
- **Decks Folder** - Stores the generated card images and PDFs for each deck.

## Example Usage

Run the executable and input the Archidekt deck URL when prompted:

```shell
Enter the Archidekt deck URL: https://archidekt.com/decks/12345678/my_deck
```

The program downloads the card images, generates the printable PDF, and opens it automatically once completed.

## Roadmap

- Add support for additional deck list websites.
- Improve PDF customization options.
- Add options for specific print formats, like single-page layouts for entire decks.