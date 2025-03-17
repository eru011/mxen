import streamlit as st
import streamlit.components.v1 as components
import requests
import os
import yt_dlp
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def download_audio(video_id):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'temp_%(id)s.%(ext)s'
    }
    
    url = f"https://www.youtube.com/watch?v={video_id}"
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        return f"temp_{video_id}.mp3"

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
                    if st.button(f"Download MP3", key=video_id):
                        with st.spinner('Downloading...'):
                            file_path = download_audio(video_id)
                            with open(file_path, "rb") as f:
                                bytes_data = f.read()
                                st.download_button(
                                    label="Download",
                                    data=bytes_data,
                                    file_name=f"{item['snippet']['title']}.mp3",
                                    mime="audio/mpeg"
                                )
                            # Clean up temp file
                            os.remove(file_path)

    except Exception as e:
        st.error(f"Search failed: {str(e)}")