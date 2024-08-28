import requests
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# API Key and symbols
api_key = 'WZHBG3XXRP8IM5VD'
symbols = ['META', 'AAPL', 'MSFT', 'AMZN', 'GOOGL']
all_overview_data = []

# Function to fetch data from a given API endpoint
def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        if "Error Message" in data or "Note" in data: 
            print(f"Error fetching data: {data.get('Error Message', data.get('Note'))}")
            return None
        return data
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Fetch data for each symbol
for symbol in symbols:
    overview_url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}'
    overview_data = fetch_data(overview_url)
    if overview_data:
        all_overview_data.append(overview_data)

# Convert the collected data to a pandas DataFrame
df = pd.DataFrame(all_overview_data)

# Aiven MySQL connection details
db_config = {
    'user': 'avnadmin',
    'password': 'AVNS_eTYy8GEwyO7dZHa-CFs',
    'host': 'mysql-104f94f-mamaa-05.h.aivencloud.com',
    'port': 17567,
    'database': 'mamaa'
}

# Path to the CA certificate
ca_cert_path = 'D:/Projects/ETL/ca.pem'  # Adjust this path to where your CA cert is stored

# Create SQLAlchemy engine to connect to Aiven MySQL Database with SSL
connection_string = (
    f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@"
    f"{db_config['host']}:{db_config['port']}/{db_config['database']}?"
    f"ssl_verify_cert=true&ssl_ca={ca_cert_path}"
)
engine = create_engine(connection_string)

# Prepare the SQL UPSERT query
insert_query = """
    INSERT INTO company_data ({columns}) VALUES ({values})
    ON DUPLICATE KEY UPDATE {updates}
"""

# Define the columns and values for your DataFrame
columns = ', '.join(df.columns)
values = ', '.join(['%s'] * len(df.columns))
updates = ', '.join([f"{col} = VALUES({col})" for col in df.columns])

# Prepare the final query
final_query = insert_query.format(columns=columns, values=values, updates=updates)

# Convert DataFrame to list of tuples
data_tuples = [tuple(row) for row in df.to_numpy()]

# Insert or update data in the database
conn = engine.raw_connection()
try:
    cursor = conn.cursor()
    cursor.executemany(final_query, data_tuples)
    conn.commit()
    print("Data upserted successfully.")
except Exception as e:
    print(f"Failed to upsert data into MySQL table: {e}")
finally:
    cursor.close()
    conn.close()
