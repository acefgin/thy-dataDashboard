import pymongo
import json
from pymongo import MongoClient, InsertOne

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['Thy-testDB']
collection = db.S2R_testlog
requesting = []

with open(r"S2R_testlog.json") as f:
    for jsonObj in f:
        # print(jsonObj)
        myDict = json.loads(jsonObj)
        # requesting.append(InsertOne(myDict))

# result = collection.bulk_write(requesting)
client.close()