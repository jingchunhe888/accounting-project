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
Redmond
Seoul
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
            # return description


    pattern_end_two_upper = re.compile(r'\b[A-Z]{2}\b$')
    match_end_two_upper = re.search(pattern_end_two_upper,description)
    if match_end_two_upper:
        description = re.sub(match_end_two_upper,'')
        # return description

    # return description

def process_description(description):
    #phone number
    description = re.sub(r'\b\d{3}-?\d{3}-?\d{4}\b', '', description)
    #long numbers before I replace with space
    #merge receipts 
    description = re.sub(r'(\d{5,})\s?(\d{5,})',r'\1\2',description)

    #dates

    

    pattern_payment_to = r'^.*?Payment.*?To (.*)'
    match = re.search(pattern_payment_to, description, re.IGNORECASE)
    if match:
        part_after_to = match.group(1).strip()
        if re.search('[a-zA-Z]{2,}',part_after_to):
            description = part_after_to
        # print(f'hihi {part_after_to}')
    
    

        # Check if there are any digits in the part after 'Payment To'
        #update need to see what is wrong
        # if any(char.isdigit() for char in part_after_to):
        #     # If there are digits, return the whole part
        #     pass
        # else:
        #     description = part_after_to

    pattern_state_card = re.compile(r'(New York)? (([A-Z]){2})? Card \d{4}')
    description = re.sub(pattern_state_card,'',description)
    # match_pattern_state_card = re.search(pattern_state_card, description)
    # if match_pattern_state_card:
    #     matched_text = match_pattern_state_card.group()
    #     modified_text = re.sub(r'[A-Z]{2}', '', matched_text)
    #     description = description.replace(matched_text, modified_text)
    #     description = ' '.join(description.split())
    # else:
    #     pass
    description = re.sub(r'(\d{2}/\d{2})', '', description)


    #do not delete everything beforehand 
    #description = re.sub(r'(.*)(\d{2}/\d{2})', '', description)

    # pattern_card_transfer = re.compile(r'Ending In \d{4}', flags=re.IGNORECASE)
    # match_card_transfer = re.search(pattern_card_transfer, description)
    # if match_card_transfer:
    #     description = re.sub("Payment To ", "Payment To/From ", description).strip()
    #     return description.strip()

    # description = delete_places(description)
    # pattern_star = re.compile(r'\b\w*\*\w*\b')
    # match_star = re.search(pattern_star, description)
    # if match_star:
    #     match_star = match_star.group()
    #     if re.search(r'[a-zA-Z]',match_star):
    #         if re.search(r'\d', match_star):
    #             pass
    #         description = re.sub(r'\S*\*', '', description)
    #     else:
    #         description = re.sub(r'\S*\*', '', description)

    #chase bank characteristics 
    pattern = r'Orig CO Name:(.*?) Orig ID:'
    match = re.search(pattern, description)
    if match:
        description = match.group(1).strip()
    description = re.sub(r'PPD ID:','', description)
    description = re.sub(r'CCD ID:','', description)
    description = re.sub(r'Web ID:','', description)
    description = re.sub(r'^(Recurring )?Card Purchase (With Pin)?','',description)
    description = re.sub(r'^Refund of', '', description)
    
    pattern_adj_fee = r'Foreign Exch Rt ADJ Fee.*'
    match = re.search(pattern_adj_fee,description)
    if match: 
        description = 'Foreign Exch Rt ADJ Fee'
        return description
    # description = re.sub(r'CP WEB PYMT P','',description)
    # description = re.sub(r'In [EDI ]?P[A]?YM[E]?NTS','',description)
    # description = re.sub(r'I EDI PYMNTS','',description)
    # description = re.sub(r'RES \d{4}','',description,flags=re.IGNORECASE)
    # description = re.sub(r'Gametime Orders Gametime 0','Gametime',description)

    #payment processors
    description = re.sub(r'SP\s*\*', ' ', description) #ADDED THIS
    description = re.sub(r'Sq\s*\*','', description,flags=re.IGNORECASE) #MOVED TO BEGINNING
    description = re.sub(r'Tst\s*\*', '', description, flags=re.IGNORECASE)  # MOVED TO BEGINNING
    # description = re.sub(r'\.Com\*','.Com ',description, flags=re.IGNORECASE)
    
    description = re.sub(r'\.\.\.', ' ', description)
    #special characters, not & not () not /
    description = re.sub(r'[!"#\$%\'*+,.:;<=>?@[\\\]\^_`{|}~]',' ',description)
    description = re.sub(r' {2,}',' ',description)
    word_counts = len(description.split())
    if word_counts < 2: 
        pass
    else: 
        description = re.sub(r'\d{7,}','',description)
        description = re.sub(r'\(.*\)', '', description)

    word_counts = len(description.split())
    if word_counts <= 1:
        pass
    else:
        #pattern_receipt = re.compile(r'[a-zA-Z\d]{6,}(-[a-zA-Z\d]{1,})*')
        pattern_receipt = re.compile(r'(?=.*?\d)(?=.*?[a-zA-Z])[a-zA-Z\d]{4,}')
        # match_receipt = re.search(pattern_receipt,description)
        match_receipt_iter = re.finditer(pattern_receipt, description)
        # description = re.sub(pattern_receipt,'',description)
        for match in match_receipt_iter:
            match = match.group()
            # print(match)
            if re.search(r'[a-zA-Z]', match):
                if re.search(r'\d', match):
                    description = re.sub(match, '', description)
    description = re.sub(r'-',' ',description)
    description = re.sub(r' {2,}',' ',description)

    word_counts = len(description.split())
    if word_counts <=1:
        pass
    else:
        description = re.sub(r'\b(?=\w*\d)(?=\w*[a-zA-Z\-!"#\$%\'*+,.:;<=>?@[\\\]\^_`{|}~])[a-zA-Z0-9-\-!"#\$%\'*+,.:;<=>?@[\\\]\^_`{|}~]{4,}\b','',description)
        # description = re.sub(r'\d{5,9}', '', description)
        # description = re.sub(r'Transfer To Chk | Transfer From Chk', ' Transfer To/From', description)
        # description = re.sub(r'\S*#\S*', '', description)
    description = description.strip()
    description = re.sub(r'(Assoc|Corp.*|Inc.*|Ltd|Mfg|Mfrs|LLC.*)$','',description,flags=re.IGNORECASE)
    # pattern_amazon = re.compile(r'Amzn Mktp US Amzn\.Com/Bill')
    # match_pattern_amazon = re.search(pattern_amazon, description)
    # if match_pattern_amazon:
    #     description = 'Amzn Mktp Amzn.Com/Bill'
    #     return description
    # print('this is description' + description)
    return description.strip()
