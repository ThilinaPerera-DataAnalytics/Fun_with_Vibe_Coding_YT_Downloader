import os
import subprocess
import yt_dlp

def check_ffmpeg():
    """Check if FFmpeg is installed and accessible."""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False


def get_download_path():
    """Return the default Windows Downloads folder."""
    return os.path.join(os.path.expanduser("~"), "Downloads")


def download_video(url, mode="Video", quality="best"):
    """Download a YouTube video or audio."""
    try:
        download_path = get_download_path()

        if mode == "Audio only":
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(download_path, "%(title)s.%(ext)s"),
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "noplaylist": True,
                "quiet": True,
                "merge_output_format": None
            }
        else:
            # Map quality string to format
            format_map = {
                "best": "bestvideo+bestaudio/best",
                "720p": "bestvideo[height<=720]+bestaudio/best",
                "480p": "bestvideo[height<=480]+bestaudio/best",
                "360p": "bestvideo[height<=360]+bestaudio/best"
            }
            ydl_opts = {
                "format": format_map.get(quality, "bestvideo+bestaudio/best"),
                "outtmpl": os.path.join(download_path, "%(title)s.%(ext)s"),
                "merge_output_format": "mp4",
                "noplaylist": True,
                "quiet": True,
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if mode == "Audio only":
            return True, f"Audio downloaded successfully to {download_path}"
        else:
            return True, f"Video downloaded successfully to {download_path}"

    except yt_dlp.utils.DownloadError as e:
        return False, f"Download error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"
