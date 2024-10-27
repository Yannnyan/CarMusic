""" Defines environment variables for scripting """
import os

os.environ.setdefault('YOUTUBE_STREAM_AUDIO', "140")
os.environ.setdefault('DOWNLOAD_DESTINATION', r'E:\mp3')
os.environ.setdefault('CONVERT_SCRIPT_PATH',
                      r'~\Desktop\Music\Download-Music\convert_mp4_to_mp3.ps1')
os.environ.setdefault("ENCODING", "utf_8")
os.environ.setdefault("ENCRYPTION_ALGO", "sha256")

YOUTUBE_STREAM_AUDIO = os.environ.get("YOUTUBE_STREAM_AUDIO")
DOWNLOAD_DESTINATION = os.environ.get("DOWNLOAD_DESTINATION")
CONVERT_SCRIPT_PATH  = os.environ.get("CONVERT_SCRIPT_PATH")
