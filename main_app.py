# from controllers.dataProcessing import *
# from resources.mainView import *
# from controllers.dbOperations import *
from views.mainWin import *
from controllers.dbOperations import connectDB, queryDB
from views.myPlotWidget import *

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
    
#     client, testLogs = connectDB('thy_testsDB', 's2r_testlog')
    
#     ui.setupUi(MainWindow, graphWidget, dbItemListWidget)
#     ui.scene.addWidget(ui.graphicsView.graphWidget)
#     ui.listView.loadItemFromDB(testLogs)
#     MainWindow.show()
#     size = ui.graphicsView.size()
#     ui.graphicsView.graphWidget.resize(size * 0.96)
    
#     sys.exit(app.exec_())

def listWidgetCtrl(lsWidget, plotWidget):
    lsWidget.listWidget.onClickSignal.connect(plotWidget.curvesPlot)
    cbboxItems = lsWidget.listWidget.cbboxItemsSets
    keylist = lsWidget.listWidget.keyList
    lsWidget.comboBox.addItem("All")
    lsWidget.comboBox_2.addItem("All")
    lsWidget.comboBox_3.addItem("All")
    for i in range(len(keylist)):
        for item in cbboxItems[i]:
            if i == 0:
                lsWidget.comboBox.addItem(item)
            elif i == 1:
                lsWidget.comboBox_2.addItem(item)
            elif i == 2:
                lsWidget.comboBox_3.addItem(item)
        if i == 0:
            lsWidget.comboBox.currentTextChanged.connect(lambda value: lsWidget.listWidget.updateListItem(keylist[0], value))
        elif i == 1:
            lsWidget.comboBox_2.currentTextChanged.connect(lambda value: lsWidget.listWidget.updateListItem(keylist[1], value))
        elif i == 2:
            lsWidget.comboBox_3.currentTextChanged.connect(lambda value: lsWidget.listWidget.updateListItem(keylist[2], value))

def dataVisualWidgetCtrl(dataVisualWidget):
    dataVisualWidget.addWidget(dataVisualWidget)


class mainAppWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(mainAppWindow, self).__init__(parent)
        self.setupUi(self)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = mainAppWindow()
    listWidgetCtrl(MainWindow.widget_2, MainWindow.widget.graphicsView)
    # dataVisualWidgetCtrl(MainWindow.widget.graphicsView)
    MainWindow.show()
    sys.exit(app.exec_())