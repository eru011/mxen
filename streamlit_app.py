import streamlit as st
import requests
import yt_dlp as ytdl
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

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
    .stButton button {
        background-color: #1DB954;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Create Streamlit UI
st.title("Xen Music")

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
        
        for item in data.get('items', []):
            if item['id']['kind'] == 'youtube#video':
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.image(item['snippet']['thumbnails']['high']['url'])
                
                with col2:
                    st.subheader(item['snippet']['title'])
                    st.write(item['snippet']['channelTitle'])
                    
                    video_id = item['id']['videoId']
                    if st.button(f"Play {item['snippet']['title']}", key=f"play_{video_id}"):
                        try:
                            video_url = f"https://www.youtube.com/watch?v={video_id}"
                            with ytdl.YoutubeDL({
                                'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio',
                                'quiet': True,
                                'no_warnings': True,
                                'extract_audio': True
                            }) as ydl:
                                info = ydl.extract_info(video_url, download=False)
                                formats = info.get('formats', [])
                                audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
                                best_audio = max(audio_formats, key=lambda x: float(x.get('abr', 0) or 0))
                                audio_url = best_audio['url']
                                st.audio(audio_url)
                        except Exception as e:
                            st.error(f"Failed to play audio: {str(e)}")
                
                st.divider()

    except Exception as e:
        st.error(f"Search failed: {str(e)}")