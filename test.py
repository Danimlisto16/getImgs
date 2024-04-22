import requests
from bs4 import BeautifulSoup

def search_text_in_page(url, text):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        html_content = response.text
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all occurrences of the specified text
        occurrences = soup.find_all(string=lambda t: text in str(t))
        
        # Print the found occurrences
        if len(occurrences) == 0:
            return False
        else:
            return True
    except Exception as e:
        print(f"Error occurred while accessing {url}: {e}")

# Example usage:
url = 'https://www.onlinetrade.ru/sitesearch.html?query=asdsads'
text_to_search = "Найденные товары по запросу"
print(search_text_in_page(url, text_to_search))  # Output: True