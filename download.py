""" 
    This module defines the thread that performs the actual
    functionality of the package, it downloads playlists
"""
import subprocess
import sys
import threading
import socket
# pylint: disable-next=redefined-builtin
from sys import exit
from pytubefix import Playlist, exceptions
from Database.database import Cardb
from config.env import CONVERT_SCRIPT_PATH

class DownloadThread(threading.Thread):
    """
        Downloader thread simple
    """
    def __init__(self, l_playlist_urls, downloads_path, server_port: int):
        threading.Thread.__init__(self,daemon=True)
        self.l_playlist_urls = l_playlist_urls
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect(('127.0.0.1',server_port))
        self.stop = False

        self.download_destination = downloads_path

    def _send(self, format_message: str):
        self.connection.send(format_message.encode("utf-8"))

    def run(self):
        database = Cardb()
        for s_playlist_url in self.l_playlist_urls:
            playlist = Playlist(s_playlist_url)
            self._send(f"Videos Count: {str(len(playlist.video_urls))} \n")
            for video in playlist.videos:
                if self.stop:
                    self.halt()
                self._send(f"Author: {video.author:40}   Title: {video.title} \n")
                try:
                    audio_stream = video.streams.get_audio_only("mp4")
                    if not database.check_song_exist(video):
                        audio_stream.download(self.download_destination)
                        database.insert_song(video,video.watch_url, True)
                except(exceptions.LiveStreamError, exceptions.VideoUnavailable,
                        exceptions.VideoPrivate,exceptions.VideoRegionBlocked,
                        exceptions.UnknownVideoError,exceptions.AgeRestrictedError,
                        AttributeError):
                    continue

    def halt(self):
        """ Halting the thread"""
        exit(0)

    def convert_to_mp3(self):
        """ Used for file format conversion """
        # Convert mp4 files to mp3 format
        with subprocess.Popen(["powershell.exe",
                            CONVERT_SCRIPT_PATH],
                            stdout=sys.stdout) as p:
            p.communicate()
