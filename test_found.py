import os
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
            img_tags = soup.find_all('img')
            # Create download folder if it doesn't exist
            
            if not os.path.exists("./"):
                os.makedirs("./")
            # Download each image
            for img_tag in img_tags:
                # Get the image URL from the src attribute
                img_url = "https:"+img_tag['src']
                if img_url:
                  try:
                      # Download the image
                      img_response = requests.get(img_url)
                      img_response.raise_for_status()  # Raise an exception for bad status codes
                      
                      img_filename = os.path.join("./Images/", os.path.basename(img_url).replace('?', '_'))
                      
                      # Save the image to the output folder
                      with open(img_filename, 'wb') as img_file:
                          img_file.write(img_response.content)
                          print(f"Image saved: {img_filename}")
                  except Exception as e:
                      print(f"Error occurred while downloading image from {img_url}: {e}")
                else:
                  print("Image URL not found.")
            return False
        else:
            return True
    except Exception as e:
        print(f"Error occurred while accessing {url}: {e}")


# Example usage:
url = 'https://elonamarket.com/search?q=apple'
text_to_search = "Search: 0 results found for"
print(search_text_in_page(url, text_to_search))  # Output: True