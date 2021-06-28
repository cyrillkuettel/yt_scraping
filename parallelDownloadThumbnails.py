import json

import requests
import threading
import numpy as np
import os
from itertools import islice


class ThumbnailDownloader:
    NUMBER_OF_THREADS = 8
    threads = []

    def __init__(self, jsonList):  # Input is all entires
        self.jsonList = jsonList
        for i in range(self.NUMBER_OF_THREADS):
            t = threading.Thread(target=self.do_request)
            t.daemon = True
            self.threads.append(t)

        for i in range(self.NUMBER_OF_THREADS):
            self.threads[i].start()

        for i in range(self.NUMBER_OF_THREADS):
            self.threads[i].join()

    def do_request(self):
        # returns the ID from a given Youtube url
        def getID(videoUrl):
            trimBefore = videoUrl[0:32]  # Is equal to "https://www.youtube.com/watch?v="
            s = videoUrl.replace(trimBefore, "")
            return s

        while len(self.jsonList) > 0:
            data = self.jsonList.pop()
            Videourl = data['url']
            Oldthumbnail = data['thumbnail']

            thumbnailURL = Oldthumbnail.replace("maxresdefault", "0")
            file_extension = os.path.splitext(thumbnailURL)[1]
            ID = getID(Videourl)
            file_name = ID + file_extension
            thumbnailDirectory = os.path.join(os.getcwd(), "thumbnails")
            completeName = os.path.join(thumbnailDirectory, file_name)

            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
            }

            try:
                r = requests.get(thumbnailURL, headers=headers)
            except:
                print("Requests Failed!")

            try:
                with open(completeName, 'wb') as f:
                    f.write(r.content)
            except:
                print("error writing File")
            print("It Worked :)")


