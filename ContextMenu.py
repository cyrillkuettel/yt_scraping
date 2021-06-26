import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

'''
How to pop up the menu
 How to pop up a menu when the conditions are met
'''
class TableWidgetContextMenu(QWidget):
    def __init__(self):
        super(TableWidgetContextMenu, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Show context menu in table")
        self.resize(500, 300)
        layout = QHBoxLayout()

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(3)

        layout.addWidget(self.tableWidget)

        self.tableWidget.setHorizontalHeaderLabels(['Name', 'gender', 'age'])

        # first row
        Item1 = QTableWidgetItem("Pharaoh")
        self.tableWidget.setItem(0, 0, Item1)

        Item2 = QTableWidgetItem("male")
        self.tableWidget.setItem(0, 1, Item2)

        Item3 = QTableWidgetItem("30")
        self.tableWidget.setItem(0, 2, Item3)

        # second line
        Item1 = QTableWidgetItem("Little King")
        self.tableWidget.setItem(1, 0, Item1)

        Item2 = QTableWidgetItem("male")
        self.tableWidget.setItem(1, 1, Item2)

        Item3 = QTableWidgetItem("28")
        self.tableWidget.setItem(1, 2, Item3)

        # The third row
        Item1 = QTableWidgetItem("Little Red")
        self.tableWidget.setItem(2, 0, Item1)

        Item2 = QTableWidgetItem("Female")
        self.tableWidget.setItem(2, 1, Item2)

        Item3 = QTableWidgetItem("18")
        self.tableWidget.setItem(2, 2, Item3)

        # Allow popup menu
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)

        # Connect the signal request to the slot (click the right mouse button to call the method)
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)

        self.setLayout(layout)

    # pos is the clicked position
    def generateMenu(self, pos):
        print(pos)
        # Get index
        for i in self.tableWidget.selectionModel().selection().indexes():
            rowNum = i.row()

        # If the selected row index is less than 1, the context menu will pop up
        if rowNum < 3:
            menu = QMenu()
            item1 = menu.addAction("Menu 1")
            item2 = menu.addAction("Menu 2")
            item3 = menu.addAction("Menu 3")
            # Make the menu display in the normal position
            screenPos = self.tableWidget.mapToGlobal(pos)

            # Click on a menu item to return, making it blocked
            action = menu.exec(screenPos)
            if action == item1:
                print('Select Menu 1', self.tableWidget.item(rowNum, 0).text())
            if action == item2:
                print('Select menu 2', self.tableWidget.item(rowNum, 0).text())
            if action == item3:
                print('Select menu 3', self.tableWidget.item(rowNum, 0).text())
            else:
                return



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = TableWidgetContextMenu()
    main.show()
    sys.exit(app.exec_())
