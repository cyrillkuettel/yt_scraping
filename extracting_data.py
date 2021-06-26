#!/home/cyrill/anaconda3/envs/youtube_history_extractor/bin/python

# run this before running download_thumbnails
# Very Important: On Laptop I have to run "python3.5 extracting_data.py"

import urllib3
import sys
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from bs4 import BeautifulSoup
import json
import requests
import pathlib
import ctypes

EntryObjects = {}  # Most Important data structure in the entire Project.
json_file_name = "15k.json"  # in the future, this will be a command line argument args[]
file1 = open(json_file_name, 'r')
Lines = file1.readlines()

verlauf_trimmed = '../verlauf/verlauf_trimmed.html'
test_filename_div = '../verlauf/test_filename_div.html'
link_file = 'link_file.txt'


class Entry:  # Stores a single Video. information [title, url ,thumbnail, channelUrl] is added to attributes.
    # What I don't like is that we are using the Entry class for two use cases right now.
    # In the process we are creating a lot of redundancy
    title = ""
    url = ""
    thumbnail = ""
    channelUrl = ""

    def __str__(self):
        return "Entry Object: Title: {} Url:  {}, thumbnailUrl : {}".format(self.title, self.url, self.thumbnail)

    def extractYoutubeIdFromUrl(self):
        failed = False
        try:
            url_data = urllib3.parse_url(self.url)
        except Exception as e:
            failed = True
        try:
            query = urllib3.parse_url.parse_qs(url_data.query)
        except Exception as e:
            failed = True

        try:
            yt_id = query["v"][0]  # ?? who knows what this does, one can only guess
        except Exception as e:
            failed = True
        if not failed:
            return yt_id
        else:
            return "ID_extraction_Failed"

    def __init__(self, title, url, thumbnail):
        self.title = title
        self.url = url
        self.thumbnail = thumbnail

    # similar to Overloading a constructor, the pythonic way. this one we will use When inputting from raw html
    @classmethod
    def withChannelUrl(self, title, url, channelUrl):
        title = title.replace('\n', '')
        title = re.sub(' +', ' ', title)  # remove whitespace in the middle
        self.title = ''.join(title).encode('utf-8').strip()
        self.url = ''.join(url).encode('utf-8').strip()
        self.channelUrl = ''.join(channelUrl).encode('utf-8').strip()

        yt_id = self.extractYoutubeIdFromUrl()

        if not yt_id == "ID_extraction_Failed":  # 99% of the time it's possible to craft the link for thumbnail.
            thumbnail_string = "http://img.youtube.com/vi/" + yt_id + "/maxresdefault.jpg"
            self.thumbnail = ''.join(thumbnail_string).encode('utf-8').strip()
        else:
            self.thumbnail = yt_id


def find_channel_and_title_in_div(filename):
    # TODO:
    #   This function wants as an input the raw html data.
    #   this is quite buggy and does nothing. Getting the channel has not been accomplished so far.
    #   instead of printing, write the output to file.
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
            # EntryObjects.append(entry)  # this might not be necessary. In fact, you could just write the output to file.
            print(vars(entry))
    print("}")  # close the json object


def loadEachVideoAsJsonIntoArray(Lines):
    jsonList = []
    for line in Lines:
        data = json.loads(line)  # successfully loaded a json objet.
        title = data['title']
        videoUrl = data['url']
        thumbnail = data['thumbnail']
        try:
            entry = Entry(title, videoUrl, thumbnail)
            EntryObjects[title] = entry
            jsonList.append(data)
        except Exception as e:
            print("{} {}".format("Error in loadEachVideoAsJsonIntoArray while creating Entry Object. ", e))
    return jsonList


class UiMainWindow(object):
    currentSearchResult = {}  # Dictionary of current Search results. Maps {title -> EntryObject }
    currentNumberOfSearchResults = 0

    # TODO:
    #  -join words together, so it is possible to search multiple
    #  -is quicksort a idea, an improvment?
    #  -make case Insensitive
    #   -trigger Enter event
    #  -also full text search, and "nearness" of words in terms of space
    def getSearchResults(self, currentjsonList, s):
        searchString = ''.join(s)
        count = 0
        resultList = []
        for dic_t in currentjsonList:
            title = self.getID(dic_t["title"])
            if searchString in title:
                count += 1
                resultList.append(dic_t)
        self.currentNumberOfSearchResults = count
        return resultList

    # returns the ID from a given Youtube url
    def getID(self, videoUrl):
        trimBefore = videoUrl[0:32]  # Is equal to "https://www.youtube.com/watch?v="
        s = videoUrl.replace(trimBefore, "")
        return s

    def testButtonClicked(self):

        titlesOfResults = []

        query = self.lineEdit.text()
        results = self.getSearchResults(jsonList, query)
        for item in results:
            title = item['title']
            titlesOfResults.append(title)
            self.currentSearchResult[title] = EntryObjects.get(title)  # this might seem unnecessary, but I want the
            # class to be independent.
        self.lblOccurrences.setText("Found {} Occurrences for query".format(self.currentNumberOfSearchResults))

        # If there is a search result, put the items into Table Widget
        # Logic is not yet written
        # I will write the logic now.
        self.updateResultsIntoTable(results)

    def updateResultsIntoTable(self, results):  # Results holds all the titles
        # Some design stuff
        self.tbl.clear()
        # self.tbl.setRowCount(len(results))
        self.tbl.setHorizontalHeaderLabels(["Title", "Url", "Thumbnail", "Channel"])
        # Expected type 'Union[QBrush, QColor, GlobalColor, QGradient]', got 'int' instead
        # brush = QtGui.QBrush()
        # pen = QtGui.QPen(brush, QtGui.QColor(0, 0, 255, 127))
        # self.tbl.setGridStyle(pen)
        count = 0
        # self.tableWidget.setItem(
        #                 row_number, column_number, QTableWidgetItem(str(data)))
        for key, value in self.currentSearchResult.items():
            rowPosition = self.tbl.rowCount()
            self.tbl.insertRow(rowPosition)  # Insert empty row
            print(value.url)
            print(value.thumbnail)

            self.tbl.setItem(count, 0, QtWidgets.QTableWidgetItem(str(value.title)))
            self.tbl.setItem(count, 1, QtWidgets.QTableWidgetItem(str(value.url)))
            self.tbl.setItem(count, 2, QtWidgets.QTableWidgetItem(str(value.thumbnail)))
            self.tbl.setItem(count, 3, QtWidgets.QTableWidgetItem("channel"))
            count += 1
        self.tbl.resizeColumnsToContents()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1031, 782)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(800, 90, 201, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.testButtonClicked)

        self.lblthumbnail = QtWidgets.QLabel(self.centralwidget)
        self.lblthumbnail.setGeometry(QtCore.QRect(10, 240, 166, 94))
        self.lblthumbnail.setScaledContents(True)
        self.lblthumbnail.setObjectName("lblthumbnail")
        self.lblOccurrences = QtWidgets.QLabel(self.centralwidget)
        self.lblOccurrences.setGeometry(QtCore.QRect(190, 47, 101, 20))
        self.lblOccurrences.setObjectName("lblOccurrences")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(190, 90, 591, 31))
        self.lineEdit.setObjectName("lineEdit")

        # Table Widget will replace the Listwidget
        self.tbl = QtWidgets.QTableWidget(self.centralwidget)
        self.tbl.setGeometry(QtCore.QRect(190, 130, 811, 541))
        self.tbl.setObjectName("resultTable")
        self.tbl.setColumnCount(4)
        #self.tbl.setRowCount(0)
        # self.tbl.itemSelectionChanged(self.selectionChanged)

        self.thumbnail = QtWidgets.QLabel(self.centralwidget)
        self.thumbnail.setGeometry(QtCore.QRect(10, 240, 170, 96))
        self.thumbnail.setText("")
        self.thumbnail.setScaledContents(True)
        self.thumbnail.setObjectName("thumbnail")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1031, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionImport = QtWidgets.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        self.menuFile.addAction(self.actionImport)
        self.menubar.addAction(self.menuFile.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Search"))
        self.lblthumbnail.setText(_translate("MainWindow", "View"))
        self.lblOccurrences.setText(_translate("MainWindow", "occurrences"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionImport.setText(_translate("MainWindow", "Import"))

    def selectionChanged(self):
        title = self.tbl.currentItem().text()
        print(self.currentSearchResult.get(title).thumbnail)


if __name__ == "__main__":
    jsonList = loadEachVideoAsJsonIntoArray(Lines)

    # TODO:
    #       - Instead of ListView, use a Table Widget ( like in prototype1.py )                 [ ]
    #       - Thumbnail                                                                         [ ]

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
