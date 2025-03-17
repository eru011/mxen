import streamlit as st
from main import app
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import yt_dlp as ytdl

# Set page config
st.set_page_config(
    page_title="Xen Music",
    page_icon="🎵",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Create Streamlit UI
st.title("Xen Music")

query = st.text_input("Search for songs...")

if query:
    # Use your existing search logic here
    try:
        # Implement the search functionality directly in Streamlit
        # (Copy relevant parts from your main.py search function)
        st.write("Searching for:", query)
        # Display results...

    except Exception as e:
        st.error(f"Search failed: {str(e)}")