import streamlit as st
import streamlit.components.v1 as components
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# Set page config (only once)
st.set_page_config(
    page_title="Xen Music",
    page_icon="🎵",
    layout="wide"
)

# Create Streamlit UI
st.title("Xen Music")

# Create search interface
query = st.text_input("Search for songs...")

if query:
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet,id",
            "q": query,
            "type": "video",
            "maxResults": 10,
            "key": YOUTUBE_API_KEY
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Display results in a grid
        cols = st.columns(3)
        for idx, item in enumerate(data.get('items', [])):
            if item['id']['kind'] == 'youtube#video':
                with cols[idx % 3]:
                    st.image(item['snippet']['thumbnails']['high']['url'])
                    st.write(item['snippet']['title'])
                    st.write(item['snippet']['channelTitle'])
                    video_id = item['id']['videoId']
                    if st.button(f"Play", key=video_id):
                        st.video(f"https://www.youtube.com/watch?v={video_id}")

    except Exception as e:
        st.error(f"Search failed: {str(e)}")