#!/home/cyrill/anaconda3/envs/youtube_history_extractor/bin/python

# run this before running download_thumbnails

import urllib3
import json
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from bs4 import BeautifulSoup
import json
import requests
import pathlib
import sys
import ctypes

json_file_name = "15k.json"  # in the future, this will be a command line argument args[]
file1 = open(json_file_name, 'r')
Lines = file1.readlines()

verlauf_trimmed = '../verlauf/verlauf_trimmed.html'
test_filename_div = '../verlauf/test_filename_div.html'
link_file = 'link_file.txt'
my_objects = []  # deprecated. Write to file for permanent storage


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
            yt_id = query["v"][0]  # ??
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
            if isChannelLink(channel, channelURL):
                # print("found channel : {}".format(channelURL))
                count += 1
            else:  # in that case, it links to a Video
                try:
                    title = element.contents[0]  # test this
                    if not "https://www.youtube.com" in title:  # avoid deleted Videos
                        VidUrl = element['href']
                except Exception as e:
                    pass
            entry = Entry(title, VidUrl, channelURL)
            # my_objects.append(entry)  # this might not be necessary. In fact, you could just write the output to file.
            print(vars(entry))
    print("}")  # close the json object


def loadEachVideoAsJsonIntoArray(Lines):
    jsonList = []
    for line in Lines:
        # print(line)
        try:
            data = json.loads(line)  # successfully loaded a json objet. note there is also json.load without an 's'
            jsonList.append(data)
        except Exception as e:
            print("{} {}".format("could not load json for this video. Probably url not valid. ", e))
    return jsonList


# TODO:
#  join words together, so it is possible to search multiple
def getSearchResults(jsonList, s):
    searchString = ''.join(s)
    print(searchString)
    count = 0
    resultList = []
    for dic_t in jsonList:
        title = getID(dic_t["title"])  # strip the title
        if searchString in title:
            count += 1
            resultList.append(dic_t)
    print("found = {} occurrences".format(count))
    return resultList


def getID(videoUrl):
    trimBefore = videoUrl[0:32]  # Is equal to "https://www.youtube.com/watch?v="
    s = videoUrl.replace(trimBefore, "")
    return s


def isChannelLink(channel, channelUrl):
    if channel in channelUrl:
        return True
    else:
        return False


class Ui_MainWindow(object):
    def testButtonClicked(self):
        self.listWidget.clear()
        titlesOfResults = []
        searchWord = self.textEdit.toPlainText()
        results = getSearchResults(jsonList, searchWord)
        for item in results:
            titlesOfResults.append(item['title'])

        self.listWidget.addItems(titlesOfResults)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(400, 60, 89, 31))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(30, 60, 351, 31))
        self.textEdit.setObjectName("textEdit")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 110, 771, 461))
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 10, 521, 17))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.pushButton.clicked.connect(self.testButtonClicked)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Search"))
        self.label.setText(_translate("MainWindow", "Pleased To meet you, hope you guessed my name."))


if __name__ == "__main__":
    jsonList = loadEachVideoAsJsonIntoArray(Lines)
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
