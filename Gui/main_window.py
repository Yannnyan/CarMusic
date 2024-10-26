import os
import threading
from download import DownloadThread
from tkinter import Frame, Tk, ttk, filedialog, Text, Scrollbar
from tkinter.scrolledtext import ScrolledText
import socket
import tkinter as tk

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Youtube Playlist Downloader")
        self.geometry("400x350")
        
        self.control_frame = Frame(self, width=50,height=20)

        self.browse_playlist = ttk.Button(self.control_frame, text='Open the playlists file', command=self.open_playlists, width=20)
        self.browse_playlist.grid(row=0,column=0,sticky="W")

        self.view_playlist = ttk.Label(self.control_frame,text="Na")
        self.view_playlist.grid(row=0,column=1,sticky="W")

        self.browse_downloads = ttk.Button(self.control_frame,text='Downloads Folder', command=self.open_downloads,width=20)
        self.browse_downloads.grid(row=1,column=0,sticky="W")

        self.view_downloads = ttk.Label(self.control_frame,text="Na")
        self.view_downloads.grid(row=1,column=1,sticky="W")

        self.oper_download = ttk.Button(self.control_frame, text="Start Download", command=self.download,width=20)
        self.oper_download.grid(row=2,column=0,sticky="W")

        self.oper_cancel = ttk.Button(self.control_frame, text="Stop Download", command=self.cancel,width=20)
        self.oper_cancel.grid(row=2,column=1,sticky="W")

        self.control_frame.pack()
        self.view_log = ScrolledText(self,width=400)

        self.view_log.pack()

        self.l_playlists = None
        self.download_finished = False
        self.downloads_path = None
        self.download_process: DownloadThread = None
        self.logging_thread = threading.Thread(target=self.listen_logs,daemon=True)
        self.logging_thread.start()
        self.log_port = None

    def listen_logs(self):
        sock = socket.socket()
        sock.bind(('127.0.0.1',0))
        sock.listen()
        self.log_port = sock.getsockname()[1]
        while True:
            conection, addres = sock.accept()
            log = None
            while log is None or len(log) > 0:
                log = conection.recv(65535).decode("utf-8")
                self.view_log.insert(tk.END,log)

    def download(self):
        if self.l_playlists is None or self.downloads_path is None:
            return
        if (self.download_process is not None) and (not self.download_finished):
            return
        self.download_process = DownloadThread(l_playlist_urls=self.l_playlists, downloads_path=self.downloads_path, server_port=self.log_port)
        self.download_process.start()


    def cancel(self):
        self.download_process.stop = True
        self.download_finished = True
        self.download_process = None

    def open_playlists(self):
        file = filedialog.askopenfile(mode='r', filetypes=[('Playlists list', '*.*')])
        if file:
            self.l_playlists = file.readlines()
            self.view_playlist["text"] = (os.path.abspath(file.name))

    def open_downloads(self):
        path = filedialog.askdirectory(title="Downloads Directory")
        if path:
            self.downloads_path = path
            self.view_downloads["text"] = path

