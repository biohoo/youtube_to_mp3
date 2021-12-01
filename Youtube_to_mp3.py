import youtube_dl


YOUTUBE_DOWNLOADER_OPTIONS = {
    'format': 'worstaudio/worst',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

youtubeURLS = ['https://www.youtube.com/watch?v=jBc_fJgLQ58']


def youtube_to_mp3(links, options=YOUTUBE_DOWNLOADER_OPTIONS):
    '''Takes a list of YouTube URLs and outputs MP3 files according to options.'''

    if not links or type(links) is not list:
        print('Please provide an **iterable** of YouTube URLs.')
        return

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download(links)


if __name__ == "__main__":
    youtube_to_mp3(youtubeURLS)
