import yt_dlp as dlp

PARAMS = {'extract_audio': True, 'format': 'bestaudio', '--skip-unavailable-fragments': True, "extract_flat": True}


async def download(url):
    downloader = dlp.YoutubeDL(PARAMS)
    queue = []
    data = downloader.extract_info(url, download=False)
    try:
        if data["_type"] == "playlist":
            for i in data["entries"]:
                queue.append(i)
            return queue
    except KeyError:
        return data
