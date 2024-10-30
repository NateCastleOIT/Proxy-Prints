import requests

def fetch_website_content(url):

    try:
        response = requests.get(url)
        response.raise_for_status() # raise an exception in case of http errors
        print("Response content:\n", response.text)

        # Write raw content to file
        write_to_file(formatted_content, "raw_content_temp.txt")
        return response.text

    except requests.exceptions.RequestException as e:
        print("Error fetching website content: ", e)
        return None

def format_response_content(response, output_file):
     # Parse HTML with BeautifulSoup
     try:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract details
        title = soup.find('title').text if soup.find('title') else "No title found"
        description = soup.find('meta', {'name': 'description'})
        description_content = description['content'] if description else "No description found"
        author = soup.find('meta', {'name': 'author'})
        author_content = author['content'] if author else "No author found"
        og_image = soup.find('meta', {'property': 'og:image'})
        og_image_url = og_image['content'] if og_image else "No image found"

        # Format content
        formatted_content = (
            f"Title: {title}\n"
            f"Author: {author_content}\n"
            f"Description: {description_content}\n"
            f"Image URL: {og_image_url}\n"
            f"URL: {url}\n"
        )

        # Write content to file
        write_to_file(formatted_content, output_file)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def write_to_file(content, output_file):
    try:
        with open(output_file, 'w') as file:
            file.write(content)
            print(f"Content written to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Test the function
url = "https://archidekt.com/decks/9166525/dsc_miracle_worker"

output_file = "formatted_content_temp.txt"

response = fetch_website_content(url)

if response:
    format_response_content(response, output_file)