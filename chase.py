#ocr for chase bank statements

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd
import re
from pdf import *
import os
import time
import datetime
import sys
from config import *

def process_data(text, year, count):

    pattern_date = re.compile(r'(\d{2}/\d{2})')  # Pattern to match MM/DD format
    pattern_price = re.compile(r'(-?\$?\b(\d{1,3}(?:,\d{3})*|\d*)\.\d{2}\b|(?<=\s)\.\d{2}(?=\s|$))')
    # pattern_price = re.compile(r'-?\$?\b\d{1,3}(?:,\d{3})*\.\d{2}\b')
    pattern_check_number = re.compile(r'\d{3,6}')

    # pattern_aba = re.compile(r'Body Evolution')

    # CC
    # def changesign():
    #     if forever:
    #         sign = 'Payment'
    #     else:
    #         sign = 'Deposit'
    #     return sign

    lines = text.split('\n')
    dates = []
    prices = []
    descriptions = []
    checks = []
    # signs = []
    memo = []

    has_date = False
    has_price = False
    has_check = False

    year_provided = False
    forever = False
    year = year
    # lines = [line for line in lines if pattern_date.match(line) or pattern_check_number.match(line)]

    for line in lines:
        type = 'description'
        match_date = re.search(pattern_date, line)  # Search for MM/DD format
        match_price = re.search(pattern_price, line)  # Search for price with optional comma and decimal
        match_check = re.match(pattern_check_number, line)

        if match_check:
            type = 'check'
            has_check = True

        if match_price:
            price = match_price.group()
            price = price.replace('$', "")
            price = price.replace(',', '')
            price_float = float(price)
            if price_float < 0:
                sign = 'Deposit'
            else:
                sign = 'Payment'
            # price = price.replace('-','')
            price = f"{float(price):.2f}"
            price = float(price)
            has_price = True

        if match_date:
            date = match_date.group()
            # Check if the date includes a year
            if len(date.split('/')) == 2:
                if not year_provided:
                    # Ask the user for the year if not already provided
                    year_provided = True
                date += f'/{year}'
            # dates.append(date)
            has_date = True

            # Extract the description starting after the date
            start = match_date.end()

            if (type == 'description' and has_date and has_price):
                if match_price:
                    end = match_price.start()
                    description = line[start:end].strip()
                else:
                    description = line[start:].strip()
                full_description = description
                memo.append(full_description)
                description = process_description(description)
                descriptions.append(description)
                prices.append(price)
                dates.append(date)
                checks.append('')
                # CC
                # sign = changesign()
                # signs.append(sign)

        if (type == 'check' and has_check and has_date and has_price):
            match_check = re.match(pattern_check_number, line)
            if match_check:
                check = match_check.group()
                descriptions.append('Check')
                checks.append(check)
                forever = True
                # CC
                # sign = changesign()
            prices.append(price)
            dates.append(date)
            # signs.append(sign)
            memo.append('')

        has_date = False
        has_check = False
        has_price = False

    print(len(dates))
    print(len(prices))
    print(len(descriptions))
    print(len(checks))
    # print(len(signs))
    df = pd.DataFrame({'Date': dates, 'Description': descriptions, 'Price': prices, 'Checks': checks,
                        'Memo': memo})  # ,deleted'Transaction Type': signs
    df['Account'] = None

    if count > 1:
        df['Transaction Type'] = ['Deposit' if i < count else 'Payment' for i in range(len(df))]

    # If count is 0, then all are 'Payment'
    if count <1:
        df['Transaction Type'] = 'Payment'

    df['Invoices'] = df.apply(
        lambda
            row: f'=TEXT("{row["Date"]}", "mmddyyyy") & " " & "{self.end_date}" & " " & "{row["Description"]}" & " $" & "{row["Price"]:.2f}"'
        if row['Transaction Type'] == 'Payment' else '',
        axis=1
    )

    account_order = ['Date', 'Description', 'Account', 'Price', 'Checks', 'Memo', 'Transaction Type',
                        'Invoices']
    df = df[account_order]

    print(df.shape)
    return df
    # df.to_clipboard(index=False)

    # print(df.Date.to_string())
    # print(df.Description.to_string())
    # print(df.Price.to_string())
    # df = df.to_string(index = False)
    # print(df)

    # print(df.Date.to_string())
    # print(df.Description.to_string())
    # print(df.Price.to_string())
    # df = df.to_string(index = False)
    # print(df)

    # return df

    # description = re.sub(r'\S*\d\S*', '', description)  # Remove digits
    # description = re.sub(r'\b(?:CCD|ID|Bkcd|Stlmt|PPD)\b', '', description, flags=re.IGNORECASE)
    # description = re.sub(r'https', '', description, flags=re.IGNORECASE).strip()
    # description = re.sub(r'http', '', description, flags=re.IGNORECASE).strip()
    # description = re.sub(r'www', '', description, flags=re.IGNORECASE).strip()
    # description = re.sub(r'\bRecurring Card Purchase\b', '', description, flags=re.IGNORECASE).strip()
    # description = re.sub(r'\bCard Purchase\b', '', description, flags=re.IGNORECASE).strip()
    # description = re.sub(r'With Pin', '', description, flags=re.IGNORECASE).strip()
    # description = re.sub(r'\b(?:Card)\b', '', description, flags=re.IGNORECASE)
    # description = re.sub(r'\bTsysTransfirst\s+', '', description).strip()
    # description = re.sub(r'\b[A-Z]{2}\b', '', description)
    # description = re.sub(r'New York', '', description)
    # description = re.sub(r'[\/\\,-]', '', description)
    # description = re.sub(r'(\.com)(?=.*\.com)', '', description, flags=re.IGNORECASE)
    # description = re.sub(r'\.(?!com)', '', description, flags=re.IGNORECASE)
    # word_counts = len(description.split())
    # if word_counts < 2:
    #     description = re.sub(r'.com', '', description, flags=re.IGNORECASE)
    #     print(word_counts)
    # else:
    #     description = re.sub(r'\S*\.com\S*', '', description, flags=re.IGNORECASE)  # Remove .com and following word
    #     description = re.sub(r'\S*\.com\S*', '', description, flags=re.IGNORECASE).strip()
    #
    # description = re.sub(r'[.-:\*]', ' ', description)
    #
    #
    # # Remove everything after a digit without a preceding space
    # description = re.sub(r'(\S*\d\S*).*', '', description)
    # description = ' '.join(description.split())

    # description = re.sub(r'\d', '', description)
    # description = re.sub(r'\b(?:Card|Purchase|CCD|ID|Bkcd|Stlmt)\b', '', description, flags=re.IGNORECASE)
    # description = re.sub(r'\bTsysTransfirst\s+', '', description).strip()
    # description = re.sub(r'[\/\\,]', '', description)
    # description = re.sub(r'\.com\b', '', description, flags=re.IGNORECASE)
    # description = re.sub(r'[.-:]', '', description)>

    # Create DataFrame from dates and prices

def chase(file_path):


    if os.path.isdir(file_path):
        all_df = []
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

    #add extra section for individual files
    else:
        if os.path.isfile(file_path):  # Check if it's a file
            try: 
                combined_df = driver(file_path) #instead of full_path
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
    # folder_path = r'/Users/jinhe/Downloads/BodhiSattva Enterprises LLC/Bank Statements/5632- PERSONAL/2021'

    # 1
    # count = 0
    # for filename in os.listdir(folder_path):
    #     file_path = os.path.join(folder_path, filename)
    #     QB_file_1 = main_pdf(file_path)
    #     df = process_data(QB_file_1,year)
    #     df['Ref']=count
    #     count += 1
    #     all_df.append(df)
    #     print(df.shape)
    # combined_df = pd.concat(all_df, ignore_index=True)
    # return combined_df

    # 1
    # 1

    #returns the text of the pdf file
    QB_file_1 = main_pdf(file_path_config)
    print(QB_file_1)



    count = get_count()+1
    print(f'this is count type {type(count)}')
    # df = process_data(QB_file_1, self.start_date, count)
    # all_df.append(df)
    # print(df.shape)
    # combined_df = pd.concat(all_df, ignore_index=True)
    # return combined_df

def save_dataframe_to_excel(df, file_path):
    directory, filename_with_ext = os.path.split(self.file_path_statement)
    filename, ext = os.path.splitext(filename_with_ext)
    with pd.ExcelWriter(file_path, if_sheet_exists="replace",
                        mode='a') as writer:
        df.to_excel(writer, sheet_name=filename, index=False)
    print(f"DataFrame has been written to the '{filename}' sheet in '{file_path}'.")

end_date = datetime.datetime(2024, 10, 20)  # Example: 5th August 2024

# Get the current date
current_date = datetime.datetime.now()

# main_get_df(file_path_config)
