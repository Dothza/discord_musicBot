import yt_dlp as dlp

PARAMS = {'extract_audio': True, 'format': 'bestaudio', 'outtmpl': '%(title)s.mp3'}


async def download(url):
    downloader = dlp.YoutubeDL(PARAMS)
    data = downloader.extract_info(url, download=True)
    return data
