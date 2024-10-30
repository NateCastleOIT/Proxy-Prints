import requests
import json
from bs4 import BeautifulSoup

ARCHIDEKT_TAG = 'script'
ARCHIDEKT_TAG_ID = '__NEXT_DATA__'

def fetch_website_content(url):

    try:
        response = requests.get(url)
        response.raise_for_status() # raise an exception in case of http errors
        # print("Response content:\n", response.text)

        # Write raw content to file
        write_to_file(response.text, "raw_content_temp.txt")
        return response.text

    except requests.exceptions.RequestException as e:
        print("Error fetching website content: ", e)
        return None

def format_response_content(response, output_file):
     # Parse HTML with BeautifulSoup
    try:
        soup = BeautifulSoup(response, 'html.parser')
        
        # Extract details
        title = soup.find('title').text if soup.find('title') else "No title found"
        description = soup.find('meta', {'name': 'description'})
        description_content = description['content'] if description else "No description found"
        author = soup.find('meta', {'name': 'author'})
        author_content = author['content'] if author else "No author found"
        og_image = soup.find('meta', {'property': 'og:image'})
        og_image_url = og_image['content'] if og_image else "No image found"

        script_tag = soup.find(ARCHIDEKT_TAG, id=ARCHIDEKT_TAG_ID)

        # Extract JSON data from script tag
        if script_tag:
            # Extract JSON content
            json_content = script_tag.string

            # Load the JSON content into a Python dictionary
            data = json.loads(json_content)

            # Pretty formatted data the dictionary
            data_pretty = json.dumps(data, indent=2)

            # Now 'data' is a dictionary containing the JSON data
            #print(data_pretty) # pretty print the dictionary

        # Format content
        formatted_content = (
            f"Title: {title}\n"
            f"Author: {author_content}\n"
            f"Description: {description_content}\n"
            f"Image URL: {og_image_url}\n"
            f"URL: {url}\n"
            f"JSON data:\n{data_pretty}"
        )

        # Write content to file
        write_to_file(formatted_content, output_file)

        return formatted_content, data_pretty

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def write_to_file(content, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(content)
            print(f"Content written to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Test the function
url = "https://archidekt.com/decks/9166525/dsc_miracle_worker"

output_file = "formatted_content_temp.txt"

response = fetch_website_content(url)

formatted_response, card_data = "", ""

if response:
    formatted_response, card_data = format_response_content(response, output_file)