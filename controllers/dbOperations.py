import pymongo
import json
import gridfs
import os
import sys      
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QListWidgetItem

def connectDB(dbName, collectionName):
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client[dbName]
    collection = db[collectionName]
    return client, collection

def putImage(collection, filepath):
    fs = gridfs.GridFS(collection)

    with open(filepath, 'rb') as f:
        contents = f.read()
    file = os.path.splitext(os.path.basename(filepath))[0]
    fs.put(contents, filename=file)

def queryDB(collection, query):
    return collection.find_one(query)

class dbItemListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self.setStyleSheet('font-size: 16px;')
        self.itemDoubleClicked.connect(self.getItem)

    def loadItemFromDB(self, db):
        testItems = db.find()
        self.db = db
       
        for test in testItems:
            self.addItem(test["TestId"])

    def getItem(self, lstItem):
        TestId = lstItem.text()
        selectedTest = self.db.find_one({"TestId": TestId})
        
        print(selectedTest["Well1"])
        
    
if __name__ == '__main__':
    client, testLogs = connectDB('thy_testsDB', 's2r_testlog')
    
    # print(testLog["Well1"])

    app = QApplication(sys.argv)

    demo = dbItemListWidget()
    demo.loadItemFromDB(testLogs)
    
    demo.show()

    sys.exit(app.exec_())