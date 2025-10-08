import os
import sys
import streamlit as st
from yt_downloader import check_ffmpeg, download_video

# Ensure script can find yt_downloader.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.title("🎬 Fun with Vibe Coding - YouTube Downloader")

# Check FFmpeg
if not check_ffmpeg():
    st.error("⚠️ FFmpeg not found in PATH. Please install it and restart the app.")
    st.stop()

# Input fields
url = st.text_input("Enter YouTube URL")
mode = st.selectbox("Select download mode", ["Video", "Audio only"])
quality = st.selectbox("Select quality (for video only)", ["best", "720p", "480p", "360p"])

if st.button("Download"):
    if not url.strip():
        st.warning("Please enter a valid YouTube URL.")
    else:
        st.info("⏳ Downloading... Please wait.")
        success, msg = download_video(url, mode, quality)
        if success:
            st.success(f"✅ {msg}")
        else:
            st.error(f"❌ {msg}")
