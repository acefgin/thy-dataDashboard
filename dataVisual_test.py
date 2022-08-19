from PyQt5 import QtCore, QtGui, QtWidgets

from resources.customWidgets import dataVisual_Widget
from controllers.dbOperations import connectDB, queryDB
from views.myPlotWidget import *

def setupui(MainWindow):
    MainWindow.setCentralWidget()

def dataVisualWidgetCtrl(dataVisualWidget):
    client, testLogs = connectDB('thy_testsDB', 's2r_testlog')
    testLog = queryDB(testLogs, {"TestId": "2022-06-22_NABITA010.10_3"})
    client.close()
    dataVisualWidget.curvesPlot(testLog)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    widget1 = dataVisual_Widget()
    MainWindow.setCentralWidget(widget1)
    MainWindow.setGeometry(200, 200, 320, 720)
    dataVisualWidgetCtrl(widget1.graphicsView)
    MainWindow.show()
    sys.exit(app.exec_())