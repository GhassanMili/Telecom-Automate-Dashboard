import pandas as pd
from datetime import datetime

# Load the CSV file
file_path = r'C:\Users\ghass\Desktop\telecom-dashboard\data\ea6c5947-408f-490a-87f7-2f1b6ed05e08.csv'
try:
    data = pd.read_csv(file_path)
    print(f"Loaded data with {len(data)} rows.")
except Exception as e:
    print(f"Error loading data: {e}")
    exit(1)

# Select the necessary attributes
columns_needed = [
    'NE', 'FILENAME', 'A_MSISDN', 'B_MSISDN', 'START_TIME', 'PROC_HOUR', 'EVENT_TYPE', 
    'EVENT_TYPE_ORIG', 'CALL_TYPE', 'EVENT_STATUS', 'FILTER_CODE', 'SUBSCRIBER_TYPE', 
    'TRAFFIC_TYPE', 'SERVICE_TYPE', 'TEST_FLAG', 'CHARGE_AMOUNT_ORIG', 'PRICE_PLAN_CODE', 
    'ORIG_START_TIME', 'RECORD_TYPE', 'C_NUM', 'PARTIAL_SEQ_ID', 'LAST_PARTIAL'
]

# Filter the data to retain only the necessary attributes
data = data[columns_needed]
print(f"Data after selecting necessary attributes: {len(data)} rows.")

# Print unique values in 'START_TIME' to inspect any non-datetime entries
print("Unique START_TIME values before conversion:")
print(data['START_TIME'].unique())

# Handle known incorrect values or patterns
# Replace '_N' with a default valid date
data['START_TIME'] = data['START_TIME'].replace('_N', '2024-06-01 00:00:00')

# Convert 'START_TIME' to datetime, ignoring errors
data['START_TIME'] = pd.to_datetime(data['START_TIME'], errors='coerce')

# Print out rows with NaT in 'START_TIME' to inspect problematic entries
print(f"Rows with invalid 'START_TIME': {len(data[data['START_TIME'].isna()])}")
print(data[data['START_TIME'].isna()])

# Drop rows where 'START_TIME' could not be converted to datetime
data = data.dropna(subset=['START_TIME'])
print(f"Data after dropping invalid 'START_TIME': {len(data)} rows.")

# Save the cleaned data to a new CSV file
cleaned_file_path = r'C:\Users\ghass\Desktop\telecom-dashboard\backend\cleaned_data.csv'
try:
    data.to_csv(cleaned_file_path, index=False)
    print(f"Cleaned data saved to {cleaned_file_path} with {len(data)} rows.")
except PermissionError as e:
    print(f"Permission denied error: {e}. Trying alternative path.")
    # Try saving to an alternative path
    alternative_path = r'C:\Users\ghass\Desktop\telecom-dashboard\backend\cleaned_data_alt.csv'
    try:
        data.to_csv(alternative_path, index=False)
        print(f"Cleaned data saved to {alternative_path} with {len(data)} rows.")
    except Exception as e:
        print(f"Error saving cleaned data to alternative path: {e}")
