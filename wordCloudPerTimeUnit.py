import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtWidgets
import random

from PIL import Image
from wordcloud import WordCloud, STOPWORDS



class Window(QDialog):
    comment_words = ''
    stopwords = set(STOPWORDS)

    def __init__(self,  parent=None):
        super(Window, self).__init__(parent)

        self.imgLabel = QtWidgets.QLabel()
        # self.imgLabel.setGeometry(QtCore.QRect(10, 240, 166, 94))
        self.imgLabel.setObjectName("thumbnailPreview")
        self.button = QtWidgets.QPushButton()

        # self.button.clicked.connect(self.generateWordCloud)

        self.slider = QtWidgets.QSlider()
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        # self.canvas = FigureCanvas(plt.figure())

        layout = QVBoxLayout()
        layout.addWidget(self.slider)
        layout.addWidget(self.button)
        layout.addWidget(self.imgLabel)
        # layout.addWidget(self.canvas)

        self.setLayout(layout)

    def generateWordClouds(self, titleList):
        for val in titleList:
            val = str(val)
            tokens = val.split()
            # Converts each token into lowercase
            for i in range(len(tokens)):
                tokens[i] = tokens[i].lower()
            self.comment_words += " ".join(tokens) + " "

        wordcloud = WordCloud(width=800, height=800,
                              background_color='white',
                              stopwords=self.stopwords,
                              min_font_size=10).generate(self.comment_words)

        tempFilename = "test_img.png"
        wordcloud.to_file(tempFilename)
        self.updateImage(tempFilename)

    def updateImage(self, path):
        im = Image.open(path)
        width, height = im.size  # I think this is the same size always anyway
        image = QtGui.QPixmap(path).scaled(width, height,
                                           aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                           transformMode=QtCore.Qt.FastTransformation)
        self.imgLabel.setMinimumSize(width, height)
        self.imgLabel.setPixmap(image)

