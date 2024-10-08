# MAMAA Financial Performance

## Overview

The **MAMAA Financial Performance** project provides comprehensive insights into the financial performance and trends of major tech companies known as MAMAA: Microsoft, Apple, Meta, Amazon, and Alphabet. This web app delivers detailed analysis and visualizations to aid in making informed investment decisions by integrating data scraping, financial analytics, and advanced machine learning techniques.

Explore the live application here: [MAMAA Financial Performance Web App](https://mamaa-financial-performance.streamlit.app/)

## Main Objectives

- **Financial Insights**: Explore detailed analyses and visualizations of MAMAA companies' financial performance.
- **Predictive Analytics**: Utilize advanced machine learning models, including LSTM networks, to forecast future stock prices.
- **Data Collection and Storage**: Collect and store data from reliable sources in a cloud database for in-depth analysis.
- **Interactive Experience**: Provide a seamless and interactive user experience using Streamlit.

## Technical Details

### Machine Learning Models

- **LSTM Networks**:
  - **Architecture**: Long Short-Term Memory (LSTM) networks are a type of Recurrent Neural Network (RNN) designed for time series forecasting, effectively capturing long-term dependencies in sequential data.
  - **Training Data**: Historical stock price data, including sequences of closing prices, is preprocessed (normalized and split) to train the LSTM model.
  - **Prediction**: The trained LSTM model predicts future stock prices based on recent data, with predictions visualized within the app.

### Data Sources

- **Stock Data**: Collected via the Alpha Vantage API and stored in a cloud database on Avien.
- **News Scraping**: Yahoo Finance is used for scraping news, with sentiment analysis performed to assess market sentiment.
- **Custom Calculations**:
  - **Price Momentum**: Measures the percentage change in closing price.
  - **Volatility Score**: Calculates the range between high and low prices as a percentage of the closing price.
  - **Volume Score**: Compares current trading volume to the 50-day average volume.
  - **EMA vs SMA Score**: Compares Exponential Moving Average (EMA) to Simple Moving Average (SMA).
  - **RSI Score**: Measures the speed and change of price movements with the Relative Strength Index (RSI).
  - **Overall Investment Score**: A composite score combining various metrics to indicate investment quality.

### Data Update and Insights

- **ETL Process**: Data is updated daily using ETL processes and cron jobs to ensure the most recent information is available for analysis.

## Repository Structure

The repository is organized into several key directories:

- **`web_app/`**: Contains the Streamlit application code and models.
  - `.streamlit/`: Configuration for Streamlit.
  - `__pycache__/`: Compiled Python files.
  - `app.py`: Main script to run the Streamlit app.
  - `create_lstm_model.py`: Script for creating LSTM models.
  - `Financial_Scores.py`: Contains functions for calculating financial scores.
  - `Home.py`: Home page script for the app.
  - `News_Sentiment.py`: Script for news scraping and sentiment analysis.
  - `Overview.py`: Script for the app's overview page.
  - `requirements.txt`: List of Python dependencies.
  - `utils.py`: Utility functions for the app.
  - Model files (`AAPL_lstm_model.h5`, `AMZN_lstm_model.h5`, etc.): Pretrained LSTM models.

- **`ETL/`**: Contains scripts and documentation for the ETL process.
  - `ETL PROCESS.txt`: Documentation for the ETL process.
  - `ETL Script.ipynb`: Jupyter notebook for ETL scripting.

- **`Database/`**: Contains database-related files.
  - `EER Diagram.mwb`: EER diagram file.
  - `ER.png`: ER diagram image.
  - `table_creation.sql`: SQL script for table creation.

- **`scheduled_update_database/`**: Contains scripts for updating the database.
  - `company_data.py`: Script for managing company data.
  - `daily_data.py`: Script for managing daily data.
  - `technical_indicators.py`: Script for calculating technical indicators.

## Deployment

- **Platform**: The application is deployed on Streamlit Cloud.
- **Scaling and Performance**: For better scaling and performance, deploying on Google Cloud Platform (GCP) is recommended.
- **Configuration**: Ensure the environment is configured with all necessary dependencies and API keys.

## Dependencies

The project uses the following major libraries:

- `streamlit`
- `streamlit-option-menu`
- `pandas`
- `sqlalchemy`
- `plotly`
- `vadersentiment`
- `beautifulsoup4`
- `urllib3`
- `mysql-connector-python`
- `numpy`
- `keras`
- `tensorflow`
- `scikit-learn`

## License and Credits

This project was developed independently. Contributions to enhance features are welcome. For more information on licensing, please refer to the [LICENSE](LICENSE) file in this repository.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. Your suggestions and improvements are highly valued!

## Contact

For any questions or feedback, feel free to reach out via:

- **Email**: [jhasantanu9@gmail.com](mailto:jhasantanu9@gmail.com)
- **LinkedIn**: [Santanu Jha](https://www.linkedin.com/in/santanu-jha-845510292/)
- **GitHub**: [jhasantanu9](https://github.com/jhasantanu9)
- **Portfolio**: [santanujha.netlify.app](https://santanujha.netlify.app)
