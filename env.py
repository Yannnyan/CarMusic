import os

os.environ.setdefault('YOUTUBE_STREAM_AUDIO', "140")
os.environ['DOWNLOAD_DESTINATION'] = os.environ.get('DOWNLOAD_DESTINATION', r'E:\mp3')
os.environ.setdefault('CONVERT_SCRIPT_PATH', r'C:\Users\Yan\Desktop\Music\Download-Music\convert_mp4_to_mp3.ps1')

YOUTUBE_STREAM_AUDIO = os.environ.get("YOUTUBE_STREAM_AUDIO")
DOWNLOAD_DESTINATION = os.environ.get("DOWNLOAD_DESTINATION")
CONVERT_SCRIPT_PATH  = os.environ.get("CONVERT_SCRIPT_PATH")

shared_progress = 0
shared_continue_executing = True