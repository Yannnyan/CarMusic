from pytubefix import Playlist, exceptions
from Database.database import check_song_exist, insert_song
import subprocess, sys
from env import *


with open("playlists.txt") as f_playlist_urls:
    l_playlist_urls = f_playlist_urls.readlines()
    for s_playlist_url in l_playlist_urls:
        playlist = Playlist(s_playlist_url)
        print("Videos Count: ", len(playlist.video_urls))
        for video in playlist.videos:
            print('Author: {0:40}   Title: {1}'.format(video.author, video.title))
            try:
                audio_stream = video.streams.get_audio_only("mp4")
                if not check_song_exist(video):
                        audio_stream.download(DOWNLOAD_DESTINATION)
                        insert_song(video,video.watch_url, True)
            except(exceptions.LiveStreamError, exceptions.VideoUnavailable, exceptions.VideoPrivate, exceptions.VideoRegionBlocked, exceptions.UnknownVideoError,exceptions.AgeRestrictedError, AttributeError):
                continue

# Convert mp4 files to mp3 format
p = subprocess.Popen(["powershell.exe",
                      CONVERT_SCRIPT_PATH],
                      stdout=sys.stdout)
p.communicate()