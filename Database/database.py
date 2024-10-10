import sqlite3
from pytubefix import YouTube
import uuid

class Cardb:
    
    def __init__(self) -> None:
        self.con = sqlite3.connect('carmusic.db')
        self.cur = self.con.cursor()
        if not self.check_tables_exist():
            self.create_tables()

    def create_tables(self):
        self.cur.execute("CREATE TABLE song(id,title,author,description,likes,views,rating,url)")
        self.cur.execute("CREATE TABLE songincar(id,songId)")

    def check_tables_exist(self) -> bool:
        res = self.cur.execute("SELECT name FROM sqlite_master")
        tables = res.fetchall()
        print(tables)
        return ('song',) in tables and ('songincar',) in tables

    def insert_song(self,video: YouTube, url: str, in_car: bool):
        data = (
            str(uuid.uuid4()),
            video.title,
            video.author,
            video.description,
            video.likes,
            video.views,
            video.rating,
            url,
        )
        in_car_data = (
            str(uuid.uuid4()),
            data[0]
        )
        self.cur.execute("INSERT INTO song VALUES(?,?,?,?,?,?,?,?)", data)
        if in_car:
            self.cur.execute("INSERT INTO songincar VALUES(?,?)", in_car_data)
        self.con.commit()

    def check_song_exist(self,video: YouTube) -> bool:
        res = self.cur.execute("""
                            SELECT * FROM songincar 
                            INNER JOIN song on songincar.songId = song.id
                            WHERE title = ?
                        """, (video.title,))
        return len(res.fetchall()) > 0
