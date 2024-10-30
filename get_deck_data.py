import requests

def fetch_website_content(url):

    try:
        response = requests.get(url)
        response.raise_for_status() # raise an exception in case of http errors
        print("Response content:\n", response.text)
        return response.text

    except requests.exceptions.RequestException as e:
        print("Error fetching website content: ", e)
        return None

# Test the function
url = "https://archidekt.com/decks/9823611/but_why_is_he_here_new"
fetch_website_content(url)