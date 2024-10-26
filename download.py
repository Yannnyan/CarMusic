
from pytubefix import Playlist, exceptions
from Database.database import Cardb
import subprocess, sys
from env import *
import threading
import socket

class DownloadThread(threading.Thread):
    def __init__(self, l_playlist_urls, downloads_path, server_port: int):
        threading.Thread.__init__(self,daemon=True)
        self.l_playlist_urls = l_playlist_urls
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect(('127.0.0.1',server_port))
        self.stop = False

        self.DOWNLOAD_DESTINATION = downloads_path

    def _send(self, format_message: str):
        self.connection.send(format_message.encode("utf-8"))

    def run(self):
        database = Cardb()
        for s_playlist_url in self.l_playlist_urls:
            playlist = Playlist(s_playlist_url)
            self._send("Videos Count: " + str(len(playlist.video_urls)) + "\n")
            for video in playlist.videos:
                if self.stop == True:
                    self.halt()
                self._send('Author: {0:40}   Title: {1}\n'.format(video.author, video.title))
                try:
                    audio_stream = video.streams.get_audio_only("mp4")
                    if not database.check_song_exist(video):
                            audio_stream.download(self.DOWNLOAD_DESTINATION)
                            database.insert_song(video,video.watch_url, True)
                except(exceptions.LiveStreamError, exceptions.VideoUnavailable, exceptions.VideoPrivate, exceptions.VideoRegionBlocked, exceptions.UnknownVideoError,exceptions.AgeRestrictedError, AttributeError):
                    continue
    
    def halt(self):
        exit(0)

    def convert_to_mp3(self):
        # Convert mp4 files to mp3 format
        p = subprocess.Popen(["powershell.exe",
                            CONVERT_SCRIPT_PATH],
                            stdout=sys.stdout)
        p.communicate()
