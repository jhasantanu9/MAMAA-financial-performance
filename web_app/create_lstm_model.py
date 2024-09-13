# Creating and saving LSTM model for each companies 

from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

# Get the database credentials from Streamlit secrets
db_config = st.secrets["connections"]["mysql"]

# Create SQLAlchemy engine to connect to the MySQL Database
connection_string = (
    f"{db_config['dialect']}+mysqlconnector://{db_config['username']}:{db_config['password']}@"
    f"{db_config['host']}:{db_config['port']}/{db_config['database']}?"
    f"charset={db_config['query']['charset']}"
)

# Create the SQLAlchemy engine
engine = create_engine(connection_string)

@st.cache
# Function to fetch data from the database
def fetch_data():
    companies_query = 'SELECT * FROM company_data'
    daily_data_query = 'SELECT * FROM daily_data'
    technical_indicator_query = 'SELECT * FROM technical_indicators'
    
    # Execute queries and load data into DataFrames
    with engine.connect() as connection:
        companies_df = pd.read_sql(companies_query, connection)
        daily_df = pd.read_sql(daily_data_query, connection)
        technical_indicator_df = pd.read_sql(technical_indicator_query, connection)
    
    return companies_df, daily_df, technical_indicator_df

# Fetch the latest data from the database
companies_df, daily_df, technical_indicator_df = fetch_data()

# Merge datasets 
merged_df = pd.merge(daily_df, companies_df, on='symbol', how='inner')
merged_df = pd.merge(merged_df, technical_indicator_df, on=['symbol', 'date'], how='inner')

# Selecting relevant columns for the model
final_data = merged_df[['date', 'symbol', 'high', 'low', 'close', 'volume', 'sma', 'ema', 'rsi']]

def create_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_and_save_model(symbol, data):
    # Preprocess data for the company
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data[['close']].values)

    # Create dataset
    time_step = 60
    X, y = create_dataset(scaled_data, time_step)
    X = X.reshape(X.shape[0], X.shape[1], 1)

    # Create and train the model
    model = create_lstm_model((X.shape[1], 1))
    model.fit(X, y, epochs=20, batch_size=64, verbose=1)

    # Save the model
    model.save(f'{symbol}_lstm_model.h5')
    print(f'Model for {symbol} saved successfully!')

def create_dataset(data, time_step=60):
    X, y = [], []
    for i in range(len(data) - time_step):
        X.append(data[i:(i + time_step), 0])
        y.append(data[i + time_step, 0])
    return np.array(X), np.array(y)

symbols = ['AAPL', 'AMZN', 'GOOGL', 'META', 'MSFT']
for symbol in symbols:
    company_data = final_data[final_data['symbol'] == symbol]
    train_and_save_model(symbol, company_data)
