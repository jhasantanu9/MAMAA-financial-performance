import streamlit as st
from streamlit_option_menu import option_menu
import os

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
        .app-description {
            text-align: left;
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
        .btn-repo {
            background-color: #6c757d;
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
            <p>The MAMAA Financial Insights app is designed to provide a deep dive into the financial health of major tech giants. The app regularly collects data from a reliable API, stores it in a robust database, and uses this data to perform detailed analyses. By leveraging techniques in data scraping, database management, and financial analytics, including advanced machine learning with LSTM networks for predicting stock closing prices, the app delivers up-to-date insights crucial for making informed investment choices.</p>
            <p>This app is powered by Streamlit, enabling a seamless and interactive user experience. It combines the power of Python, SQL, and API handling to bring you comprehensive financial insights at your fingertips.</p>
        </div>
        
        <div class="contact-container">
                <a href="https://github.com/jhasantanu9/MAMAA-financial-performance/tree/main" target="_blank"  class="btn btn-repo">View the GitHub Repository</a>
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
