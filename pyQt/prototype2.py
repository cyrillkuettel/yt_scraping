
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1031, 782)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(800, 90, 201, 31))
        self.pushButton.setObjectName("pushButton")
        self.lblthumbnail = QtWidgets.QLabel(self.centralwidget)
        self.lblthumbnail.setGeometry(QtCore.QRect(10, 240, 166, 94))
        self.lblthumbnail.setScaledContents(True)
        self.lblthumbnail.setObjectName("lblthumbnail")
        self.tbl = QtWidgets.QTableWidget(self.centralwidget)
        self.tbl.setGeometry(QtCore.QRect(190, 130, 811, 541))
        self.tbl.setObjectName("tbl")
        self.tbl.setColumnCount(0)
        self.tbl.setRowCount(0)
        self.lblOccurrences = QtWidgets.QLabel(self.centralwidget)
        self.lblOccurrences.setGeometry(QtCore.QRect(190, 47, 101, 20))
        self.lblOccurrences.setObjectName("lblOccurrences")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(190, 90, 591, 31))
        self.lineEdit.setObjectName("lineEdit")
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
