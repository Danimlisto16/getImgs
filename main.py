import os
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
    product = Product(str(row["Clover ID"]), str(row["Name"]), str(row["Product Code"]), str(row["imageExist"]))
    product_list.append(product)
  return product_list

def loadWebsitesfromFile(websitesPath): #DONE
  websites_list = []
  df = pd.read_excel(websitesPath)
  for index, row in df.iterrows():
    website = Website(row["URL"], row["NotFoundMsg"], row["CLASS"])
    websites_list.append(website)
  return websites_list
  

def get_images(class_name, soup):
    # Find all elements with the given class name
    elements = soup.find_all(class_=class_name)
    # Initialize a list to store image URLs
    img_urls = []
    # Iterate over the found elements
    for element in elements:
        # Find all image elements within the current element
        imgs = element.find_all('img')
        # Extract the 'src' attribute from each image element and add it to the list
        for img in imgs:
            img_urls.append(img['src'])
    return img_urls
  
  
def checkUrl(url):
  if "//" == url[:2]:
    return "https:"+url
  if "http" in url:
    return url
  else:
    return "https://"+url

def save_image_from_url(image_url, save_path):
    # Send a GET request to the image URL
    image_url = checkUrl(image_url)
    response =  requests.get(image_url) #WELL THE PROBLEM IS, SOMETIMES IT GETS A URL IMAGE WITH HTTPS AND OTHER TIMES WITHOU HTTP
    # Check if the request was successful
    
    if response.status_code == 200:
        # Open a file in binary write mode and write the image content to it
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Image saved successfully at {save_path}")
    else:
        print(f"Failed to save image from {image_url}. Status code: {response.status_code}")

  
def searchProductOnWebsite(website = Website, product = Product, image_num = int):
  listPropertiesofProduct = [product.barcode, product.name]
  for propertie in listPropertiesofProduct:
    webProduct  = website.url.replace("keyword", propertie)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    # Send a GET request to the modified URL
    response = requests.get(webProduct, headers=headers)
      # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Implement image search logic here by finding image elements on the page
        if not checkNotFound(website.notFoundMsg, soup):  #IMPROVE THIS CODE TOO
            #find all images in the page
            #save 3 images with the barcode name in the Images folder
            #convert image to webp format
            images = get_images(website.divClass,soup)
            
            if(len(images) > 0):
              path = f"./Images"
              if not os.path.exists(path):
                os.makedirs(path)
              save_image_from_url(images[0],path+"/"+product.barcode+"_"+str(image_num)+".webp")
              product.imageExists = 1 
              #update row in the new_restaurants.xlsx file to imageExists = 1 
              return True #save in the new file
                #then update the new_items.xlsx file
    else:
        # If the request was not successful, print an error message and return False
      print("Error: Unable to retrieve data from >> "+ website.url)
      return False
    
    
def checkNotFound(notFoundMsg, soup):    
    try:
        # Find all occurrences of the specified text
        occurrences = soup.find_all(string=lambda t: notFoundMsg in str(t))    
        # Print the found occurrences
        if len(occurrences) == 0:
            return False
        else:
            return True
    except Exception as e:
        print(f"Error occurred while accessing website: {e}")
        return True



def updateRowInExcelFile(df, product): #DONE
  # Define the condition for updating
  
  # Update the row where the condition is True
  df.loc[condition, 'Age'] = 31  # Change Bob's age to 31
  # Print the updated DataFrame
  df.to_excel('New_Kalinka.xlsx', index=False)


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
websitesList = loadWebsitesfromFile(websitesPath) #refactor to parse to objects products

productsList = loadProductsfromFile("./Items/New_Kalinka.xlsx")

iterator = 0
img_saved = 0
minimunBarcodeDigits = 6

for product in productsList: #search for image on websites
  for website in websitesList:
    if product.barcode == 'nan' or len(product.barcode) < minimunBarcodeDigits:
      break
    else: 
      print("invalid barcode")
    if searchProductOnWebsite(website, product,iterator):
      img_saved += 1
      break
    iterator += 1
    
    
    
print("|| =========================<< REP0RT >>================================= ||")
print(f"Images saved: {img_saved}")
print(f"Images not saved: {iterator - img_saved}")
print(f"Total images: {iterator}")
print("|| ====================================================================== ||")
#save the new file
