import re


table_settings = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "text",
    "snap_y_tolerance": 4,
    "intersection_x_tolerance": 3,
}

file_path_config = "/Users/jinhe/Documents/M&T Bank/Files(1)/chase rako arligton 20220531-statements-5392-.pdf"

# '/Users/jinhe/Documents/Different Bank Types/Chase Business Select Checking.pdf'
base_year_config = '20'
date_config = 'Date'
deposit_config = "Deposits and Other Credits(+)"
withdrawal_config = "Withdrawals & Other Debits (-)"
account_config = 'Account'
memo_config = 'Memo'
checks_config = 'Checks'
description_ai_config = 'Name Suggested'
description_config = 'Description'
columns_config = ["Date", "Memo", "Deposits and Other Credits(+)","Withdrawals & Other Debits (-)"]
all_columns_config = [date_config,description_config,account_config,memo_config,deposit_config,withdrawal_config]

bank_config = ['MANUFACTURERS AND TRADERS TRUST COMPANY','JPMORGAN CHASE BANK','WWW.CHASE.COM','BANK OF AMERICA']

year_formats_config = [
    re.compile(r'( *).*,.*through.*, (.*)',flags=re.IGNORECASE),
    re.compile(r'(Opening\/Closing Date) \d{2}\/\d{2}\/\d{2} - \d{2}\/\d{2}\/(\d{2})')
]

num_deposits_config = [ 
    re.compile(r' *?Deposits *?(-?\$?\b(?:\d{1,3}(?:,\d{3})*|\d*)\.\d{2}\b|(?<=\s)\.\d{2}(?=\s|$))',flags=re.IGNORECASE),
    re.compile(r' *?Total Deposits and Additions *?(?:\$)? *?(-?\$?\b(\d{1,3}(?:,\d{3})*|\d*)\.\d{2}\b|(?<=\s)\.\d{2}(?=\s))( *)',flags=re.IGNORECASE)
                       

] 

#chase
cdda_config = re.compile(r'^( *DATE *)?\n?( *CHECK NO\.| *?CHECK *?NUMBER)( *DESCRIPTION)?( *PAID| *DATE)?( *AMOUNT) *?$', flags=re.IGNORECASE)
cdda_pattern_config = re.compile(r'^ *?(\d{3,6}) *?\^? *?(.*?)(\d{1,2}\/\d{1,2}(?:\/\d{2,4})?) *?(-?\$?\b(?:\d{1,3}(?:,\d{3})*|\d*)\.\d{2}\b|(?<=\s)\.\d{2}(?=\s|$)) *?$',flags=re.IGNORECASE)

#TD Bank example:
#POSTING DATE DESCRIPTION     AMOUNT
#chase example: 
#DATE DESCRIPTION AMOUNT
#chase cc example: 
#Merchant Name or Transaction Description $ Amount


dda_config = re.compile(r'^( *?POSTING)?( *?DATE)?( *?DESCRIPTION| *?Merchant Name or Transaction Description)( *?\$? *?AMOUNT) *$', flags=re.IGNORECASE)
dda_pattern_config = re.compile(r'^ *?(\d{1,2}\/\d{1,2}(?:\/\d{2,4})?)(.*?)(-?\$?\b(?:\d{1,3}(?:,\d{3})*|\d*)\.\d{2}\b|(?<=\s)\.\d{2}(?=\s|$)) *?$',flags=re.IGNORECASE)

ddab_config = re.compile(r'^( *DATE)( *DESCRIPTION)( *AMOUNT)( *BALANCE) *?$',flags = re.IGNORECASE)
ddab_pattern_config = re.compile(r'^ *?(\d{1,2}\/\d{1,2}(?:\/\d{2,4})?)(.*?)(-?\$?\b(?:\d{1,3}(?:,\d{3})*|\d*)\.\d{2}\b|(?<=\s)\.\d{2}(?=\s|$)) *?-?\$?\b(?:\d{1,3}(?:,\d{3})*|\d*)\.\d{2}\b|(?<=\s)\.\d{2}(?=\s|$) *?$',flags=re.IGNORECASE)

#citi bank
dddcb_config = re.compile(r'^( *Date)( *Description)( *Debits)( *Credits)( *Balance)',flags=re.IGNORECASE)

#American Express CC
#date, description, payment
#Example: 
#Payments Amount
#Credits Amount
# Amount
pa_config = re.compile(r'^( *?Payments|( *?Credits))?( *?)Amount( *?)',flags=re.IGNORECASE)



headings_config = {
    pa_config:dda_pattern_config,
    cdda_config: cdda_pattern_config,    
    dda_config: dda_pattern_config,
    ddab_config: ddab_pattern_config,
    dddcb_config:ddab_pattern_config

}



#     pattern_date = re.compile(r'\d{1,2}\/\d{1,2}(\/\d{2,4})?')  # Pattern to match MM/DD format
#     pattern_price = re.compile(r'(-?\$?\b(\d{1,3}(?:,\d{3})*|\d*)\.\d{2}\b|(?<=\s)\.\d{2}(?=\s|$))')

ignore_config = [
    #TD BANK and BOA
    re.compile(r'( *)DATE( *)BALANCE( *)(\(.*\))?( *)DATE( *)BALANCE( *)(\(.*\))?',flags=re.IGNORECASE),
    #PNC Bank
    re.compile(r'( *)DATE( *)Ledger balance( *)DATE( *)Ledger balance',flags=re.IGNORECASE),
    #chase bank
    re.compile(r'^( *)DATE( *)AMOUNT( *)DATE( *)AMOUNT',flags=re.IGNORECASE),
    #citi bank ignore checks
    re.compile(r'^Check( *)Date( *)Amount( *)Check( *)Date( *)Amount')

]
