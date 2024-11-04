import pandas as pd
import cx_Oracle

# Load the necessary data
cleaned_data_path = r'C:\Users\ghass\Desktop\telecom-dashboard\backend\cleaned_data.csv'
price_list_path = r'C:\Users\ghass\Desktop\telecom-dashboard\data\Price List.xlsx'
calculated_data_path = r'C:\Users\ghass\Desktop\telecom-dashboard\frontend\public\calculated_data.csv'

# Load cleaned data
try:
    cleaned_data = pd.read_csv(cleaned_data_path, parse_dates=['ORIG_START_TIME'])
    print(f"Loaded cleaned data from {cleaned_data_path}.")
    print(f"Cleaned data shape: {cleaned_data.shape}")
except Exception as e:
    print(f"Error loading cleaned data: {e}")
    exit(1)

# Load price list
try:
    price_list = pd.read_excel(price_list_path)
    print(f"Loaded price list from {price_list_path}.")
    print("Price list columns:", price_list.columns)
except Exception as e:
    print(f"Error loading price list: {e}")
    exit(1)

# Ensure necessary columns are present
required_price_list_columns = ['Keyword', 'Prix unitaire']
required_cleaned_data_columns = ['SERVICE_TYPE']

missing_columns = [col for col in required_price_list_columns if col not in price_list.columns]
if missing_columns:
    print(f"Missing columns in price list: {missing_columns}")
    exit(1)

if 'SERVICE_TYPE' not in cleaned_data.columns:
    print("SERVICE_TYPE column is missing in cleaned_data.")
    exit(1)

# Merge cleaned data with price list
merged_data = pd.merge(cleaned_data, price_list, left_on='SERVICE_TYPE', right_on='Keyword', how='left')
print(f"Merged data shape: {merged_data.shape}")

# Filter out rows where SERVICE_TYPE ends with '_N'
merged_data = merged_data[~merged_data['SERVICE_TYPE'].str.endswith('_N')]
print(f"Data shape after removing SERVICE_TYPE ending with '_N': {merged_data.shape}")

# Filter data for successful events with specific event types
filtered_data = merged_data[
    (merged_data['EVENT_STATUS'] == 'Success') & 
    (merged_data['EVENT_TYPE'].isin([74, 75]))
]
print(f"Filtered data shape: {filtered_data.shape}")

# Truncate ORIG_START_TIME to only the date (yyyy/mm/dd)
filtered_data['ORIG_START_TIME'] = filtered_data['ORIG_START_TIME'].dt.date
print("Truncated ORIG_START_TIME to yyyy/mm/dd")

# Group by relevant columns and count the number of occurrences for NB_SMS and calculate the total price
grouped_data = filtered_data.groupby(
    ['B_MSISDN', 'ORIG_START_TIME', 'EVENT_TYPE', 'CALL_TYPE', 'EVENT_STATUS', 
     'SUBSCRIBER_TYPE', 'SERVICE_TYPE', 'RECORD_TYPE', 'Prix unitaire']
).agg(
    NB_SMS=('SERVICE_TYPE', 'size')
).reset_index()

# Calculate the total price for each group
grouped_data['TOTAL_PRICE'] = grouped_data['NB_SMS'] * grouped_data['Prix unitaire']

print(f"Grouped data shape: {grouped_data.shape}")

# Save the grouped data to a CSV file
grouped_data.to_csv(calculated_data_path, index=False)
print(f"Calculated data saved to {calculated_data_path} with {len(grouped_data)} rows.")

