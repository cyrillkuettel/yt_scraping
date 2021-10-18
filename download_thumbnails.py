import json
from collections import OrderedDict

import requests
import pathlib
import sys
from Data_Storage_Structure import Entry
from bs4 import BeautifulSoup

# This is mostly obsolete. Nostalgia could be the the word

json_file_name = "15k.json"  # in the future, this will be a command line argument args[]
# This class is essentially only used in the initial phase, when the history file is first opened.


path_to_raw_html = "/home/cyrill/Documents/Takeout/new_Takeout_Okt18/youtube_and_youtube_music/Verlauf" \
                   "/Wiedergabeverlauf.html"


# file1 = open(json_file_name, 'r')
# file2 = open(path_to_raw_html, 'r')

# Lines = file1.readlines()
#Lines2 = file2.readlines()

EntryObjects = OrderedDict()
EntrySet = set()


def find_channel_and_title_in_div(filename):
    # TODO:
    #   This function wants as an input the raw html data.
    #   this is quite buggy and does nothing. Getting the channel has not been accomplished so far.
    #   instead of printing, write the output to file.
    #   UPDATE: 18.10: The Wiedergabeverlauf.html is fucking 250000 lines of code.
    #   Strategy for this issue: Easy would be to just split the html into multiple chunks, then do multiprocessing


    soup = BeautifulSoup(open(filename), "html.parser")
    channel = "https://www.youtube.com/channel/"  # to match the string
    print("{")
    for div in soup.findAll('div', attrs={'class': 'content-cell'}):
        count = 0
        for element in div.findAll('a',
                                   href=True):  # there are multiple <a> Elements in Div. Find the one with "channel"
            channelURL = element['href']  # channel link
            # print(element['href'])
            if channel in channelURL:
                # print("found channel : {}".format(channelURL))
                count += 1
            else:  # in that case, it links to a Video
                try:
                    title = element.contents[0]
                    if "https://www.youtube.com" not in title:  # avoid deleted Videos
                        VidUrl = element['href']
                except Exception as e:
                    pass
            entry = Entry(title, VidUrl, channelURL)
            # EntryObjects.append(entry)  # this might not be necessary. In fact, you could just write the output to
            # file.
            print(vars(entry))
    print("}")  # close the json object


def loadEachVideoAsJsonIntoArray(Lines):
    jsonInnerList = []
    for line in Lines:
        data = json.loads(line)  # successfully loaded a json objet.
        title = data['title']
        videoUrl = data['url']
        thumbnail = data['thumbnail']
        try:
            entry = Entry(title, videoUrl, thumbnail)
            EntryObjects[title] = entry
            EntrySet.add(title)
            jsonInnerList.append(data)
        except Exception as e:
            print("{} {}".format("Error in loadEachVideoAsJsonIntoArray during initial phase. ", e))
    return jsonInnerList


if __name__ == "__main__":
    find_channel_and_title_in_div(path_to_raw_html)
    #jsonList = loadEachVideoAsJsonIntoArray(Lines)

# idea. Json is not really necessary , and just use python dict I think.... This would simplify the code tremendously
# consider: Some objects may have not the expected values. Test this! If it occurs, this incidence should not
# confound the correct chronological order. Just jump to the next one.
#

# Initially: Load the html raw data. Then feed that into python dict. And maybe, parallel, thumbnails download
