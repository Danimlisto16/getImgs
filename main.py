import pandas as pd
import requests
from bs4 import BeautifulSoup
from os.path  import basename

def loadProductsfromFile(productsPath): #DONE
  df = pd.read_excel(productsPath)
   # Filter rows where 'IMAGEEXIST' column is not equal to 0
  filtered_df = df[df['imageExist'] == 0]
  return filtered_df
  
def checkIfproductHasImage(row): #DONE
  product = row["imageExists"]
  if product == 1:
    return True
  return False


def searchImageOnWebsite(website, product, notFoundMessages):
  listPropertiesofProduct = [str(product["Name"]), str(product["Product Code"])]
  for propertie in listPropertiesofProduct:
    webProduct  = website.replace("keyword", propertie)
    # Send a GET request to the modified URL
    response = requests.get(webProduct)
      # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Implement image search logic here by finding image elements on the page
        # For example, if images are wrapped in <img> tags, you can find them using:
        #FIRST SEARCH FOR NOT FOUND MESSAGES, to continue or not with the search
        if not checkNotFound(notFoundMessages, soup):  #IMPROVE THIS CODE TOO
            
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

def loadNotFoundMessages(notFoundFile_path): #DONE
  messages = []
  try:
      with open(notFoundFile_path, 'r', encoding='utf-8') as f:
          for line in f:
              messages.append(line.strip())
  except Exception as e:
      print(f"Error occurred while loading not found messages from {notFoundFile_path}: {e}")
  return messages


def checkNotFound(notFoundMsgList, soup):
    # Find if the notFoundMsg exists in the webpage
    for msg in notFoundMsgList:
      if soup.find(string=msg):
        return True
    return False


def getAndSaveImage(images,imgName,imgSavePath):  #IMPROVE THIS LOGIC
  for link in images:
    if "http" in link.get('src'):
        lnk = link.get('src')
        with open(basename(lnk), "wb") as f:
            f.write(requests.get(lnk).content)
    
    
def getWebsites(websitesPath): #DONE
  websites = []
  with open(websitesPath) as f:
    for line in f:
      websites.append(line.strip())
  return websites

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


#This function will create a new file from the old file, 
# with CLOVER ID, NAME, PRODUCT CODE and a new column IMAGE EXIST


columns_to_read = ["Clover ID", "Name", "Product Code"]
sourceFile = "./Items/Kalinka.xlsx" #replace with the path to your file
destinationFile = "./Items/New_Kalinka.xlsx" #replace with the path to your new file


# --------- ONLY RUN THIS FUNCTION ONCE TO CREATE THE NEW FILE ----------
#createNewFileFromOldFile(sourceFile, destinationFile, columns_to_read)

websitesPath = "./websites/websites.txt"
websites = getWebsites(websitesPath)
notFoundmessages = loadNotFoundMessages("./notFoundMessages/notFoundMessages.txt")
productsList = loadProductsfromFile("./Items/New_Kalinka.xlsx")

for index, product in productsList.iterrows(): #search for image on websites
  for website in websites:
    searchImageOnWebsite(website, product,notFoundmessages)