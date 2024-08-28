import os
import requests
import pandas as pd
from sqlalchemy import create_engine, text

# API Key and symbols
api_key = os.getenv('API_KEY_technical_indicators')
symbols = ['META', 'AAPL', 'MSFT', 'AMZN', 'GOOGL']

# Initialize lists to store all the JSON data
all_sma_data = []
all_ema_data = []
all_rsi_data = []

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

# Loop through each symbol and fetch the required data
for symbol in symbols:
    # Fetch SMA data
    sma_url = f'https://www.alphavantage.co/query?function=SMA&symbol={symbol}&interval=daily&time_period=10&series_type=close&apikey={api_key}'
    sma_data = fetch_data(sma_url)
    if sma_data:
        all_sma_data.append(sma_data)

    # Fetch EMA data
    ema_url = f'https://www.alphavantage.co/query?function=EMA&symbol={symbol}&interval=daily&time_period=10&series_type=close&apikey={api_key}'
    ema_data = fetch_data(ema_url)
    if ema_data:
        all_ema_data.append(ema_data)

    # Fetch RSI data
    rsi_url = f'https://www.alphavantage.co/query?function=RSI&symbol={symbol}&interval=daily&time_period=14&series_type=close&apikey={api_key}'
    rsi_data = fetch_data(rsi_url)
    if rsi_data:
        all_rsi_data.append(rsi_data)

# Convert JSON data to DataFrame
def json_to_dataframe(data_list, key, symbol_key):
    frames = []
    for data in data_list:
        try:
            meta_data = data['Meta Data']
            symbol = meta_data[symbol_key]
            time_series = data[key]

            df = pd.DataFrame(time_series).transpose().reset_index()
            df = df.rename(columns={'index': 'date'})
            df['symbol'] = symbol
            frames.append(df)
        except KeyError as e:
            print(f"KeyError: {e} in data: {data}")
            continue
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

# Convert and process SMA, EMA, and RSI data
sma_df = json_to_dataframe(all_sma_data, 'Technical Analysis: SMA', '1: Symbol')
ema_df = json_to_dataframe(all_ema_data, 'Technical Analysis: EMA', '1: Symbol')
rsi_df = json_to_dataframe(all_rsi_data, 'Technical Analysis: RSI', '1: Symbol')

# Clean and transform DataFrame
def clean_transform(df, date_col='date'):
    df = df.reset_index(drop=True)
    df[date_col] = pd.to_datetime(df[date_col])
    for col in df.columns:
        if col not in [date_col, 'symbol']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.drop_duplicates()
    return df

sma_df = clean_transform(sma_df)
ema_df = clean_transform(ema_df)
rsi_df = clean_transform(rsi_df)

# Combine all technical indicators into one DataFrame
tech_indicators_df = pd.concat([sma_df, ema_df, rsi_df], axis=1)
tech_indicators_df = tech_indicators_df.loc[:, ~tech_indicators_df.columns.duplicated()]
tech_indicators_df = tech_indicators_df.fillna(0)

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

# Truncate the technical_indicators table before inserting new data
with engine.connect() as connection:
    connection.execute(text("TRUNCATE TABLE technical_indicators"))

# Insert the DataFrame into the technical_indicators table
try:
    tech_indicators_df.to_sql('technical_indicators', con=engine, if_exists='append', index=False)
    print("Data successfully inserted into the technical_indicators table.")
except Exception as e:
    print(f"Failed to insert data into MySQL table: {e}")