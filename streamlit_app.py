import streamlit as st
import streamlit.components.v1 as components
import requests
import yt_dlp as ytdl
import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

# Load environment variables and setup Jinja2
load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
env = Environment(loader=FileSystemLoader('templates'))

# Set page config
st.set_page_config(
    page_title="Xen Music",
    page_icon="🎵",
    layout="wide"
)

def render_template(template_name, **kwargs):
    template = env.get_template(template_name)
    return template.render(**kwargs)

# Render the main page using your original HTML
main_html = render_template('index.html', request={})
components.html(main_html, height=1000, scrolling=True)

# Handle search in Streamlit but render results using your HTML template
query = st.text_input("Search for songs...", key="search_input")

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
        
        results = []
        for item in data.get('items', []):
            if item['id']['kind'] == 'youtube#video':
                results.append({
                    'id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'thumbnail': item['snippet']['thumbnails']['high']['url'],
                    'author': item['snippet']['channelTitle']
                })
        
        # Render results using your original HTML template
        results_html = render_template('_results.html', results=results)
        components.html(results_html, height=600, scrolling=True)

    except Exception as e:
        st.error(f"Search failed: {str(e)}")