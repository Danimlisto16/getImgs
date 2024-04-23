import pandas as pd
import requests
from bs4 import BeautifulSoup
from os.path  import basename

from Classes.Product import Product
from Classes.Website import Website


def loadProductsfromFile(productsPath): #DONE
  product_list = []
  df = pd.read_excel(productsPath)
   # Filter rows where 'IMAGEEXIST' column is not equal to 0
  filtered_df = df[df['imageExist'] == 0]
  for index, row in filtered_df.iterrows():
    product = Product(row["Clover ID"], row["Name"], row["Product Code"], row["imageExist"])
    product_list.append(product)
  return product_list

def loadWebsitesfromFile(websitesPath): #DONE
  websites_list = []
  df = pd.read_excel(websitesPath)
  for index, row in df.iterrows():
    website = Website(row["URL"], row["NotFoundMsg"], row["CLASS"])
    websites_list.append(website)
  return websites_list
  
  
def searchProductOnWebsite(website = Website, product = Product):
  listPropertiesofProduct = [product.barcode, product.name]
  for propertie in listPropertiesofProduct:
    webProduct  = website.url.replace("keyword", propertie)
    # Send a GET request to the modified URL
    response = requests.get(webProduct)
      # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Implement image search logic here by finding image elements on the page
        if not checkNotFound(website, soup):  #IMPROVE THIS CODE TOO
            #find all images in the page
            images = soup.find_all('img')
            
            #get img links
            
            #save 3 images with the barcode name in the Images folder
            
            #convert image to webp format
            
            #update row in the new_restaurants.xlsx file to imageExists = 1
            product["imageExists"] = 1
            
            #save in the new file
            
            
            # Check if any images were found
    else:
      # If the request was not successful, print an error message and return False
      print("Error: Unable to retrieve data from the website.")
      return False

def checkNotFound(notFoundMsgList, soup):
    for message in notFoundMsgList:    
      try:
          # Find all occurrences of the specified text
          occurrences = soup.find_all(string=lambda t: message in str(t))    
          # Print the found occurrences
          if len(occurrences) == 0:
              return False
          else:
              return True
      except Exception as e:
          print(f"Error occurred while accessing {url}: {e}")


def getAndSaveImage(images,imgName,imgSavePath):  #IMPROVE THIS LOGIC
  for link in images:
    if "http" in link.get('src'):
        lnk = link.get('src')
        with open(basename(lnk), "wb") as f:
            f.write(requests.get(lnk).content)

def createNewFileFromOldFile(sourceFile, destinationFile, columns_to_read): #DONE
  # Replace 'file_path.xls' with the path to your Excel file
  file_path = sourceFile
  df = pd.read_excel(file_path, usecols = columns_to_read)
  # Add a new column with a scalar value
  df['imageExist'] = 0  # Replace scalar_value with your desired value
  #save as new file
  df.to_excel(destinationFile, index = False)
  
  
  
#-----------------PSEUDO CODE--------------------------------
#load products from file in pandas rows
#get identifier, name, barcode, image fields
#rename image to imageExists
#clear all the imageExists fields
#then get the websites and search for name or barcode,
#if found, save the image in the Images folder and update the imageExists field to True
#do this until image is found or all websites are searched
#if image is not found, save the name and barcode in a notFound.csv file








""" --------- ONLY RUN THIS FUNCTION ONCE TO CREATE THE NEW FILE ----------

sourceFile = "./Items/Kalinka.xlsx" #replace with the path to your file
destinationFile = "./Items/New_Kalinka.xlsx" #replace with the path to your new file
columns_to_read = ["Clover ID", "Name", "Product Code"]
createNewFileFromOldFile(sourceFile, destinationFile, columns_to_read)

"""


websitesPath = "./websites/websites.xls"
websites = loadWebsitesfromFile(websitesPath) #refactor to parse to objects products

productsList = loadProductsfromFile("./Items/New_Kalinka.xlsx")

for product in productsList: #search for image on websites
  for website in websites:
    searchProductOnWebsite(website, product)