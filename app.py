import streamlit as st
from yt_downloader import check_ffmpeg, download_video

st.title("🎬 ~ Fun Vibes YT Downloader ~ 🍿")

if not check_ffmpeg():
    st.error("❌ FFmpeg is not installed or not added to PATH. Please install it before continuing.")
else:
    st.success("✅ FFmpeg detected successfully!")

# UI elements
download_type = st.selectbox("Select Download Type:", ["Single Video", "Playlist"])
url = st.text_input("Enter YouTube URL:")
mode = st.selectbox("Select Format:", ["Audio (.mp3)", "Video only", "Merged (audio + video)"])
quality = st.selectbox("Select Quality:", ["Best Quality", "1080p", "720p"])

if st.button("Download"):
    if url.strip() == "":
        st.warning("Please enter a valid YouTube URL.")
    else:
        with st.spinner("Downloading... Please wait."):
            try:
                download_video(url, mode, quality)
                st.success("✅ Download completed! Check your Downloads folder.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
