import os
import requests
import pandas as pd
from sqlalchemy import create_engine, text

# API Key and symbols
api_key = os.getenv('API_KEY_daily_data')
symbols = ['META', 'AAPL', 'MSFT', 'AMZN', 'GOOGL']

# Initialize lists to store all the JSON data
all_daily_data = []

# Function to fetch data from a given API endpoint
def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        if "Error Message" in data or "Note" in data:  # Check for API error messages
            print(f"Error fetching data: {data.get('Error Message', data.get('Note'))}")
            return None
        return data
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Loop through each symbol and fetch the required data
for symbol in symbols:
    daily_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={api_key}'
    daily_data = fetch_data(daily_url)
    if daily_data:
        all_daily_data.append(daily_data)

# Convert JSON data to DataFrame
def json_to_dataframe(data_list, key, symbol_key):
    frames = []
    for data in data_list:
        try:
            meta_data = data['Meta Data']
            symbol = meta_data[symbol_key]
            time_series = data[key]

            # Convert the time series to a DataFrame
            df = pd.DataFrame(time_series).transpose().reset_index()
            df = df.rename(columns={'index': 'date'})
            df['symbol'] = symbol  # Add symbol column

            frames.append(df)
        except KeyError as e:
            print(f"KeyError: {e} in data: {data}")
            continue

    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

# Convert and process daily data
daily_df = json_to_dataframe(all_daily_data, 'Time Series (Daily)', '2. Symbol')

def clean_transform(df, date_col='date'):
    df = df.reset_index(drop=True)
    df[date_col] = pd.to_datetime(df[date_col])  # Convert date columns to datetime

    for col in df.columns:
        if col not in [date_col, 'symbol']:
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert numerical columns
    
    # Rename columns to match your database schema
    df = df.rename(columns={
        'index': 'date',
        '1. open': 'open',
        '2. high': 'high',
        '3. low': 'low',
        '4. close': 'close',
        '5. volume': 'volume'
    })

    df = df.drop_duplicates()
    return df

daily_df = clean_transform(daily_df)

# Database configuration
db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME')
}
ca_cert_path = os.getenv('CA_CERT_PATH')

# Create SQLAlchemy engine to connect to Aiven MySQL Database with SSL
connection_string = (
    f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@"
    f"{db_config['host']}:{db_config['port']}/{db_config['database']}?"
    f"ssl_verify_cert=true&ssl_ca={ca_cert_path}"
)
engine = create_engine(connection_string)

# Truncate the table and insert data
try:
    with engine.connect() as connection:
        # Truncate the table
        connection.execute(text("TRUNCATE TABLE daily_data"))
        
        # Insert the DataFrame into the table
        daily_df.to_sql('daily_data', con=engine, if_exists='append', index=False)
        print("Data successfully inserted into the daily_data table.")
except Exception as e:
    print(f"Failed to truncate and insert data into MySQL table: {e}")