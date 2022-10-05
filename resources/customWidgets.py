from resources.dataVisul_Widget import dataVisualWidget_Form
from resources.dbList_Widget import dbListWidget_Form
from resources.testImport_Widget import testImportWidget_Form

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import *

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

class testImport_Widget(QtWidgets.QWidget, testImportWidget_Form):
    def __init__(self, parent=None):
        super(testImport_Widget, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.createTest)
        self.pushButton_2.clicked.connect(self.deleteTest)
        self.pushButton_7.clicked.connect(self.selectFolder)
        self.objectDis = {}

    def createTest(self):
        date = self.lineEdit.text()
        deviceId = self.lineEdit_2.text()
        runNum = self.spinBox.value()
        location = self.lineEdit_4.text()
        input = self.lineEdit_3.text()
        kitLot = self.lineEdit_5.text()
        protocol = self.comboBox.currentText()
        devOperator = self.comboBox_2.currentText()
        kitOperator = self.comboBox_3.currentText()

        testId = date + '_' + deviceId + f'_{runNum}'

        document = {}
        document["TestId"] = testId
        document["Protocol"] = protocol
        document["Location"] = location
        document["DeviceOperator"] = devOperator
        document["devOperator"] = kitOperator
        document["KitLot"] = kitLot
        document["Input"] = input
        document["TestDate"] = date
        document["DeviceId"] = deviceId

        self.listWidget.addItem(f'{testId}==>{protocol}==>{input}@{location}')
        self.objectDis[testId] = document

    
    def deleteTest(self):
        curText = self.listWidget.currentItem().text()
        curRow = self.listWidget.currentRow()
        self.listWidget.takeItem(curRow)
        testId = curText[:curText.index("=")]
        self.objectDis.pop(testId)

    def selectFolder(self):
        folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        model = QFileSystemModel()
        model.setRootPath(folderpath)
        
        self.listView.setModel(model)
        self.listView.setRootIndex(model.index(folderpath))
        




        

        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    centralwidget = QtWidgets.QWidget(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
