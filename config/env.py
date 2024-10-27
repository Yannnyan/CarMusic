""" Defines environment variables for scripting """
import os

def set_environment():
    """ Set the environment variables """
    if os.environ.get('Environment') == "Dev":
        os.environ.setdefault('YOUTUBE_STREAM_AUDIO', "140")
        os.environ.setdefault('DOWNLOAD_DESTINATION', r'E:\mp3')
        os.environ.setdefault('CONVERT_SCRIPT_PATH',
                            r'~\Desktop\Music\Download-Music\convert_mp4_to_mp3.ps1')
        os.environ.setdefault("ENCODING", "utf_8")
        os.environ.setdefault("ENCRYPTION_ALGO", "sha256")
    else:
        os.environ.setdefault('YOUTUBE_STREAM_AUDIO', "140")
        os.environ.setdefault('DOWNLOAD_DESTINATION', r'E:\mp3')
        os.environ.setdefault('CONVERT_SCRIPT_PATH',
                            r'~\Desktop\Music\Download-Music\convert_mp4_to_mp3.ps1')
        os.environ.setdefault("ENCODING", "utf_8")
        os.environ.setdefault("ENCRYPTION_ALGO", "sha256")
