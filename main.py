import pandas as pd
import requests
from bs4 import BeautifulSoup
from os.path  import basename

def loadProductsfromFile():
  products = []
  with open("products.txt") as f:
    for line in f:
      products.append(line.strip())
  return products

def checkIfproductHasImage(row):
  product = row["imageExists"]
  if product == 1:
    return True
  return False

def searchImageOnWebsite(webiste, productName, productBarcode):
  webProduct  = webiste.replace("keyword", productName)
  # Send a GET request to the modified URL
  response = requests.get(webProduct)

    # Check if the request was successful
  if response.status_code == 200:
      # Parse the HTML content of the page using BeautifulSoup
      soup = BeautifulSoup(response.content, 'html.parser')
        
      # Implement image search logic here by finding image elements on the page
      # For example, if images are wrapped in <img> tags, you can find them using:
      images = soup.find_all('img')
        
        # Check if any images were found
      if images:
          # You can further process the images, extract their URLs, or perform any other necessary action
          # For now, just return True to indicate that images were found
          return True
      else:
          # If no images were found, return False
          return False
  else:
    # If the request was not successful, print an error message and return False
    print("Error: Unable to retrieve data from the website.")
    return False
  return True

def checkNotFoundItemsOnWebsite(notFoundAnswersFile_path, websites):
  
  return True

def getAndSaveImage(links):
  for link in links:
    if "http" in link.get('src'):
        lnk = link.get('src')
        with open(basename(lnk), "wb") as f:
            f.write(requests.get(lnk).content)
    
def getWebsites(websitesPath):
  websites = []
  with open(websitesPath) as f:
    for line in f:
      websites.append(line.strip())
  return websites


def createNewFileFromOldFile(sourceFile, destinationFile, columns_to_read):
  # Replace 'file_path.xls' with the path to your Excel file
  file_path = sourceFile
  df = pd.read_excel(file_path, usecols = columns_to_read)
  # Add a new column with a scalar value
  df['imageExist'] = 0  # Replace scalar_value with your desired value
  #save as new file
  df.to_excel(destinationFile, index = False) 
  

#load products from file in pandas rows
#get identifier, name, barcode, image fields
#rename image to imageExists
#clear all the imageExists fields
#then get the websites and search for name or barcode,
#if found, save the image in the Images folder and update the imageExists field to True
#do this until image is found or all websites are searched
#if image is not found, save the name and barcode in a notFound.csv file


#This function will create a new file from the old file, 
# with CLOVER ID, NAME, PRODUCT CODE and a new column IMAGE EXIST

columns_to_read = ["Clover ID", "Name", "Product Code"]
sourceFile = "./Items/Kalinka.xlsx"
destinationFile = "./Items/New_Kalinka.xlsx"

#createNewFileFromOldFile(sourceFile, destinationFile, columns_to_read)

websitesPath = "./websites/websites.txt"
websites = getWebsites(websitesPath)

