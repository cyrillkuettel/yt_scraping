#!/home/cyrill/anaconda3/envs/youtube_history_extractor/bin/python

# run this before running download_thumbnails
# Very Important: On Laptop I have to run "python3.5 extracting_data.py"
import os
from typing import Dict, Any

import pyperclip
import urllib3
import sys
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from bs4 import BeautifulSoup
import json
from collections import OrderedDict
import random
import requests
from WordCloudGenerator import myWordCloud
from PIL import Image
from parallelDownloadThumbnails import ThumbnailDownloader

EntryObjects = OrderedDict()  # type: Dict[Any, Any] # Most Important data structure in the entire Project.
json_file_name = "15k.json"  # in the future, this will be a command line argument args[]
file1 = open(json_file_name, 'r')
Lines = file1.readlines()

verlauf_trimmed = '../verlauf/verlauf_trimmed.html'
test_filename_div = '../verlauf/test_filename_div.html'
link_file = 'link_file.txt'


# noinspection PyInterpreter
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

    # similar to Overloading a constructor, the pythonic way. this one we will use when inputting from raw html
    @classmethod
    def withChannelUrl(self, title, url, channelUrl):
        title = title.replace('\n', '')
        title = re.sub(' +', ' ', title)  # remove whitespace in the middle
        self.title = ''.join(title).encode('utf-8').strip()
        self.url = ''.join(url).encode('utf-8').strip()
        self.channelUrl = ''.join(channelUrl).encode('utf-8').strip()

        yt_id = self.extractYoutubeIdFromUrl()

        if not yt_id == "ID_extraction_Failed":  # 99% of the time it's possible to craft the link for thumbnail.
            thumbnail_string = "http://img.youtube.com/vi/" + yt_id + "/0.jpg"
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
    currentSearchResult = OrderedDict()  # Maps {title -> EntryObject } (After Python3.7 OrderedDicts are the norm)
    titlesOfCurrentSearchResult = []
    currentNumberOfSearchResults = 0

    # TODO:
    #  -join words together, so it is possible to search multiple
    #  -is quicksort a idea, an improvment?
    #  -also full text search, and "nearness" of words in terms of space

    def getSearchResults(self, currentjsonList, s):
        searchString = ''.join(s).lower()
        resultList = []
        for dic_t in currentjsonList:
            title = self.getID(dic_t["title"])
            if searchString in title.lower():
                resultList.append(dic_t)
        return resultList

    # returns the ID from a given Youtube url
    def getID(self, videoUrl):
        trimBefore = videoUrl[0:32]  # Is equal to "https://www.youtube.com/watch?v="
        s = videoUrl.replace(trimBefore, "")
        return s

    def searchButtonClicked(self):
        query = self.lineEdit.text()
        if query == "":
            self.updateResultsIntoTable(True)
            return
        results = self.getSearchResults(jsonList, query)
        self.currentSearchResult = {}  # new Search, clear contents.
        for item in results:
            title = item['title']
            self.titlesOfCurrentSearchResult.append(title)
            self.currentSearchResult[title] = EntryObjects.get(title)  # this might seem unnecessary, but I want the
            # class to be independent.
        # print('\n'.join('{}'.format(item) for item in titlesOfCurrentSearchResult))
        self.updateResultsIntoTable()

    def updateResultsIntoTable(self, everything=False):
        self.tbl.clear()
        if everything:  # show everything, no filter
            self.prepareToShowAll()  # Here's how it works: prepareToShowAll() fills the local variable
            # currentSearchResult with all 12k Lines

        self.tbl.setHorizontalHeaderLabels(["Title", "Url", "Thumbnail", "Channel"])
        self.currentNumberOfSearchResults = len(self.currentSearchResult)
        self.slider.setRange(0, self.currentNumberOfSearchResults - 1)  # range = the number of items, Zero-based
        magicNumber = random.randint(-50, 50)
        self.slider.setSliderPosition(self.currentNumberOfSearchResults // 2 - magicNumber)
        self.lblOccurrences.setText("Found {} Occurrences for query".format(self.currentNumberOfSearchResults))
        count = 0
        for key, value in self.currentSearchResult.items():
            rowPosition = self.tbl.rowCount()
            self.tbl.insertRow(rowPosition)  # Insert empty row
            self.tbl.setItem(count, 0, QtWidgets.QTableWidgetItem(str(value.title)))
            self.tbl.setItem(count, 1, QtWidgets.QTableWidgetItem(str(value.url)))
            self.tbl.setItem(count, 2, QtWidgets.QTableWidgetItem(str(value.thumbnail)))
            self.tbl.setItem(count, 3, QtWidgets.QTableWidgetItem("channel"))

            count += 1
        # delete possibly present blank Lines:
        self.tbl.setRowCount(len(self.currentSearchResult))
        # determine gap between columns
        self.tbl.resizeColumnsToContents()
        header = self.tbl.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)
        header.resizeSection(0, 250)  # the title Column should not be too wide
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Interactive)
        header.resizeSection(1, 370)

    def prepareToShowAll(self):
        for key, value in EntryObjects.items():
            self.currentSearchResult[key] = EntryObjects.get(key)  # Copy all. This creates redundancy, but simplifies
            self.titlesOfCurrentSearchResult.append(key)
            # the code.

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Youtube History Inspector")
        MainWindow.showMaximized()
        MainWindow.setMinimumSize(1300, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1100, 90, 201, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.searchButtonClicked)

        self.wordCloudButton = QtWidgets.QPushButton(self.centralwidget)
        self.wordCloudButton.setGeometry(QtCore.QRect(1100, 40, 201, 31))
        self.wordCloudButton.setObjectName("wordCloudButton")
        self.wordCloudButton.clicked.connect(self.generateWordCloud)

        self.imgLabel = QtWidgets.QLabel(self.centralwidget)
        self.imgLabel.setGeometry(QtCore.QRect(10, 240, 166, 94))
        self.imgLabel.setObjectName("thumbnailPreview")

        self.lblThumbnail = QtWidgets.QLabel(self.centralwidget)
        self.lblThumbnail.setGeometry(QtCore.QRect(20, 560, 400, 96))
        self.lblThumbnail.setFont(QtGui.QFont('Arial', 15))
        self.lblThumbnail.setText("Title goes here")

        self.lblOccurrences = QtWidgets.QLabel(self.centralwidget)
        self.lblOccurrences.setGeometry(QtCore.QRect(490, 47, 250, 20))
        self.lblOccurrences.setObjectName("lblOccurrences")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(490, 90, 591, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.returnPressed.connect(self.pushButton.click)  # Trigger return Button

        # Table Widget will replace the Listwidget
        self.tbl = QtWidgets.QTableWidget(self.centralwidget)
        self.tbl.setGeometry(QtCore.QRect(490, 130, 1000, 850))
        self.tbl.setObjectName("resultTable")
        self.tbl.setColumnCount(4)  # Very important, else it's crashing
        self.tbl.setHorizontalHeaderLabels(["Title", "Url", "Thumbnail", "Channel"])
        self.tbl.itemSelectionChanged.connect(self.selectionChanged)
        # Allow Context menu
        self.tbl.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # Connect the signal request to the slot (click the right mouse button to call the method)
        self.tbl.customContextMenuRequested.connect(self.generateContextMenu)



        self.slider = QtWidgets.QSlider(self.centralwidget)
        self.slider.setGeometry(QtCore.QRect(20, 610, 360, 36))
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("horizontalSlider")
        self.slider.valueChanged.connect(self.sliderValueChanged)
        self.slider.setTickPosition(0)

        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1031, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionImport = QtWidgets.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        self.menuFile.addAction(self.actionImport)
        self.menubar.addAction(self.menuFile.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #  In the beginning, show all items of course and initialize some stuff
        self.updateResultsIntoTable(everything=True)
        # pos is the clicked position

    def generateContextMenu(self, pos):
        # print(pos)
        row = self.tbl.selectedItems()
        if len(row) == 1:
            print(row)
            menu = QtWidgets.QMenu()
            copyAction = menu.addAction("Copy Cell")
            # Make the menu display in the normal position
            screenPos = self.tbl.mapToGlobal(pos)
            # Click on a menu item to return, making it blocked
            action = menu.exec(screenPos)
            if action == copyAction:
                print('Copying row {}'.format(row[0].text()))
                pyperclip.copy(row[0].text())  # Text Copied to clipboard

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Search"))
        self.wordCloudButton.setText(_translate("MainWindow", "WordCloud"))
        self.lblOccurrences.setText(_translate("MainWindow", "occurrences"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionImport.setText(_translate("MainWindow", "Import"))

    def sliderValueChanged(self, value):
        # finally I'm writing code again. this is it. This is what I love. This is the flow.
        # print(self.titlesOfCurrentSearchResult[value])
        title = self.titlesOfCurrentSearchResult[value]
        try:
            self.updateThumbnailPicture(title)
        except:
            print("Failed to set The Thumbnail.")
        self.lblThumbnail.setText(title)

    def selectionChanged(self):
        row = self.tbl.selectedItems()
        # only trigger when 1 Row is selected (or a part thereof)
        if (len(row)) == 4:
            tryGetTheSecondLine = self.currentSearchResult.get(row[self.tbl.columnCount() - 1].text())
            # ensure it is actually the row. For this we can check the dictionary access. if there are more than
            # 1 matches, it's a false alarm
            if tryGetTheSecondLine is not None:
                return

        if len(row) == 4 or len(row) == 1:
            # need do differentiate between selection on thumbnail and selection on the title
            if len(row) == 1:
                try:
                    title = row[0].text()
                    self.updateThumbnailPicture(title)
                except:
                    print("Error. Possible that id could not be found")
                    return
            try:
                thumbnailURL = self.currentSearchResult.get(row[0].text()).thumbnail
            except:
                return  # this will happen if the cell is anything else than a  title

            """ 
            # if all else fails, we can use this.  This downloads the image with requests
            thumbnailURL = thumbnailURL.replace("maxresdefault", "0")
            thumbnailDirectory = os.path.join(os.getcwd(), "thumbnails")
            
            file_extension = os.path.splitext(thumbnailURL)[1]
            file_name = "0" + file_extension
            completeName = os.path.join(thumbnailDirectory, file_name)
            r = requests.get(thumbnailURL)
           
          
                with open(completeName, 'wb') as f:
                    f.write(r.content)
                im = Image.open(completeName)
                width, height = im.size
                 """

    def updateThumbnailPicture(self, title):
        entry = self.currentSearchResult.get(title)
        file_extension = os.path.splitext(entry.thumbnail)[1]
        file_name = self.getID(entry.url) + file_extension
        thumbnailDirectory = os.path.join(os.getcwd(), "thumbnails")  # connect current Directory to thumbnails dir
        completeName = os.path.join(thumbnailDirectory, file_name)
        im = Image.open(completeName)
        width, height = im.size  # I think this is the same size always anyway
        image = QtGui.QPixmap(completeName).scaled(width * 0.9, height * 0.9,
                                                   aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                                   transformMode=QtCore.Qt.FastTransformation)
        self.imgLabel.setMinimumSize(width, height)
        self.imgLabel.setPixmap(image)

    def generateWordCloud(self):
        wordCloud = myWordCloud(EntryObjects.keys())
        wordCloud.show()


if __name__ == "__main__":
    jsonList = loadEachVideoAsJsonIntoArray(Lines)
    # td = ThumbnailDownloader(jsonList)

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
