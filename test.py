import pandas as pd

# Read the Excel file into a DataFrame
df = pd.read_excel('./Items/New_Kalinka.xlsx')

# Iterate over the DataFrame rows
for index, row in df.iterrows():
    # Access the 'Name' column and print its value
    print(row['Name'], row['Product Code'])