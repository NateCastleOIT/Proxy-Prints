```markdown
# Archidekt Decklist Fetcher

This Python program fetches a Magic: The Gathering decklist from the Archidekt website, formats the response, and generates a vanilla decklist. It uses the `requests` library to handle HTTP requests and `BeautifulSoup` for parsing the HTML content.

## Features

- Fetches deck information from Archidekt.
- Extracts metadata such as title, author, and description.
- Parses and pretty-prints JSON data embedded in the webpage.
- Generates a formatted decklist with card names and quantities.
- Writes output to text files for easy access.

## Requirements

To run this program, you need to have Python 3.x installed along with the following libraries:

- `requests`
- `beautifulsoup4`

You can install the required libraries using the following command:

```bash
pip install requests beautifulsoup4
```

## Usage

1. Clone this repository or download the source code.
2. Navigate to the project directory.
3. Open the script in a Python environment.
4. Modify the `url` variable to the Archidekt deck URL you want to fetch.
5. Run the script. The output files will be generated in the project directory.

```python
# Example URL to test
url = "https://archidekt.com/decks/9189676/dsc_death_toll"
```

### Output Files

The program generates the following output files:

- `TEMP_raw_content.txt`: Contains the raw HTML content fetched from the URL.
- `TEMP_formatted_content.txt`: Contains the formatted content including metadata and pretty-printed JSON data.
- `TEMP_decklist.txt`: Contains the generated decklist with card names and quantities.

## Example Output

```
Decklist:
1 Brainstone
4 Plains
3 Swamp
1 Mesa Enchantress
1 Aminatou, Veil Piercer
```

## To-Do List

- Implement support for fetching decklists from other websites.
- Improve error handling for network issues and JSON parsing.
- Allow command line arguments for specifying the URL and output files.
- Refactor function names for better clarity.
- Generate the decklist file based on deck name, author, and date.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Archidekt](https://archidekt.com/) for providing the decklist data.
- [Requests](https://docs.python-requests.org/en/latest/) for easy HTTP requests.
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) for HTML parsing.
```
