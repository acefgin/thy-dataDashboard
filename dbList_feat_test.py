from PyQt5 import QtCore, QtGui, QtWidgets

from resources.customWidgets import dbList_Widget
from controllers.dbOperations import connectDB, queryDB

def setupui(mainWindow):
    MainWindow.setCentralWidget()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    widget1 = dbList_Widget()
    MainWindow.setCentralWidget(widget1)
    MainWindow.setGeometry(200, 200, 320, 720)
    cbboxItems = widget1.listWidget.cbboxItemsSets
    keylist = widget1.listWidget.keyList
    widget1.comboBox.addItem("All")
    widget1.comboBox_2.addItem("All")
    widget1.comboBox_3.addItem("All")
    for i, key in enumerate(keylist):
        for item in cbboxItems[i]:
            if i == 0:
                widget1.comboBox.addItem(item)
            elif i == 1:
                widget1.comboBox_2.addItem(item)
            elif i == 2:
                widget1.comboBox_3.addItem(item)
        if i == 0:
            widget1.comboBox.currentTextChanged.connect(lambda value: widget1.listWidget.updateListItem(keylist[0], value))
        elif i == 1:
            widget1.comboBox_2.currentTextChanged.connect(lambda value: widget1.listWidget.updateListItem(keylist[1], value))
        elif i == 2:
            widget1.comboBox_3.currentTextChanged.connect(lambda value: widget1.listWidget.updateListItem(keylist[2], value))
    MainWindow.show()
    sys.exit(app.exec_())