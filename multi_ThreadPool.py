from multiprocessing.pool import ThreadPool
from time import time
import requests
import os


class MultiThumbnailDownloader:
    CPUS = os.cpu_count()
    def __init__(self, jsonList):
        self.jsonList = jsonList
        start = time()
        ThreadPool(self.CPUS).imap_unordered(self.do_request, jsonList)  # applies the function to all elements of List
        print("Zeit parallel ", time() - start)

    def getID(self, videoUrl):
        trimBefore = videoUrl[0:32]  # Is equal to "https://www.youtube.com/watch?v="
        s = videoUrl.replace(trimBefore, "")
        return s

    def do_request(self, element):
        data = element  # One Single Entry
        Videourl = data['url']
        Oldthumbnail = data['thumbnail']

        uri = Oldthumbnail.replace("maxresdefault", "0")
        file_extension = os.path.splitext(uri)[1]
        ID = self.getID(Videourl)
        file_name = ID + file_extension
        thumbnailDirectory = os.path.join(os.getcwd(), "thumbnails")
        completeName = os.path.join(thumbnailDirectory, file_name)

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }
        if not os.path.exists(completeName):
            try:
                r = requests.get(uri, headers=headers)
            except Exception as e:
                print(e)

            if r.status_code == 200:
                try:
                    with open(completeName, 'wb') as f:
                        f.write(r.content)
                except Exception as e:
                    print(e)