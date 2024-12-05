import argparse
import requests
import os
import re
import json
from bs4 import BeautifulSoup

# PDF generation
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

ARCHIDEKT_TAG = 'script'
ARCHIDEKT_TAG_ID = '__NEXT_DATA__'
MTGGOLDFISH_TAG = 'script'
MTGGOLDFISH_TAG_ID = 'deck'

TEMP_RAW_CONTENT = "TEMP_raw_content.txt"
TEMP_FORMATTED_CONTENT = "TEMP_formatted_content.txt"
TEMP_DECKLIST_TXT = "TEMP_decklist.txt"

MTG_CARD_WIDTH_IN_POINTS= 2.46*72 # 2.46 inches, 1 inch = 72 points
MTG_CARD_HEIGHT_IN_POINTS= 3.46*72 # 3.46 inches, 1 inch = 72 points

WRITE_TEMP_FILES = True
PRINT_CARD_IMAGE_URLS = False

def fetch_website_content(url, output_file=TEMP_RAW_CONTENT):
    if output_file == "":
        print("Using TEMP_raw_content.txt...")
        output_file = TEMP_RAW_CONTENT

    try:
        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
                }

        response = requests.get(url, headers=headers)
        response.raise_for_status() # raise an exception in case of http errors
        # print("Response content:\n", response.text)

        if WRITE_TEMP_FILES:
            # Write raw response to file
            soup = BeautifulSoup(response.text, 'html.parser')
            write_to_file(soup.prettify(), "TEMP_RAW_RESPONSE.txt")
            write_to_file(soup.get_text(), "TEMP_RAW_TEXT_RESPONSE.txt")

        return response.text

    except requests.exceptions.RequestException as e:
        print("Error fetching website content: ", e)
        return None

def mtggoldfish_format_response_content(response, url="", output_file=TEMP_FORMATTED_CONTENT):
    soup = BeautifulSoup(response, 'html.parser')

    card_data = soup.find('table', class_='deck-view-deck-table')

    card_data = json.loads(card_data)

    data_pretty = json.dumps(card_data, indent=2)

    write_to_file(data_pretty, output_file)



    #script_tag = soup.find_all()

def archidekt_format_response_content(response, url="", output_file=TEMP_FORMATTED_CONTENT):
    if output_file == "":
        print("Using TEMP_formatted_content.txt...")
        output_file = TEMP_FORMATTED_CONTENT

    # Parse HTML with BeautifulSoup
    try:
        soup = BeautifulSoup(response, 'html.parser')
        
        script_tag = None
        if url.startswith("https://archidekt.com/decks/"):
            script_tag = soup.find(ARCHIDEKT_TAG, id=ARCHIDEKT_TAG_ID)
        else:
            print("Site not supported")
            return

        # Extract details
        title = soup.find('title').text if soup.find('title') else "No title found"
        description = soup.find('meta', {'name': 'description'})
        description_content = description['content'] if description else "No description found"
        author = soup.find('meta', {'name': 'author'})
        author_content = author['content'] if author else "No author found"
        og_image = soup.find('meta', {'property': 'og:image'})
        og_image_url = og_image['content'] if og_image else "No image found"

        # Default JSON data
        data_pretty = "No JSON data found"

        # Extract JSON data from script tag
        if script_tag:
            # Extract JSON content
            json_content = script_tag.string

            try:
                # Load the JSON content into a Python dictionary
                data = json.loads(json_content)

                # Pretty formatted data the dictionary
                data_pretty = json.dumps(data, indent=2)
            except json.JSONDecodeError as e:
                print(f"An error occurred decoding the JSON content: {e}")

        # Format content
        formatted_content = (
            f"Title: {title}\n"
            f"Author: {author_content}\n"
            f"Description: {description_content}\n"
            f"Image URL: {og_image_url}\n"
            f"URL: {url}\n"
            f"JSON data:\n{data_pretty}"
        )

        return formatted_content, data_pretty, sanitize_title(title.split("•")[0].strip())

    except requests.exceptions.RequestException as e:
        print(f"An error occurred formatting the response: {e}")

def generate_vanilla_decklist(card_data, output_file=TEMP_DECKLIST_TXT):
    if output_file == "":
        print("Using TEMP_decklist.txt...")
        output_file = TEMP_DECKLIST_TXT

    # Load the JSON data into a Python dictionary
    card_data = json.loads(card_data)

    # Generate a vanilla decklist from the card data
    card_map = card_data.get('props', {}).get('pageProps', {}).get('redux', {}).get('deck', {}).get('cardMap', {})

    #card_names = [card_info['name'] for card_info in card_map.values() if 'name' in card_info]
    card_list = []

    for card_info in card_map.values():
        name = card_info.get('name', '')
        quantity = card_info.get('qty', 1)

        # Append quantity to the card name if quantity is greater than 1
        card_list.append(f"{quantity} {name}")
    
    return card_list

def get_card_urls(card_data):
    """
    Extracts card names and their image URLs from the card data using the UUID (uid) field.

    Parameters:
        card_data (dict): Processed JSON data containing deck and card information.

    Returns:
        dict: A dictionary with card names as keys and their image URLs as values.
    """
    card_images = {}
    card_data = json.loads(card_data)
    card_map = card_data.get('props', {}).get('pageProps', {}).get('redux', {}).get('deck', {}).get('cardMap', {})

    for card_id, card_info in card_map.items():
        card_name = card_info.get('name', 'Unknown Card')

        card_qty = card_info.get('qty', 1)
        
        # Use 'uid' to construct the image URL if available
        uid = card_info.get('uid')
        if uid:
            image_url = f"https://cards.scryfall.io/large/front/{uid[0]}/{uid[1]}/{uid}.jpg"
            card_images[card_name] = image_url, card_qty
        else:
            card_images[card_name] = "No image available", card_qty
    
    return card_images

def create_new_deck_folder(base_folder_name, deck_directory="Decks"):
    """
    Generates a unique folder name by appending an incremented number if the folder already exists.

    Parameters:
        base_folder_name (str): The base name for the folder.

    Returns:
        str: A unique folder name.
    """
    # Sanitize the folder name
    folder_name = sanitize_title(base_folder_name)

    # Loop until we find a folder name that doesn't exist
    folder_name = increment_file_name(deck_directory + "\\", folder_name)
    deck_name = folder_name
    deck_folder_name = f'{deck_directory}\{folder_name}\deck_list'
    deck_folder_path = os.path.join(os.getcwd(), deck_folder_name)

    return deck_folder_path, deck_name

def increment_file_name(directory, file_name, extension=""):
    """
    Increments a file name by appending a number to it if the file already exists.

    Parameters:
        parent_path (str): The path to the parent directory.
        file_name (str): The base file name.
        extension (str): The file extension.

    Returns:
        str: A unique file name.
    """
    # Initialize the file name counter
    counter = 1
    new_file_name = file_name + extension

    # Loop until we find a file name that doesn't exist
    while os.path.exists(os.path.join(directory, new_file_name)):
        new_file_name = f"{file_name} ({counter}){extension}"
        counter += 1

    return new_file_name

def sanitize_title(title):
    """
    Sanitizes a title to create a safe file name by removing or replacing special characters.

    Parameters:
        title (str): The original title.

    Returns:
        str: A sanitized file name.
    """
    # Replace any characters that are not letters, numbers, spaces, or underscores
    sanitized_title = re.sub(r'[^\w\s-]', '', title)
    # Replace spaces with underscores to avoid spaces in file names
    sanitized_title = sanitized_title.replace(" ", "_")

    return sanitized_title

def download_images(card_images, deck_name="TEMP_deck"):
    """
    Downloads images from URLs and saves them in a new folder.

    Parameters:
        card_images (dict): Dictionary with card names as keys and image URLs as values.
        deck_name (str): Name for the folder where images will be saved.
    """
    # Create a unique directory for each deck
    folder_name = f"{deck_name}_images"

    # Sanitize the folder name
    folder_name, deck_name = create_new_deck_folder(folder_name)

    print(f"\nCreating folder: {folder_name}")

    # Create the directory
    os.makedirs(folder_name, exist_ok=True)

    # Download each image
    for card_name, image_url in card_images.items():
        for i in range(image_url[1]):
            if image_url[1] > 1:
                if i > 0:
                    card_name = card_name.replace(f"_{i}", f"_{i+1}")
                else:
                    card_name = f"{card_name}_{i+1}"
            if image_url == "No image available":
                print(f"No image available for {card_name}")
                continue

            try:
                response = requests.get(image_url[0], stream=True)
                response.raise_for_status()
                
                # Save the image with the card name
                image_path = os.path.join(folder_name, f"{card_name}.jpg")
                
                # Change MDFC card names to use a hyphen instead of a //
                image_path = image_path.replace('//', '--')

                with open(image_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                
                print(f"Downloaded {card_name} image.")
            
            except requests.exceptions.RequestException as e:
                print(f"Failed to download image for {card_name}: {e}")
    return folder_name

def write_to_file(content, output_file):
    if WRITE_TEMP_FILES:
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(content)
                # print(f"\nContent written to {output_file}")
        except Exception as e:
            print(f"An error occurred: {e}")

def get_cards_from_any_link(url):
    raw_response = fetch_website_content(url, )

    if "mtggoldfish" in url:
        mtggoldfish_format_response_content(raw_response, url)

    if raw_response:
        # Format the response content and extract the deck information
        formatted_deck_information, card_data, deck_title = archidekt_format_response_content(raw_response, url)

        # Generate a vanilla decklist from the card data
        decklist = generate_vanilla_decklist(card_data)

        # Print the decklist
        print("\n\nDecklist:")
        print("\n".join(decklist))

        # Get card images
        card_images = get_card_urls(card_data)
        new_deck_image_folder = download_images(card_images, deck_name=deck_title)

        # Print card image urls
        if PRINT_CARD_IMAGE_URLS:
            print("\nCard images:")
            for card_name, image_url in card_images.items():
                print(f"{card_name}: {image_url}")


        if WRITE_TEMP_FILES:
            # Write raw response to file
            write_to_file(raw_response, new_deck_image_folder.split('deck_list')[0] + f"{deck_title}_RAW_RESPONSE.txt")

            # Write formatted deck information to file\
            write_to_file(formatted_deck_information, new_deck_image_folder.split('deck_list')[0] + f"{deck_title}_FORMATTED_DECK_INFO.txt")

            # Write decklist to file
            write_to_file("\n".join(decklist), new_deck_image_folder.split('deck_list')[0] + f"{deck_title}_DECKLIST.txt")

        # Generate a PDF with the card images
        # pdf_path = f"{new_deck_image_folder.split('deck_list')[0]}PRINTABLE_9_{deck_title}.pdf"
        pdf_path2 = f"{new_deck_image_folder.split('deck_list')[0]}PRINTABLE_10_{deck_title}.pdf"

        # print(f"\nGenerating PDF...")
        # pdf_generator = PDFGenerator(pdf_path, margin=0, padding=2)
        # pdf_generator.add_images_to_pdf(new_deck_image_folder, grids=((3, 3),), positions=((0, 0),), angle=(0,), offset=((9, 9),))
        # print(f"\nPDF generated: {pdf_path}")

        # os.startfile(pdf_path)

        print(f"\nGenerating PDF...")
        pdf_generator = PDFGenerator(pdf_path2, margin=0, padding=2)
        pdf_generator.add_images_to_pdf(new_deck_image_folder,
         grids=((1, 3),(2,2),(3,1)), 
         positions=
         ((0, 0),
         (MTG_CARD_HEIGHT_IN_POINTS + 2, 0),
         (0, 3*MTG_CARD_WIDTH_IN_POINTS + 6),
         ),
         angle=(90,0,0,))
        print(f"\nPDF generated: {pdf_path2}\n\n")

        # Open the PDF file
        os.startfile(pdf_path2)

class PDFGenerator:
    def __init__(self, output_file, page_size=letter, padding=10, margin=20):
        """
        Initializes the PDF generator with specified parameters.

        Parameters:
            output_file (str): The file path for the generated PDF.
            page_size (tuple): The size of the PDF pages.
            grid_size (tuple): The number of images per row and column.
            padding (int): The space between images.
            margin (int): The margin around images.
        """
        self.output_file = output_file
        self.page_width, self.page_height = page_size
        self.padding = padding
        self.margin = margin
        self.canvas = canvas.Canvas(output_file, pagesize=page_size)
    
    def add_images_to_pdf(self, image_folder, grids=((3, 3),), positions=((0, 0),), angle=(0,), offset=(7, 8)):
            """
            Arranges images into a specified grid size and saves them in the PDF.
            """
            positions = [(position[0] + offset[0], position[1] + offset[1]) for position in positions]

            image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

            image_index = 0
            while image_index < len(image_files):
                for grid_index, grid in enumerate(grids):
                    
                    grid_columns, grid_rows = grid

                    cell_width = MTG_CARD_WIDTH_IN_POINTS
                    cell_height = MTG_CARD_HEIGHT_IN_POINTS

                    if angle[grid_index]:
                        cell_width, cell_height = cell_height, cell_width


                    x_offset = positions[grid_index][0]
                    y_offset = -positions[grid_index][1] + self.page_height - cell_height


                    for row in range(grid_rows):
                        for col in range(grid_columns):
                            if image_index >= len(image_files):
                                continue

                            image_path = os.path.join(image_folder, image_files[image_index])
                            image = self.process_image(image_path, angle[grid_index])[0]

                            x = x_offset + col * (cell_width + self.padding)
                            y = y_offset - row * (cell_height + self.padding)
                            
                            self.canvas.drawImage(image, x, y, width=cell_width, height=cell_height)

                            image_index += 1

                self.canvas.showPage()  # Start a new page after filling the grid

            self.canvas.save()

    def process_image(self, image_path, angle=0,):
        with Image.open(image_path) as img:
            if angle:
                img = img.rotate(angle, expand=True)
            img.save(image_path)  # Overwrites the image or use a temp file if needed
            return image_path, img


# TODO: Allow for other sites to be used
# TODO: Automatically detect the site and use appropriate parsing strategy.
# TODO: Use command line arguments to specify the URL and output files
# TODO: Rename functions to be more descriptive


def main(url):
    get_cards_from_any_link(url)

TEST_URL_ARCHIDEKT = "https://archidekt.com/decks/9929643/bing_bong"

TEST_URL_MTGGOLDFISH = "https://www.mtggoldfish.com/archetype/standard-golgari-midrange-dmu#paper"


if __name__ == "__main__":
    while True:
        # Prompt for URL input
        URL = TEST_URL_ARCHIDEKT
        URL  = input("Enter the Archidekt deck URL (or press Enter to quit): ").strip()
        print("\n")
        
        # If the input is empty, break out of the loop
        if not URL:
            print("No URL provided. Exiting.")
            break

        main(URL)