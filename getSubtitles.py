from __future__ import unicode_literals
import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'skip_download': True,
    'writesubtitles': True,
    'allsubtitles': True,
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

if __name__ == "__main__":
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['http://www.youtube.com/watch?v=sS9QBLrezuY'])
