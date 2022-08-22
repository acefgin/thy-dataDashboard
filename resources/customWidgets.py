from resources.dataVisul_Widget import dataVisualWidget_Form
from resources.dbList_Widget import dbListWidget_Form

from PyQt5 import QtCore, QtGui, QtWidgets

class dataVisual_Widget(QtWidgets.QWidget, dataVisualWidget_Form):
    def __init__(self, parent=None):
        super(dataVisual_Widget, self).__init__(parent)
        self.setupUi(self)
        self.checkBox.stateChanged.connect(lambda: self.graphicsView.toggleCurve(self.checkBox.isChecked(), 0))
        self.checkBox_2.stateChanged.connect(lambda: self.graphicsView.toggleCurve(self.checkBox_2.isChecked(), 1))
        self.checkBox_3.stateChanged.connect(lambda: self.graphicsView.toggleCurve(self.checkBox_3.isChecked(), 2))
        self.checkBox_4.stateChanged.connect(lambda: self.graphicsView.toggleCurve(self.checkBox_4.isChecked(), 3))
        self.checkBox_5.stateChanged.connect(lambda: self.graphicsView.toggleCurve(self.checkBox_5.isChecked(), 4))
    
    def updateTestInfo(self, testLog):
        self.checkBox.setChecked(True)
        self.checkBox_2.setChecked(True)
        self.checkBox_3.setChecked(True)
        self.checkBox_4.setChecked(True)
        self.checkBox_5.setChecked(True)
        labelTexts = [testLog["Input"], testLog["Protocol"], testLog["TestDate"]]
        self.label_2.setText(labelTexts[0])
        self.label_4.setText(labelTexts[1])
        self.label_6.setText(labelTexts[2])
        featList = self.graphicsView.curvesPlot(testLog)

        qTable = self.tableWidget

        for c in range(5):
            for r in range(3):
                if r == 0:
                    item = QtWidgets.QTableWidgetItem(str(featList[c][0]))
                elif r == 1:
                    item = QtWidgets.QTableWidgetItem(str(featList[c][3]))
                elif r == 2:
                    item = QtWidgets.QTableWidgetItem(str(featList[c][1]))
                qTable.setItem(r, c, item)

class dbList_Widget(QtWidgets.QWidget, dbListWidget_Form):
    def __init__(self, parent=None):
        super(dbList_Widget, self).__init__(parent)
        self.setupUi(self)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    centralwidget = QtWidgets.QWidget(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())