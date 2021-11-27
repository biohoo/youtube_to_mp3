import youtube_dl

YOUTUBE_DOWNLOADER_OPTIONS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

youtubeURLS = ['https://www.youtube.com/watch?v=jBc_fJgLQ58']


def youtube_to_mp3(links, options=YOUTUBE_DOWNLOADER_OPTIONS):
    '''Takes a list of YouTube URLs and outputs MP3 files according to options.'''

    if links is None:
        print('Please provide an iterable of YouTube URLs')
    else:
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download(links)


if __name__ == "__main__":
    youtube_to_mp3(youtubeURLS)
