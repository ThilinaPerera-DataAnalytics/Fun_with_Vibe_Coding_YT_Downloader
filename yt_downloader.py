import os
import platform
import subprocess
from pathlib import Path
import yt_dlp


def get_download_path():
    """Return the default Downloads folder for Windows."""
    if platform.system() == "Windows":
        return Path(os.path.expanduser("~/Downloads"))
    else:
        return Path.home() / "Downloads"


def check_ffmpeg():
    """Verify that ffmpeg is installed and accessible."""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False


def download_video(url, mode, quality):
    """Download YouTube content based on user selections."""
    download_path = get_download_path()

    # Map Streamlit quality options to yt-dlp formats
    quality_map = {
        "Best Quality": "bestvideo+bestaudio/best",
        "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]"
    }
    format_code = quality_map.get(quality, "best")

    ydl_opts = {
        "outtmpl": str(download_path / "%(title)s.%(ext)s"),
        "noplaylist": False,
        "quiet": False,
        "merge_output_format": "mp4",
    }

    # Adjust download mode
    if mode == "Audio (.mp3)":
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })
    elif mode == "Video only":
        ydl_opts["format"] = format_code.split("+")[0]
    elif mode == "Merged (audio + video)":
        ydl_opts["format"] = format_code
        ydl_opts["merge_output_format"] = "mp4"

    # Perform download
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except yt_dlp.utils.DownloadError as e:
        print("❌ Download error:", e)
        if "Encoder not found" in str(e):
            print("⚠️ Retrying using M4A format (no external MP3 encoder needed)...")
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
            }]
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])


if __name__ == "__main__":
    print("YT Downloader module ready.")
