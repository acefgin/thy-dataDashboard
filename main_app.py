from controllers.dataProcessing import *
from resources.mainView import *
from controllers.dbOperations import *
# from views.mainWin import *


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    
    client, testLogs = connectDB('thy_testsDB', 's2r_testlog')
    
    ui.setupUi(MainWindow, graphWidget, dbItemListWidget)
    ui.scene.addWidget(ui.graphicsView.graphWidget)
    ui.listView.loadItemFromDB(testLogs)
    MainWindow.show()
    size = ui.graphicsView.size()
    ui.graphicsView.graphWidget.resize(size * 0.96)
    
    sys.exit(app.exec_())

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())