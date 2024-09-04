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
from chase import *

def format_date(date):
    pattern_date = re.compile(r'^\d{1,2}\/\d{1,2}\/\d{2,4}$')
    if pattern_date.match(date):
        month, day, year = date.split('/')
        month = month.zfill(2)
        day = day.zfill(2)
        if len(year) == 2:
            year = base_year_config + year
        formatted_date = f'{month}/{day}/{year}'
        return formatted_date
    else: 
        return date

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
    # pageim = page1.to_image()
    table = page1.extract_table(table_settings)
    return table

# Function to convert table to DataFrame
def print_df(table): 
    df = pd.DataFrame(table[1:], columns=table[0]).reset_index(drop=True)
    return df

# Function to process each page and extract the table
def get_rows(page):
    text, count, h, w , account_activity = extract_original(page)
    if count == 0: 
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
        # return page1
        table = get_table_data(table_settings, page1)
        return table

# Open the PDF file
def bank_main(file_path):
    pdf = pdfplumber.open(file_path)
    all_pages = []  # List to store all DataFrames

    # Loop through each page and extract the table
    for page in pdf.pages: 
        table = get_rows(page)
        if table is not None:  # Check if table extraction was successful
            try:
                df = print_df(table).reset_index(drop=True)
                common_columns = ['', '', '', '']
                df = df.reindex(columns=common_columns)
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

def is_valid_date(date_str):
    pattern_date = re.compile(r'^\d{1,2}\/\d{1,2}\/\d{2,4}$')
    """Check if the date_str matches MM/DD/YYYY format."""
    if pd.isna(date_str):
        return False
    if bool(pattern_date.match(date_str)) == True:
        return bool(pattern_date.match(date_str))
    else: 
        print(f'wrong date {date_str}')
        return bool(pattern_date.match(date_str))



# Apply function to filter DataFrame


def driver(file_path, bank):
    if os.path.isdir(file_path):
        all_df = []  # Flat list to store all DataFrames from all files
        for filename in os.listdir(file_path):
            full_path = os.path.join(file_path, filename)
            if os.path.isfile(full_path):  # Check if it's a file
                if bank == bank_config[0]:
                    try: 
                        combined_df = bank_main(full_path)
                        all_df.append(combined_df)
                    except Exception as e: 
                        print(f'Problem with {full_path}: {e}')
                if bank == bank_config[1]:
                    print('to be determined 1')
        # Concatenate all DataFrames from all files
        if bank == bank_config[0]:
            if all_df:  # Ensure that all_df is not empty
                final_combined_df = pd.concat(all_df, ignore_index=True)
                final_combined_df = final_combined_df[~(final_combined_df == '').all(axis=1)]
                # print(final_combined_df.shape)
                columns = columns_config
                if len(final_combined_df.columns) == len(columns):
                    final_combined_df.columns = columns
                else:
                    print("The number of columns does not match the length of the column names list.")

                final_combined_df = final_combined_df[final_combined_df['Date'].apply(is_valid_date)]
                final_combined_df['Date'] = final_combined_df['Date'].apply(format_date).astype(str)
                final_combined_df = final_combined_df[final_combined_df[memo_config].str.strip() != 'BEGINNING BALANCE']
                final_combined_df[description_config] = None
                final_combined_df['Account']=None
                final_combined_df[description_config] = final_combined_df[memo_config].apply(process_description)
                final_combined_df = final_combined_df[all_columns_config]
                
                # print(final_combined_df.to_string())
                final_combined_df.reset_index(drop=True, inplace=True)
                final_combined_df.to_clipboard(index = True)
            else:
                print("No tables found in any of the files.")
                
        if bank == bank_config[1]:
            print('to be determined 2')

    #add extra section for individual files
    else:
        if os.path.isfile(file_path):  # Check if it's a file
            if bank == bank_config[0]:
                m_and_t_file(file_path)
            if bank == bank_config[1]:
                print('to be determined')
            

def m_and_t_file(file_path):
    try: 
        combined_df = bank_main(file_path) #instead of full_path
        all_df = combined_df #instead of append
        if not all_df.empty:  # Ensure that all_df is not empty
            final_combined_df = all_df #instead of concat
            final_combined_df = final_combined_df[~(final_combined_df == '').all(axis=1)]
            # print(final_combined_df.shape)
            columns = columns_config
            if len(final_combined_df.columns) == len(columns):
                final_combined_df.columns = columns
            else:
                print("The number of columns does not match the length of the column names list.")

            final_combined_df = final_combined_df[final_combined_df['Date'].apply(is_valid_date)]
            final_combined_df['Date'] = final_combined_df['Date'].apply(format_date).astype(str)
            final_combined_df = final_combined_df[final_combined_df[memo_config].str.strip() != 'BEGINNING BALANCE']
            final_combined_df[description_config] = None
            final_combined_df['Account']=None
            final_combined_df[description_config] = final_combined_df[memo_config].apply(process_description)
            final_combined_df = final_combined_df[all_columns_config]
            
            # print(final_combined_df.to_string())
            final_combined_df.reset_index(drop=True, inplace=True)
            final_combined_df.to_clipboard(index = True)
        else:
            print("No tables found in any of the files.")
    except Exception as e: 
        print(f'Problem with {file_path}: {e}') #instead of full_path

        

def get_bank(file_path, bank): 
    pdf = pdfplumber.open(file_path)
    for page in pdf.pages:
        text = page.extract_text()
        bank_count = text.upper().count(bank)
        if bank_count > 0: 
            return bank
        else:
            return False

def main(file_path):
    if os.path.isdir(file_path):
        for filename in os.listdir(file_path):
            full_path = os.path.join(file_path, filename)
            if os.path.isfile(full_path):  # Check if it's a file
                check_bank(full_path, file_path)
    else:
        if os.path.isfile(file_path):
            check_bank(file_path, file_path)  # Check if it's a file

def check_bank(file_full_path, file_path):
    try: 
        for bank in bank_config: 
            is_bank = get_bank(file_full_path, bank)
            if is_bank: 
                driver(file_path, bank)
            else: 
                print("We cannot process your bank yet.")
    except Exception as e: 
        print(f'1 Problem with {file_full_path}: {e}')

    # try: 
    #     is_bank_1 = get_bank(file_full_path, bank_config)
    #     if is_bank_1: 
    #         print('i am chase')
    #     else: 
    #         print('we cannot process your bank')
    #         # chase(file_full_path)
    # except Exception as e: 
    #     print(f'1 Problem with {file_full_path}: {e}')
   
main(file_path_config)
