# utils.py

import streamlit as st

def footer():
    # CSS for layout and styling
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton button {
            background-color: #007bff;
            color: white;
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
        }
        .stButton button:hover {
            background-color: #0056b3;
            color: white;
        }
        .footer {
            background-color: #2e3b4e;
            color: white;
            text-align: center;
            padding: 20px;
            border-radius: 10px;
            margin-top: 3rem;
        }
        .footer a {
            color: #007bff;
            text-decoration: none;
        }
        .welcome-text {
            text-align: center;
            margin-top: 3rem;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Footer HTML
    st.markdown("""
        <div class="footer">
            <p>© 2024 MAMAA Companies Dashboard @Santanu Jha</p>
        </div>
        """, unsafe_allow_html=True)
