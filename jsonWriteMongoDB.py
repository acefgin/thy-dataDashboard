import pymongo
import json
from json import JSONDecoder
from functools import partial

def json_parse(fileobj, decoder=JSONDecoder(), buffersize=2048):
    buffer = ''
    for chunk in iter(partial(fileobj.read, buffersize), ''):
         buffer += chunk
         while buffer:
             try:
                 result, index = decoder.raw_decode(buffer)
                 yield result
                 buffer = buffer[index:].lstrip()
             except ValueError:
                 # Not enough data to decode, read more
                 break

from pprint import pprint
from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['mytest_db']
collection = db['mytest_collection']
requesting = []

with open(r'sample.json') as f:
    myDicts = json.load(f)
    # print(type(myDicts))
    for myDict in myDicts:
        requesting.append(InsertOne(myDict))
    print(requesting)

result = collection.bulk_write(requesting)
client.close()