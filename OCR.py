#this is to extract the text from a pdf. I need to recreate multiple versions of this depending on what bank it is from. 

#first run main
#second run history
#third copy paste and rename payee to description 
#fourth fill in the values and get empty values pycharm

import pandas as pd
import pdfplumber
from config import *
import os
import datetime
import re
from process_df import *

# Function to extract text and other information from a page
def extract_original(page):
    text = page.extract_text()
    count = text.lower().count('page')
    account_activity = text.lower().count('account activity')
    h = page.height
    w = page.width
    return text, count, h, w, account_activity

# Function to get table data from a cropped page
def get_table_data(table_settings, page1): 
    pageim = page1.to_image()
    table = page1.extract_table(table_settings)
    return table

# Function to convert table to DataFrame
def print_df(table): 
    df = pd.DataFrame(table[1:], columns=table[0])
    return df

# Function to process each page and extract the table
def get_rows(page):
    text, count, h, w , account_activity = extract_original(page)
    if count == 0 or account_activity == 0: 
        return None
    else: 
        while True: 
            if count == 0:
                break
            h = h - 9
            crop_box = (0, 0, w, h)
            page1 = page.within_bbox(crop_box)
            text = page1.extract_text()
            count1 = text.lower().count('page')
            if count > count1: 
                break
        table = get_table_data(table_settings, page1)
        return table

# Open the PDF file
def driver(file_path):
    pdf = pdfplumber.open(file_path)
    all_pages = []  # List to store all DataFrames

    # Loop through each page and extract the table
    for page in pdf.pages: 
        table = get_rows(page)
        if table is not None:  # Check if table extraction was successful
            try:
                df = print_df(table)
                all_pages.append(df)
            except Exception as e: 
                print(f"Error processing page: {e}")

    # Combine all DataFrames into a single DataFrame
    if all_pages:  # Ensure that all_pages is not empty
        combined_df = pd.concat(all_pages, ignore_index=True)
        combined_df = combined_df[~(combined_df == '').all(axis=1)]
        return combined_df
    else:
        print("No tables found in the PDF.")
        return pd.DataFrame()  # Return an empty DataFrame if no tables are found


pattern_date = re.compile(r'^\d{2}/\d{2}/\d{4}$')

def is_valid_date(date_str):
    """Check if the date_str matches MM/DD/YYYY format."""
    if pd.isna(date_str):
        return False
    if bool(pattern_date.match(date_str)) == True:
        return bool(pattern_date.match(date_str))
    else: 
        print(f'wrong date {date_str}')
        return bool(pattern_date.match(date_str))



# Apply function to filter DataFrame


def main(file_path):
    if os.path.isdir(file_path):
        all_df = []  # Flat list to store all DataFrames from all files
        for filename in os.listdir(file_path):
            full_path = os.path.join(file_path, filename)
            if os.path.isfile(full_path):  # Check if it's a file
                try: 
                    combined_df = driver(full_path)
                    all_df.append(combined_df)
                except Exception as e: 
                    print(f'Problem with {full_path}: {e}')
        # Concatenate all DataFrames from all files
        if all_df:  # Ensure that all_df is not empty
            final_combined_df = pd.concat(all_df, ignore_index=True)
            final_combined_df = final_combined_df[~(final_combined_df == '').all(axis=1)]
            print(final_combined_df.shape)
            columns = ["Date", "Memo", "Deposits and Other Credits(+)","Withdrawals & Other Debits (-)"]
            if len(final_combined_df.columns) == len(columns):
                final_combined_df.columns = columns
            else:
                print("The number of columns does not match the length of the column names list.")

            final_combined_df = final_combined_df[final_combined_df['Date'].apply(is_valid_date)]
            final_combined_df = final_combined_df[final_combined_df['Memo'].str.strip() != 'BEGINNING BALANCE']
            final_combined_df['Description'] = None
            final_combined_df['Account']=None
            final_combined_df['Description'] = final_combined_df['Memo'].apply(process_description)
            final_combined_df = final_combined_df[['Date','Description','Account','Memo','Deposits and Other Credits(+)','Withdrawals & Other Debits (-)']]
            
            print(final_combined_df.columns)
            
            print(final_combined_df.to_string())
            final_combined_df.reset_index()
            final_combined_df.to_clipboard(index = True)
        else:
            print("No tables found in any of the files.")


main(file_path)
