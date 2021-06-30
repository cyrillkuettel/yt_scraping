import os
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtWidgets
import pprint
from PIL import Image
from wordcloud import WordCloud, STOPWORDS


class Window(QDialog):
    comment_words = ''
    wordcloudImageFolder = "wordclouds"
    stopwords = set(STOPWORDS)
    wordList = set()  # Main List, holding all the titles

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.imgLabel = QtWidgets.QLabel()
        self.imgLabel.setObjectName("thumbnailPreview")
        self.slider = QtWidgets.QSlider()
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        layout = QVBoxLayout()

        layout.addWidget(self.imgLabel)
        layout.addWidget(self.slider)
        # layout.addWidget(self.canvas)
        self.setLayout(layout)

    def injectList(self, wordList):
        self.wordList = [item.lower() for item in list(wordList)]

    def generateWordClouds(self):
        if len(self.wordList) == 0:
            print("Could not find wordList. First call injectList(list)")
            return

        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        if not os.path.isdir(self.wordcloudImageFolder):
            os.mkdir(self.wordcloudImageFolder)


        numberOfChunks = 6  # split the list
        sizeOfChunk = len(self.wordList) // numberOfChunks
        nestedList = chunks(self.wordList, sizeOfChunk)
        count = -1

        for chunk in nestedList:
            count += 1
            self.comment_words = ""  # reset the String to avoid accumulation
            for val in chunk:
                val = str(val)
                tokens = val.split()
                self.comment_words += " ".join(tokens) + " "

            wordCloudFileName = "test_img_{}.png".format(count)
            finalWordCloudFileName = os.path.join(self.wordcloudImageFolder, wordCloudFileName)
            if os.path.exists(finalWordCloudFileName):
                continue
            wordcloud = WordCloud(width=800, height=800,
                                  background_color='white',
                                  stopwords=self.stopwords,
                                  min_font_size=10).generate(self.comment_words)

            wordcloud.to_file(finalWordCloudFileName)
            self.updateImage(finalWordCloudFileName)

            print("Generated a wordCloud")

    def updateImage(self, path):
        im = Image.open(path)
        width, height = im.size
        image = QtGui.QPixmap(path).scaled(width, height,
                                           aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                           transformMode=QtCore.Qt.FastTransformation)
        self.imgLabel.setMinimumSize(width, height)
        self.imgLabel.setPixmap(image)
