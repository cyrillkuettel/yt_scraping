# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prototype1.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(966, 725)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(700, 90, 101, 31))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(190, 90, 501, 31))
        self.textEdit.setObjectName("textEdit")
        self.lblthumbnail = QtWidgets.QLabel(self.centralwidget)
        self.lblthumbnail.setGeometry(QtCore.QRect(10, 240, 166, 94))
        self.lblthumbnail.setScaledContents(True)
        self.lblthumbnail.setObjectName("lblthumbnail")
        self.tbl = QtWidgets.QTableWidget(self.centralwidget)
        self.tbl.setGeometry(QtCore.QRect(190, 130, 611, 541))
        self.tbl.setObjectName("tbl")
        self.tbl.setColumnCount(0)
        self.tbl.setRowCount(0)
        self.lblInfo = QtWidgets.QLabel(self.centralwidget)
        self.lblInfo.setGeometry(QtCore.QRect(190, 50, 67, 17))
        self.lblInfo.setText("")
        self.lblInfo.setObjectName("lblInfo")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 966, 22))
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
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionImport.setText(_translate("MainWindow", "Import"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

