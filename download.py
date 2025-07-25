""" 
    This module defines the thread that performs the actual
    functionality of the package, it downloads playlists
"""
import subprocess # nosec
import sys
import threading
import socket
import os
from pathlib import Path
import json
# pylint: disable-next=redefined-builtin
from sys import exit
from pytubefix import Playlist, exceptions
from database.database import Cardb
from config.cfg import CONVERT_SCRIPT_PATH
from config.cfg import HASH_ALGO as hash_algo, ENC_MODULE as enc_module

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
        self.hashes: list|None = None
        try:
            with open(r'security\hashes.json', 'r') as r_file:
                self.hashes = json.load(r_file)
        except FileNotFoundError:
            self._send("Not Found the hashes file!")

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
        # Check we are executing the CORRECT powershell file
        exe_path = str(Path(os.environ.get("windir"),
                                r"System32\WindowsPowerShell\v1.0",
                                "powershell.exe"))
        try:
            with open(exe_path,'r') as exe_fp:
                exe_content_coded = enc_module.encode(exe_fp.read())
                exe_hash = hash_algo(exe_content_coded).hexdigest()
                if exe_hash not in self.hashes:
                    self._send("Corrupted Powershell file for converting mp4 to mp3.\
                                Try redownloading and reinstalling")
                    return
                # Convert mp4 files to mp3 format
                with subprocess.Popen([exe_path,
                                    CONVERT_SCRIPT_PATH],
                                    stdout=sys.stdout,
                                    ) as p: # nosec
                    p.communicate()
        except FileNotFoundError:
            self._send("Not Found Necessary Script!")