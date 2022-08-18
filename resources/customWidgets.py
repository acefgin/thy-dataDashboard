from dataVisul_Widget import dataVisualWidget_Form
from dbList_Widget import dbListWidget_Form

from PyQt5 import QtCore, QtGui, QtWidgets

class dataVisual_Widget(QtWidgets.QWidget, dataVisualWidget_Form):
    def __init__(self, parent=None):
        super(dataVisual_Widget, self).__init__(parent)
        self.setupUi(self)

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