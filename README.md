```markdown
# Archidekt Deck Image Downloader and PDF Generator

This program fetches deck information from Archidekt, a popular deck-building website for Magic: The Gathering. It retrieves card information and images from a specified Archidekt deck URL, organizes the images in grids, and generates a printable PDF for easy card viewing or proxy printing. The program supports creating multiple grid configurations and customizes image placement and rotation in the generated PDF.

## Features
- Fetches deck data from Archidekt and processes it.
- Downloads card images and organizes them into a unique folder.
- Generates a PDF containing card images arranged in customizable grids.
- Supports different grid configurations, padding, and rotation options.
- Automatically opens the generated PDF upon completion.

## Requirements
- **Python 3.6+**
- **Libraries**:
  - `argparse`: For command-line argument parsing.
  - `requests`: For sending HTTP requests.
  - `os`: For directory and file management.
  - `re`: For handling regex operations.
  - `json`: For processing JSON data.
  - `BeautifulSoup` from `bs4`: For parsing HTML.
  - `Pillow`: For handling image operations.
  - `reportlab`: For generating PDF files.

You can install all required libraries using:
```bash
pip install requests beautifulsoup4 pillow reportlab
```

## Usage
1. **Running the Program**: Run the script with Python. The program will prompt you to enter an Archidekt deck URL. After processing the URL, it will fetch the deck data, download the images, and generate a PDF.

```bash
python your_script.py
```

2. **Interactive Mode**: You can input multiple URLs in sequence. To exit, simply press Enter without typing a URL.

### Command-line Arguments
This script also supports using a URL as a command-line argument.

```bash
python your_script.py "https://archidekt.com/decks/your_deck_url"
```

## Example Output
Upon entering a URL, the program will:
1. Retrieve and process the deck's card data.
2. Download card images and save them in a unique folder.
3. Generate two PDFs:
   - One with a 3x3 grid layout.
   - Another with a custom layout based on 1x3, 2x2, and 3x1 grids.
4. Automatically open both PDFs for preview.

## PDF Customization
The PDF layout and image grid configurations are customizable:
- **Grids**: Specify the number of rows and columns (e.g., `grids=((3, 3),)` for a 3x3 grid).
- **Positions**: Set custom positions for each grid.
- **Rotation**: Define rotation angles for each grid layout.

## Program Structure
- **fetch_website_content**: Fetches HTML content from the provided URL.
- **format_response_content**: Parses HTML and extracts JSON data.
- **generate_vanilla_decklist**: Produces a plain-text decklist from the card data.
- **get_card_urls**: Extracts card names and image URLs.
- **create_new_deck_folder**: Generates a unique folder for each deck's images.
- **download_images**: Downloads and saves card images to the specified folder.
- **PDFGenerator**: A class for creating and customizing PDF layouts of card images.

## Temporary Files
Temporary files are created if `WRITE_TEMP_FILES` is set to `True`, storing raw and formatted deck information for debugging purposes. Files include:
- `TEMP_raw_content.txt`: Raw HTML response.
- `TEMP_formatted_content.txt`: Extracted and formatted content.
- `TEMP_decklist.txt`: Generated deck list.

## Future Enhancements
- Support for multiple deck-building websites.
- Automatic detection of site structure and data extraction methods.
- Enhanced CLI arguments for specifying grid layouts, image rotation, and other options.

## License
This project is licensed under the Apache 2.0 License.
```
