import yt_dlp as dlp
from data.song import Song
from data.db_session import *

PARAMS = {'extract_audio': True, 'format': 'bestaudio', '--skip-unavailable-fragments': True, "extract_flat": True}


async def download(url):
    downloader = dlp.YoutubeDL(PARAMS)
    data = downloader.extract_info(url, download=False)
    try:
        if data["_type"] == "playlist":
            for i in data["entries"]:
                song = Song()
                song.name = str(i["title"])
                song.link = str((downloader.extract_info(i['url'], download=False))["url"])
                song.playlist_link = str(url)
                song.playlist_name = str(data["title"])
                db_sess = create_session()
                db_sess.add(song)
                db_sess.commit()
    except KeyError:
        song = Song()
        song.name = data["title"]
        song.link = data["url"]
        db_sess = create_session()
        db_sess.add(song)
        db_sess.commit()
    return
