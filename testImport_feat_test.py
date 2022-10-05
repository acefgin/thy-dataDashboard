from PyQt5 import QtCore, QtGui, QtWidgets

from resources.customWidgets import testImport_Widget
from controllers.dbOperations import connectDB, queryDB

def setupui(mainWindow):
    MainWindow.setCentralWidget()

def onClickSlot(a):
    print(a["Well1"])

def testImportWidgetCtrl(widget1):
    return 0

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    widget1 = testImport_Widget()
    MainWindow.setCentralWidget(widget1)
    MainWindow.setGeometry(200, 200, 1280, 669)
    # listWidgetCtrl(widget1)
    MainWindow.show()
    sys.exit(app.exec_())