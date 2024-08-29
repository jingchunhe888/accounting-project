import re
import pandas as pd

places = '''New York
Long Is City
Long Island C
Muellheim
Kifisia
San Francisco
Long Island C Astoria
LONG ISALND C ASTORIA
Long Island Long Island C
LONG ISLAND C LONG ISLAND C
Los Angeles
Long Island
Miami Beach
Koebenhavn
Las Vegas
Astoria
London
Seoul
Western Queens
San Luis Obis
South Beach
NEW YORK NEW YORK 
HENDERSON
WOODSIDE WOODSIDE
Toronto
Miami
CALIFON
NEWARK
LONG ISLAN LONG ISLAND C
Denville
ALBUQUERQUE
BROOKLYN
Columbus
Tucson 
Dallas
Washington
Washington DC
JAMAICA
'''

def delete_places(description):

    global places
    place_list = []
    place_line = places.split('\n')
    for place in place_line:
        place_list.append(place)
    for place in place_list:
        pattern_place = re.compile(re.escape(place) + r' \b[A-Z]{2}\b',flags = re.IGNORECASE)
        match_place = re.search(pattern_place, description)
        if match_place:
            sub = match_place.group()
            description = re.sub(sub, '', description)
            return description


    pattern_end_two_upper = re.compile(r'\b[A-Z]{2}\b$')
    match_end_two_upper = re.search(pattern_end_two_upper,description)
    if match_end_two_upper:
        description = re.sub(match_end_two_upper,'')
        return description

    return description




def process_description(description):
            pattern = r'Orig CO Name:(.*?) Orig ID:'
            match = re.search(pattern, description)
            if match:
                return match.group(1).strip()
            else:
                pass

            pattern_payment_to = r'^.*?Payment.*?To (.*)'
            match = re.search(pattern_payment_to, description, re.IGNORECASE)
            if match:
                part_after_to = match.group(1).strip()
                print(f'hihi {part_after_to}')

                # Check if there are any digits in the part after 'Payment To'
                if any(char.isdigit() for char in part_after_to):
                    # If there are digits, return the whole part
                    pass
                else:
                    return part_after_to

            pattern_amount = re.compile(r'IN The Amount of', flags=re.IGNORECASE)
            match_pattern_amount = re.search(pattern_amount, description)
            if match_pattern_amount:
                print(description)
                return description.strip()

            pattern_fee = re.compile(r'Foreign Exch Rt ADJ Fee')
            match_fee = re.match(pattern_fee, description)
            if match_fee:
                description = 'Foreign Exch Rt ADJ Fee'
                return description

            pattern_nyctaxi = re.compile(r'Nyctaxi', flags=re.IGNORECASE)
            match_nyctaxi = re.search(pattern_nyctaxi, description)
            if match_nyctaxi:
                description = 'NycTaxi'
                return description

            pattern_taxisvc = re.compile(r'Curb Svc', flags=re.IGNORECASE)
            match_taxisvc = re.search(pattern_taxisvc, description)
            if match_taxisvc:
                description = 'Curb Svc'
                return description

            pattern_state_card = re.compile(r'[A-Z]{2} Card.*')
            match_pattern_state_card = re.search(pattern_state_card, description)
            if match_pattern_state_card:
                matched_text = match_pattern_state_card.group()
                modified_text = re.sub(r'[A-Z]{2}', '', matched_text)
                description = description.replace(matched_text, modified_text)
                description = ' '.join(description.split())
            else:
                pass
            description = re.sub(r'(.*)(\d{2}/\d{2})', '', description)
            description = re.sub(r'\d{3}-?\d{3}-?\d{4}.*', '', description)
            description = re.sub(r'CCD ID.*', '', description)
            description = re.sub(r'PPD ID.*', '', description)
            description = re.sub(r'Orig CO Name:', '', description)
            description = re.sub(r'Orig ID:.*', '', description)

            pattern_card_transfer = re.compile(r'Ending In \d{4}', flags=re.IGNORECASE)
            match_card_transfer = re.search(pattern_card_transfer, description)
            if match_card_transfer:
                description = re.sub("Payment To ", "Payment To/From ", description).strip()
                return description.strip()

            description = delete_places(description)
            pattern_star = re.compile(r'\b\w*\*\w*\b')
            match_star = re.search(pattern_star, description)
            if match_star:
                match_star = match_star.group()
                if re.search(r'a-zA-Z' and r'\d', match_star):
                    pass
                else:
                    description = re.sub(r'\S*\*', '', description)

            description = re.sub(r'Sq\s*\*','', description,flags=re.IGNORECASE) #MOVED TO BEGINNING
            description = re.sub(r'CP WEB PYMT P','',description)
            description = re.sub(r'In [EDI ]?P[A]?YM[E]?NTS','',description)
            description = re.sub(r'I EDI PYMNTS','',description)
            description = re.sub(r'RES \d{4}','',description,flags=re.IGNORECASE)
            description = re.sub(r'Gametime Orders Gametime 0','Gametime',description)
            description = re.sub(r'Tst\s*\*', '', description, flags=re.IGNORECASE)  # MOVED TO BEGINNING
            description = re.sub(r'\.Com\*','.Com ',description, flags=re.IGNORECASE)
            description = re.sub(r'SP\s*\*', ' ', description) #ADDED THIS
            description = re.sub(r'\*', ' ', description) #ADDED THIS
            description = re.sub(r'_', ' ',description)
            description = re.sub(r',', ' ', description)
            description = re.sub(r'^\s*&', '', description)
            #pattern_receipt = re.compile(r'[a-zA-Z\d]{6,}(-[a-zA-Z\d]{1,})*')
            pattern_receipt = re.compile(r'((?=.*?\d)(?=.*?[a-zA-Z])[a-zA-Z\d]+$)')
            match_receipt = re.search(pattern_receipt,description)
            match_receipt_iter = re.finditer(pattern_receipt, description)
            description = re.sub(r'-', ' ', description)
            word_counts = len(description.split())

            if word_counts < 2:
                pass
            else:
                # pattern_store_number = re.compile(r'\d')  # CHANGED TO SIX
                # match_store_number = re.search(pattern_store_number, description)
                # match_store_number_iter = re.finditer(pattern_store_number, description)
                if match_receipt:
                    for match in match_receipt_iter:
                        match = match.group()
                        if re.search(r'a-zA-Z' and r'\d', match):
                            description = re.sub(match, '', description)
                description = re.sub(r'\d{5,9}', '', description)
                description = re.sub(r' - ', ' ', description)
                description = re.sub(r'Transfer To Chk | Transfer From Chk', ' Transfer To/From', description)
                description = re.sub(r'\.\.\.', ' ', description)
                description = re.sub(r'\S*#\S*', '', description)

            description = ' '.join(description.split())
            pattern_amazon = re.compile(r'Amzn Mktp US Amzn\.Com/Bill')
            match_pattern_amazon = re.search(pattern_amazon, description)
            if match_pattern_amazon:
                description = 'Amzn Mktp Amzn.Com/Bill'
                return description
            description = ' '.join(description.split())
            # print('this is description' + description)
            return description


# Load the Excel file and specify the sheet and column(s)
df = pd.read_excel('/Users/jinhe/Documents/Event 365 LLC.xlsx', sheet_name='2023')

# Initialize an empty list to store processed descriptions
description = []

# Iterate over each value in the "Description" column
for value in df['Description']:
    if pd.isna(value) or value == '':  # Check if the value is NaN or an empty string
        description.append('')  # Append an empty string for NaN or empty values
    else:
        new = process_description(value)  # Apply your processing function to non-empty values
        description.append(new)  # Append the processed value to the list

# Convert the 'description' list into a DataFrame with a column named "Description"
description_df = pd.DataFrame(description, columns=['Description'])
description_df.to_clipboard(index=False)
# Print the resulting DataFrame
print(description_df)


