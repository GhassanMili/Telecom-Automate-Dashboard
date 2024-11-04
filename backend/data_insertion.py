import cx_Oracle
import pandas as pd

# Oracle database connection details
dsn = cx_Oracle.makedsn("localhost", "1521", service_name="orcl")
try:
    connection = cx_Oracle.connect(user="ra@2024", password="Naders123", dsn=dsn, mode=cx_Oracle.SYSDBA)
    cursor = connection.cursor()
    print("Database connection successful.")
except cx_Oracle.DatabaseError as e:
    error, = e.args
    print(f"Database connection failed: {error.message}")
    exit(1)

# Load the cleaned CSV file
cleaned_file_path = r'C:\Users\ghass\Desktop\telecom-dashboard\backend\cleaned_data.csv'
try:
    data = pd.read_csv(cleaned_file_path)
    print(f"Loaded data from {cleaned_file_path}.")
except FileNotFoundError:
    print(f"File not found: {cleaned_file_path}")
    exit(1)
except pd.errors.EmptyDataError:
    print("No data: Empty CSV file.")
    exit(1)
except Exception as e:
    print(f"Error loading CSV file: {e}")
    exit(1)

# Convert date columns to datetime if they are not already
try:
    data['START_TIME'] = pd.to_datetime(data['START_TIME'])
    data['ORIG_START_TIME'] = pd.to_datetime(data['ORIG_START_TIME'])
except Exception as e:
    print(f"Error converting date columns: {e}")
    exit(1)

# Insert data into the database
for index, row in data.iterrows():
    try:
        NE = row['NE']
        FILENAME = row['FILENAME']
        A_MSISDN = row['A_MSISDN']
        B_MSISDN = row['B_MSISDN']
        START_TIME = row['START_TIME']
        PROC_HOUR = row['PROC_HOUR']
        EVENT_TYPE = row['EVENT_TYPE']
        EVENT_TYPE_ORIG = row['EVENT_TYPE_ORIG']
        CALL_TYPE = row['CALL_TYPE']
        EVENT_STATUS = row['EVENT_STATUS']
        FILTER_CODE = row['FILTER_CODE']
        SUBSCRIBER_TYPE = row['SUBSCRIBER_TYPE']
        TRAFFIC_TYPE = row['TRAFFIC_TYPE']
        SERVICE_TYPE = row['SERVICE_TYPE']
        TEST_FLAG = row['TEST_FLAG']
        CHARGE_AMOUNT_ORIG = row['CHARGE_AMOUNT_ORIG']
        PRICE_PLAN_CODE = row['PRICE_PLAN_CODE']
        ORIG_START_TIME = row['ORIG_START_TIME']
        RECORD_TYPE = row['RECORD_TYPE']
        C_NUM = row['C_NUM']
        PARTIAL_SEQ_ID = row['PARTIAL_SEQ_ID']
        LAST_PARTIAL = row['LAST_PARTIAL']

        cursor.execute("""
            INSERT INTO RA_MMG_ASN_CDR_DET (
                NE, FILENAME, A_MSISDN, B_MSISDN, START_TIME, PROC_HOUR, EVENT_TYPE, EVENT_TYPE_ORIG,
                CALL_TYPE, EVENT_STATUS, FILTER_CODE, SUBSCRIBER_TYPE, TRAFFIC_TYPE, SERVICE_TYPE,
                TEST_FLAG, CHARGE_AMOUNT_ORIG, PRICE_PLAN_CODE, ORIG_START_TIME, RECORD_TYPE, C_NUM, PARTIAL_SEQ_ID, LAST_PARTIAL
            ) VALUES (
                :1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, :19, :20, :21, :22
            )
        """, (NE, FILENAME, A_MSISDN, B_MSISDN, START_TIME, PROC_HOUR, EVENT_TYPE, EVENT_TYPE_ORIG,
              CALL_TYPE, EVENT_STATUS, FILTER_CODE, SUBSCRIBER_TYPE, TRAFFIC_TYPE, SERVICE_TYPE,
              TEST_FLAG, CHARGE_AMOUNT_ORIG, PRICE_PLAN_CODE, ORIG_START_TIME, RECORD_TYPE, C_NUM, PARTIAL_SEQ_ID, LAST_PARTIAL))
        print(f"Inserted row {index + 1}/{len(data)}")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Failed to insert row {index + 1}: {error.message}")
        continue  # Skip to the next row

try:
    connection.commit()
    print("Data insertion completed successfully.")
except cx_Oracle.DatabaseError as e:
    error, = e.args
    print(f"Failed to commit changes: {error.message}")
finally:
    cursor.close()
    connection.close()
    print("Database connection closed.")
