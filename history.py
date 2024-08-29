from config import *
import pandas as pd

# Load the Excel file
file_path = file_path_history_config # Replace with your file path
df = pd.read_excel(file_path, skiprows=3, sheet_name = 'QB 2022 Transactions')

# Drop rows where 'Payee' is NaN (empty)
df = df.dropna(subset=['Payee'])

# Remove duplicates based on the 'Payee' column, keeping the first occurrence
df_unique = df.drop_duplicates(subset=['Payee'], keep='first')

# Create a dictionary where 'Payee' is the key and 'Account' is the value
payee_account_dict = dict(zip(df_unique['Payee'], df_unique['Account']))

df_dict = pd.DataFrame(list(payee_account_dict.items()), columns=['Payee', 'Account'])

df_dict.to_clipboard(index=False)
# Print or use the dictionary as needed
print(df_dict.to_string())
