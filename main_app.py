from controllers.dataProcessing import *
from resources.mainView import *
from controllers.dbOperations import *


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    
    client, testLogs = connectDB('thy_testsDB', 's2r_testlog')
    testLog = queryDB(testLogs, {"TestId": "2022-06-22_NABITA010.10_3"})
    
    ui.setupUi(MainWindow, graphWidget, dbItemListWidget)
    ui.scene.addWidget(ui.graphicsView.graphWidget)
    ui.graphicsView.curvesPlot(testLog)
    ui.listView.loadItemFromDB(testLogs)
    MainWindow.show()
    
    sys.exit(app.exec_())