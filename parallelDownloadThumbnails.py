import requests
import threading
import os

# It's highly unlikely I will ever use this again.

class ThumbnailDownloader:
    NUMBER_OF_THREADS = 8
    threads = []

    def __init__(self, jsonList):
        self.number_of_thumbnails = len(jsonList)
        self.jsonList = jsonList

        configFolder = os.path.join(os.getcwd(), "config")
        if not os.path.isdir(configFolder):
            os.mkdir("config")
            configFile = os.path.join(configFolder, "config.txt")
            file = open(configFile, "w")
            file.close()
        else:
            completeName = self.getfullPathConfigFile()
            if os.path.isfile(completeName):
                number_of_thumbnails_from_last_time = int(self.readConfigFile(completeName).strip())
                if not self.number_of_thumbnails > number_of_thumbnails_from_last_time:
                    print("Already downloaded thumbnails")
                    return

        for i in range(self.NUMBER_OF_THREADS):
            t = threading.Thread(target=self.do_request)
            t.daemon = True
            self.threads.append(t)

        for i in range(self.NUMBER_OF_THREADS):
            self.threads[i].start()

        for i in range(self.NUMBER_OF_THREADS):
            self.threads[i].join()

        self.writeConfigFile(self.getfullPathConfigFile())

    def do_request(self):
        # returns the ID from a given Youtube url
        def getID(videoUrl):
            trimBefore = videoUrl[0:32]  # Is equal to "https://www.youtube.com/watch?v="
            s = videoUrl.replace(trimBefore, "")
            return s

        while len(self.jsonList) > 0:
            data = self.jsonList.pop()
            Videourl = data['url']
            RawThumbnail = data['thumbnail']
            while "ID_extraction_Failed" in RawThumbnail: # only get valid IDs
                data = self.jsonList.pop()
                Videourl = data['url']
                RawThumbnail = data['thumbnail']

            thumbnailURL = RawThumbnail.replace("maxresdefault", "0")
            file_extension = os.path.splitext(thumbnailURL)[1]
            ID = getID(Videourl)
            file_name = ID + file_extension
            if not os.path.isdir(os.getcwd() + "/thumbnails"):
                os.mkdir(os.getcwd() + "/thumbnails")
            thumbnailDirectory = os.path.join(os.getcwd(), "thumbnails")
            completeName = os.path.join(thumbnailDirectory, file_name)
            if not os.path.exists(completeName):  # if the thumbnail is already present
                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
                }
                try:
                    r = requests.get(thumbnailURL, headers=headers)
                    if r.status_code == 200:
                        try:
                            with open(completeName, 'wb') as f:
                                f.write(r.content)
                        except:
                            print("error writing thumbnail")
                        print("It Worked :)")
                except:
                    print("Requests Failed! thumbnailuRL = " + thumbnailURL)
            else:
                pass
               # print("thumbnail exists already. No need to download. ")


    def writeConfigFile(self, path):
        with open(path, 'a') as f:
            f.write(str(self.number_of_thumbnails) + '\n')
        print("Writing new config File")

    def readConfigFile(self, path):  # assuming that config.txt exists
        with open(path) as file_in:
            lines = []
            for line in file_in:
                lines.append(line)
            return lines[0]  # return the first Line

    def getfullPathConfigFile(self):
        configFolder = os.path.join(os.getcwd(), "config")
        completeName = os.path.join(configFolder, "config.txt")
        return completeName
