import requests
import threading
import os
class ThumbnailDownloader:
    NUMBER_OF_THREADS = 8
    threads = []

    def __init__(self, jsonList):  # Input is all entries
        self.number_of_thumbnails = len(jsonList)
        self.jsonList = jsonList
        # general idea:
        # Read the file. if it exists, read the number. if the self.numer_of_numbnails is higher than
        # the number in file, proceed, else break if it doesn't exist break

        if not os.path.exists(os.getcwd() + "config"):
            os.mkdir("config")

        else:
            completeName = self.getfullPathConfigFile()







        for i in range(self.NUMBER_OF_THREADS):
            t = threading.Thread(target=self.do_request)
            t.daemon = True
            self.threads.append(t)

        for i in range(self.NUMBER_OF_THREADS):
            self.threads[i].start()

        for i in range(self.NUMBER_OF_THREADS):
            self.threads[i].join()
        #

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
            if not os.path.exists(os.getcwd() + "thumbnails"):
                os.mkdir("thumbnails")
            thumbnailDirectory = os.path.join(os.getcwd(), "thumbnails")
            completeName = os.path.join(thumbnailDirectory, file_name)
            if not os.path.exists(completeName): # if the thumbnail is already present
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
            else:
                print("thumbnail exists already. No need to download. ")
                return

    def writeConfigFile(self):
            path = os.path.join(os.getcwd(), "config")
            completeName = os.path.join(path, "config.txt")
            with open(completeName, 'a') as f:
                f.write(str(self.number_of_thumbnails) + '\n')
            print("written config File")

    def readConfigFile(self): # assuming that config.txt exists
        with open(self.getfullPathConfigFile()) as file_in:
            lines = []
            for line in file_in:
                lines.append(line)
            return lines[0] # return the first Line

    def getfullPathConfigFile(self):
            configPath = os.path.join(os.getcwd(), "config")
            completeName = os.path.join(configPath, "config.txt")
            return completeName

