import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from utils import footer
from sqlalchemy import create_engine


# Set page configuration
st.set_page_config(
    page_title="MAMAA Companies Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded"
)

selected = option_menu(
    None, ["Home", "Overview", "News & Sentiment", "Financial Scores"], 
    icons=["house", "bar-chart", "newspaper", "clipboard-data"], 
    orientation="horizontal"
)

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

# Merge datasets if needed
merged_df = pd.merge(daily_df, companies_df, on='symbol', how='inner')
merged_df = pd.merge(merged_df, technical_indicator_df, on=['symbol', 'date'], how='inner')

# Load the selected page
if selected == "Home":
    import Home
    Home.main()

elif selected == "Overview":
    import Overview
    Overview.main(companies_df, daily_df)

elif selected == "News & Sentiment":
    import News_Sentiment
    News_Sentiment.main()

elif selected == "Financial Scores":
    import Financial_Scores
    Financial_Scores.main(merged_df)

footer()