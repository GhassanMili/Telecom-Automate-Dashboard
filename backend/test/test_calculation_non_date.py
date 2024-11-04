import pandas as pd
import cx_Oracle
import numpy as np

# Load the necessary data
cleaned_data_path = r'C:\Users\ghass\Desktop\telecom-dashboard\backend\cleaned_data.csv'
price_list_path = r'C:\Users\ghass\Desktop\telecom-dashboard\data\Price List.xlsx'

# Load cleaned data
try:
    cleaned_data = pd.read_csv(cleaned_data_path, parse_dates=['ORIG_START_TIME'])
    print(f"Loaded cleaned data from {cleaned_data_path}.")
    print(f"Cleaned data shape: {cleaned_data.shape}")
except FileNotFoundError:
    print(f"File not found: {cleaned_data_path}")
    exit(1)
except pd.errors.EmptyDataError:
    print("No data: Empty cleaned data CSV file.")
    exit(1)
except Exception as e:
    print(f"Error loading cleaned data CSV file: {e}")
    exit(1)

# Load price list
try:
    price_list = pd.read_excel(price_list_path)
    print(f"Loaded price list from {price_list_path}.")
    print("Price list columns:", price_list.columns)
except FileNotFoundError:
    print(f"File not found: {price_list_path}")
    exit(1)
except pd.errors.EmptyDataError:
    print("No data: Empty Price List Excel file.")
    exit(1)
except ImportError:
    print("Missing optional dependency 'openpyxl'. Use pip or conda to install openpyxl.")
    exit(1)
except Exception as e:
    print(f"Error loading Price List Excel file: {e}")
    exit(1)

# Ensure 'Keyword' and 'Prix unitaire' columns are present in price_list
if 'Keyword' not in price_list.columns or 'Prix unitaire' not in price_list.columns:
    print("Keyword or Prix unitaire column is missing in price_list.")
    exit(1)

# Ensure 'SERVICE_TYPE' column is present in cleaned_data
if 'SERVICE_TYPE' not in cleaned_data.columns:
    print("SERVICE_TYPE column is missing in cleaned_data.")
    exit(1)

# Debug: Print unique values for filtering columns
print("Unique SERVICE_TYPE values:", cleaned_data['SERVICE_TYPE'].unique())
print("Unique EVENT_STATUS values:", cleaned_data['EVENT_STATUS'].unique())
print("Unique EVENT_TYPE values:", cleaned_data['EVENT_TYPE'].unique())

# Oracle database connection details
dsn = cx_Oracle.makedsn("localhost", "1521", service_name="orcl")
connection = cx_Oracle.connect(user="sys", password="Naders123", dsn=dsn, mode=cx_Oracle.SYSDBA)
cursor = connection.cursor()

# Perform the necessary calculations
try:
    # Merge cleaned_data with price_list based on 'SERVICE_TYPE' and 'Keyword'
    merged_data = pd.merge(cleaned_data, price_list, left_on='SERVICE_TYPE', right_on='Keyword', how='left')
    print(f"Merged data shape: {merged_data.shape}")

    # Debug: Check if the merge is correct
    print(f"Merged data preview:\n{merged_data.head()}")

    # Filter data based on EVENT_STATUS and EVENT_TYPE
    filtered_data = merged_data[
        (merged_data['EVENT_STATUS'] == 'Success') & 
        (merged_data['EVENT_TYPE'].isin([74, 75]))
    ]
    print(f"Filtered data shape: {filtered_data.shape}")

    # Debug: Check if the filtering is correct
    print(f"Filtered data preview:\n{filtered_data.head()}")
    print(f"Filtered data EVENT_STATUS values: {filtered_data['EVENT_STATUS'].unique()}")
    print(f"Filtered data EVENT_TYPE values: {filtered_data['EVENT_TYPE'].unique()}")

    # Group by SERVICE_TYPE and calculate total NB_SMS and TOTAL_PRICE
    grouped_data = filtered_data.groupby(['SERVICE_TYPE', 'Prix unitaire']).agg(
        NB_SMS=pd.NamedAgg(column='A_MSISDN', aggfunc='size'),
        TOTAL_PRICE=pd.NamedAgg(column='A_MSISDN', aggfunc='size')
    ).reset_index()

    # Calculate the total price for each service type
    grouped_data['TOTAL_PRICE'] = grouped_data['NB_SMS'] * grouped_data['Prix unitaire']

    print(f"Grouped data shape: {grouped_data.shape}")

    # Debug: Check if the grouping is correct
    print(f"Grouped data preview:\n{grouped_data.head()}")

    # Save the calculated data to a new CSV file
    calculated_data_path = r'C:\Users\ghass\Desktop\telecom-dashboard\frontend\public\calculated_data.csv'
    grouped_data.to_csv(calculated_data_path, index=False)
    print(f"Calculated data saved to {calculated_data_path} with {len(grouped_data)} rows.")
except KeyError as e:
    print(f"Key error: {e}")
except Exception as e:
    print(f"Error during calculation or data insertion: {e}")
finally:
    cursor.close()
    connection.close()
