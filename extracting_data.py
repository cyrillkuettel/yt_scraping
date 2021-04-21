#!/home/cyrill/anaconda3/envs/youtube_history_extractor/bin/python

# run this before running download_thumbnails

import urllib3
import json
import re

from bs4 import BeautifulSoup

verlauf_trimmed = '../verlauf/verlauf_trimmed.html'

test_filename_div = '../verlauf/test_filename_div.html'
link_file = 'link_file.txt'
my_objects = []


class Entry:  # Stores a single Video. information [title, url ,thumbnail, channelUrl] is added to attributes.
    title = ""
    url = ""
    thumbnail = ""
    channelUrl = ""

    def __str__(self):
        return "Title: {} Url:  {}".format(self.title, self.url, self.channelUrl)

    def extractYoutubeIdFromUrl(self):
        failed = False
        try:
            url_data = urlib3.parse_url.urlib3.parse_url(self.url)
        except Exception as e:
            failed = True
        try:
            query = urlib3.parse_url.parse_qs(url_data.query)
        except Exception as e:
            failed = True

        try:
            yt_id = query["v"][0] # ??
        except Exception as e:
            failed = True
        if not failed:
            return yt_id
        else:
            return "ID_extraction_Failed"

    def __init__(self, title, url, channelUrl):

        title = title.replace('\n', '')
        title = re.sub(' +', ' ', title)  # remove whitespace in the middle
        self.title = ''.join(title).encode('utf-8').strip()
        self.url = ''.join(url).encode('utf-8').strip()
        self.channelUrl = ''.join(channelUrl).encode('utf-8').strip()

        yt_id = self.extractYoutubeIdFromUrl()

        if yt_id == "ID_extraction_Failed":
            self.thumbnail = "ID_extraction_Failed"
        else:
            thumbnail_string = "http://img.youtube.com/vi/" + yt_id + "/maxresdefault.jpg"
            self.thumbnail = ''.join(thumbnail_string).encode('utf-8').strip()


# create Entry object, and add all the objects to array my_objects.
def createObjects(filename):  # create the array Of "json objects"
    data = soup = BeautifulSoup(open(filename), "html.parser")
    print("{")
    for div in soup.findAll('div', attrs={'class': 'content-cell'}):  # selects the div which is important
        failed = False
        try:
            url = div.find('a')['href']
            title = div.find('a').contents[0]
            if "https://www.youtube.com" in title:  # avoid deleted Videos
                failed = True
        except Exception as e:
            failed = True

        if not failed:
            entry = Entry(title, url)
            # my_objects.append(entry)
            # print(entry)
            print(vars(entry))  # not working, why
    print("}")  # close the json object

# enhanced. Can now extract title, as well as the channel based on the url
def find_channel_and_title_in_div(
        filename):
    soup = BeautifulSoup(open(filename), "html.parser")
    channel = "https://www.youtube.com/channel/"  # to match the string
    print("{")
    for div in soup.findAll('div', attrs={'class': 'content-cell'}):
        count = 0
        for element in div.findAll('a',
                                   href=True):  # there are multiple <a> Elements in Div. Find the one with "channel"
            channelURL = element['href']  # channel link
            # print(element['href'])
            if channel in channelURL:  # truly is a channel Link
                # print("found channel : {}".format(channelURL))
                count+=1
            else:  # in that case, it links to a Video
                try:
                    title = element.contents[0]  # test this
                    if not "https://www.youtube.com" in title:  # avoid deleted Videos
                        VidUrl = element['href']
                except Exception as e:
                    pass
            entry = Entry(title, VidUrl, channelURL)
            # my_objects.append(entry)
            # print(entry)
            print(vars(entry))  # not working, why
    print("}")  # close the json object

def isChannelLink(channel, channelUrl):
    if channel in channelUrl:
        return True
    else:
        return False
def getOnlyVideoLinks_notChannel(link_file):
    file1 = open(link_file, 'r')
    Lines = file1.readlines()

    count = 0
    # Strips the newline character
    for line in Lines:
        count += 1
        line = line.strip()
        if "channel/" not in line:  #
            # print("Line{}: {}".format(count, line.strip())) # Interesting .format() idea which might be useful later.
            print(line.strip())


if __name__ == "__main__":
    # createObjects(test_filename_div)
    find_channel_and_title_in_div(test_filename_div)
