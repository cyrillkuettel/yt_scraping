#!/home/cyrill/anaconda3/envs/yt_scraper/bin/python


import os
from Data_Storage_Structure import Entry
import pyperclip
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from bs4 import BeautifulSoup
import json
from collections import OrderedDict
import random
import requests
# from WordCloudGenerator import myWordCloud
from wordCloudPerTimeUnit import Window
from PIL import Image
from parallelDownloadThumbnails import ThumbnailDownloader
from multi_ThreadPool import MultiThumbnailDownloader
from subprocess import call


EntryObjects = OrderedDict()  # Most Important data structure in the entire Project.
EntrySet = set()  # All titles (lowercase), created each time the program starts

json_file_name = "15k.json"  # in the future, this will be a function where the user selects the file.

file1 = open(json_file_name, 'r')
Lines = file1.readlines()


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


class UiMainWindow(object):
    currentSearchResult = OrderedDict()  # Maps {title -> EntryObject } (After Python3.7 OrderedDicts are the norm)
    titlesOfCurrentSearchResult = []
    currentNumberOfSearchResults = 0

    def searchButtonClicked(self):
        query = self.lineEdit.text()
        if query == "":
            self.updateResultsIntoTable(True)
            return
        self.searchTextChanged(query)

    def searchTextChanged(self, query):
        if len(query) == 1:  # should optimize performance
            return
        self.getSearchResults(query)
        self.updateResultsIntoTable()

    def getSearchResults(self, s):
        self.currentSearchResult = {}  # new Search, clear contents.
        searchString = ''.join(s).lower()
        for title in EntrySet:
            if searchString in title.lower():
                self.titlesOfCurrentSearchResult.append(title)
                self.currentSearchResult[title] = EntryObjects.get(title)

    def updateResultsIntoTable(self, everything=False):
        self.tbl.clear()
        if everything:  # show everything, no filter
            self.prepareToShowAll()  # Here's how it works: prepareToShowAll() fills the local variable
            # currentSearchResult with all 12k Lines.

        count = 0
        for key, value in self.currentSearchResult.items():
            rowPosition = self.tbl.rowCount()
            self.tbl.insertRow(rowPosition)  # Insert empty row
            self.tbl.setItem(count, 0, QtWidgets.QTableWidgetItem(str(value.title)))
            self.tbl.setItem(count, 1, QtWidgets.QTableWidgetItem(str(value.url)))
            self.tbl.setItem(count, 2, QtWidgets.QTableWidgetItem(str(value.thumbnail)))
            self.tbl.setItem(count, 3, QtWidgets.QTableWidgetItem("channel"))

            count += 1

        self.tbl.setHorizontalHeaderLabels(["Title", "Url", "Thumbnail", "Channel"])
        self.currentNumberOfSearchResults = len(self.currentSearchResult)
        self.lblOccurrences.setText("Found {} Occurrences for query".format(self.currentNumberOfSearchResults))
        # delete possibly present blank Lines:
        self.tbl.setRowCount(len(self.currentSearchResult))
        # determine gap between columns
        self.tbl.resizeColumnsToContents()
        header = self.tbl.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)
        header.resizeSection(0, 250)  # the title Column should not be too wide
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Interactive)
        header.resizeSection(1, 370)

    def prepareToShowAll(self):  # Gonna remove this function as well, how useless
        for key, value in EntryObjects.items():
            self.currentSearchResult[key] = EntryObjects.get(key)  # Copy all. This creates redundancy, but simplifies
            self.titlesOfCurrentSearchResult.append(key)
            # the code.

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Youtube History Inspector")
        #MainWindow.showMaximized()
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
        self.lineEdit.textChanged.connect(self.searchTextChanged)

        # Table Widget will replace the Listwidget
        self.tbl = QtWidgets.QTableWidget(self.centralwidget)
        self.tbl.setGeometry(QtCore.QRect(490, 130, 1000, 850))
        self.tbl.setObjectName("resultTable")
        self.tbl.setColumnCount(4)  # Very important, else it's crashing
        self.tbl.setHorizontalHeaderLabels(["Title", "Url", "Thumbnail", "Channel"])
        self.tbl.itemSelectionChanged.connect(self.tableSelectionChanged)
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
        self.slider.setRange(0, self.currentNumberOfSearchResults - 1)  # range = the number of items, Zero-based
        magicNumber = random.randint(-50, 50)  # so it doesn't always show the same Picture.
        self.slider.setSliderPosition(self.currentNumberOfSearchResults // 2 - magicNumber)
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
            self.updateThumbnailPicture_fromLocalFile(title)
            self.lblThumbnail.setText(title)
        except:
            print("Failed to set The Thumbnail. Title is " + title)

    def tableSelectionChanged(self):
        row = self.tbl.selectedItems()
        if (len(row)) == 4:  # 4 could also be vertical, not horizontal
            tryGetTheSecondLine = self.currentSearchResult.get(row[self.tbl.columnCount() - 1].text())
            # if there are more than 1 matches, it's a false alarm
            if tryGetTheSecondLine is not None:
                return

        if len(row) == 4 or len(row) == 1:
            # need do differentiate between selection on thumbnail and selection on the title
            if len(row) == 1:
                try:
                    title = row[0].text()
                    # update the slider position
                    index = self.tbl.currentRow()
                    self.slider.blockSignals(True)
                    self.slider.setSliderPosition(index)
                    self.slider.blockSignals(False)
                    self.updateThumbnailPicture_fromLocalFile(title)
                    self.lblThumbnail.setText(title)
                except Exception as e:
                    print(e)

    def updateThumbnailPicture_fromLocalFile(self, title):
        entry = self.currentSearchResult.get(title)
        file_extension = os.path.splitext(entry.thumbnail)[1]
        file_name = self.getID(entry.url) + file_extension
        thumbnailDirectory = os.path.join(os.getcwd(), "thumbnails")  # connect current Directory to thumbnails dir
        try:
            completeName = os.path.join(thumbnailDirectory, file_name)
            im = Image.open(completeName)
            width, height = im.size  # I think this is the same size always anyway
            image = QtGui.QPixmap(completeName).scaled(width * 0.9, height * 0.9,
                                                       aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                                       transformMode=QtCore.Qt.FastTransformation)
            self.imgLabel.setMinimumSize(width, height)
            self.imgLabel.setPixmap(image)
        except Exception as e:
            print(e)

    def generateWordCloud(self):
        wordCloudGui.injectList(EntryObjects.keys())
        wordCloudGui.show()
        wordCloudGui.generateWordClouds()



    # returns the ID from a given Youtube url
    def getID(self, videoUrl):
        trimBefore = videoUrl[0:32]  # Is equal to "https://www.youtube.com/watch?v="
        s = videoUrl.replace(trimBefore, "")
        return s


if __name__ == "__main__":
    jsonList = loadEachVideoAsJsonIntoArray(Lines)
    td = MultiThumbnailDownloader(jsonList)

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    wordCloudGui = Window()
    sys.exit(app.exec_())
