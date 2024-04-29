import requests
from bs4 import BeautifulSoup

def search_text_in_page(url, text):
    #agent to avoid 403 error
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        # Fetch the webpage content
        response = requests.get(url,headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        html_content = response.text
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all occurrences of the specified text not found
        occurrences = soup.find_all(string=lambda t: text in str(t))
        
        # Print the found occurrences
        if len(occurrences) == 0:
            return False
        else:
            return True
    except Exception as e:
        print(f"Error occurred while accessing {url}: {e}")

# Example usage:
url = 'https://world.openfoodfacts.org/cgi/search.pl?search_terms=banasdsadasdasdsad&search_simple=1&action=process'
text_to_search = "No products."
print(search_text_in_page(url, text_to_search))  # Output: True