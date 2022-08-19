from PyQt5 import QtCore, QtGui, QtWidgets

from resources.customWidgets import dataVisual_Widget
from controllers.dbOperations import connectDB, queryDB
from views.myPlotWidget import *

def setupui(MainWindow):
    MainWindow.setCentralWidget()

_translate = QtCore.QCoreApplication.translate

def testInfoWidgetCtrl(widget):
    client, testLogs = connectDB('thy_testsDB', 's2r_testlog')
    testLog = queryDB(testLogs, {"TestId": "2022-06-22_NABITA010.10_3"})
    client.close()
    labelTexts = [testLog["Input"], testLog["Protocol"], testLog["TestDate"]]
    widget.label_2.setText(labelTexts[0])
    widget.label_4.setText(labelTexts[1])
    widget.label_6.setText(labelTexts[2])
    featList = widget.graphicsView.curvesPlot(testLog)

    qTable = widget.tableWidget

    for c in range(5):
        for r in range(3):
            if r == 0:
                item = QtWidgets.QTableWidgetItem(str(featList[c][0]))
            elif r == 1:
                item = QtWidgets.QTableWidgetItem(str(featList[c][3]))
            elif r == 2:
                item = QtWidgets.QTableWidgetItem(str(featList[c][1]))
            qTable.setItem(r, c, item)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    widget1 = dataVisual_Widget()
    MainWindow.setCentralWidget(widget1)
    MainWindow.setGeometry(200, 200, 320, 720)
    testInfoWidgetCtrl(widget1)
    MainWindow.show()
    sys.exit(app.exec_())