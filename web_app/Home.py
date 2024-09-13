import streamlit as st
from streamlit_option_menu import option_menu
import os

import streamlit as st

@st.cache_data
def main():
    # Custom CSS for layout and styling
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .welcome-text {
            text-align: center;
            margin-top: 3rem;
        }
        .contact-container {
            text-align: center;
            margin-top: 3rem;
        }
        .social-links a {
            display: inline-block;
            margin: 0 10px;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            color: white;
            font-weight: bold;
        }
        .btn-primary {
            background-color: #007bff;
        }
        .btn-linkedin {
            background-color: #0077b5;
        }
        .btn-github {
            background-color: #24292e;
        }
        .btn-portfolio {
            background-color: #17a2b8;
        }
        .protection-container {
            text-align: center;
            margin-top: 3rem;
        }
        .protection-text {
            font-size: 16px;
            line-height: 1.6;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class="welcome-text">
            <h1>WELCOME ABOARD</h1>
            <p>Discover comprehensive insights into the financial performance and trends of MAMAA companies: Microsoft, Apple, Meta, Amazon, and Alphabet. This web app offers detailed analysis and visualizations to help you make informed investment decisions.</p>
        </div>
        <hr>        
     
        <br>  
        <div class="app-description">
            <p>The MAMAA Financial Insights app is designed to provide a deep dive into the financial health of major tech giants. The app regularly collects data from a reliable API, stores it in a robust database, and uses this data to perform detailed analyses. By leveraging techniques in data scraping, database management, and financial analytics, the app delivers up-to-date insights that are crucial for making informed investment choices.</p>
            <p>This app is powered by Streamlit, enabling a seamless and interactive user experience. It combines the power of Python, SQL, and API handling to bring you comprehensive financial insights at your fingertips.</p>
        </div>
        
        <div class="protection-container">
            <h4>About LSTM Stock Price Prediction</h4>
            <div class="protection-text">
                <p>Our app employs advanced machine learning techniques to predict stock prices using Long Short-Term Memory (LSTM) networks. Here's an overview of how this technology works and contributes to our app:</p>
                <ul>
                    <li><strong>LSTM Networks:</strong> LSTMs are a type of Recurrent Neural Network (RNN) that are particularly well-suited for time series forecasting due to their ability to remember long-term dependencies in data.</li>
                    <li><strong>Data Processing:</strong> Historical stock price data is preprocessed and used to train the LSTM model. This involves normalizing the data, creating sequences, and splitting it into training and testing sets.</li>
                    <li><strong>Model Training:</strong> The LSTM model is trained on historical data to learn patterns and trends in stock prices. This training process involves optimizing the model parameters to minimize prediction errors.</li>
                    <li><strong>Prediction and Visualization:</strong> Once trained, the LSTM model can predict future stock prices based on recent data. These predictions are then visualized in the app to help users make informed decisions.</li>
                </ul>
                <p>By leveraging LSTM networks, our app provides valuable insights into potential future stock price movements, enhancing your investment strategy with cutting-edge machine learning technology.</p>
            </div>
        </div>
        
        <div class="contact-container">
            <h4 style="text-align: center;">Get in Touch</h4>
            <div class="social-links">
                <a href="mailto:jhasantanu9@gmail.com" class="btn btn-primary">Email</a>
                <a href="https://www.linkedin.com/in/santanu-jha-845510292/" target="_blank" class="btn btn-linkedin">LinkedIn</a>
                <a href="https://github.com/jhasantanu9" target="_blank" class="btn btn-github">GitHub</a>
                <a href="https://santanujha.netlify.app" target="_blank" class="btn btn-portfolio">Portfolio</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
