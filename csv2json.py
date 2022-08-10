import os, csv, glob
import json

from datetime import datetime

def readTestRsult(folderPath, filename):

    LysisTemp = []
    LysisTime = []
    CartTemp = []
    AdcTemp = []
    TargetName = []
    WellResult = []
    ECVolDiffs = []
    SampleId = ''

    ReactTime = []
    Well1Readings = []
    Well2Readings = []
    Well3Readings = []
    Well4Readings = []
    Well5Readings = []

    dcoument = {}

    with open(os.path.join(folderPath, filename),'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        idx = 0

        for row in plots:
            if idx == 1:
                SampleId = row[0]
            if idx == 4:
                LysisTime = row[3:]
                LysisTime = [round(float(i)/1000, 2) for i in LysisTime if i != '']
            if idx == 5:
                LysisTemp = row[3:]
                LysisTemp = [round(float(i), 2) for i in LysisTemp if i != '']
            if idx == 8:
                ReactTime = row[7:]
                ReactTime = [round(float(i)/1000, 2) for i in ReactTime if i != '']
            if idx == 9:
                CartTemp = row[7:]
                CartTemp = [round(float(i), 2) for i in CartTemp if i != '']
            if idx == 10:
                AdcTemp = row[7:]
                AdcTemp = [round(float(i), 2) for i in AdcTemp if i != '']
            if idx == 11:

                TargetName.append(row[4])
                WellResult.append(row[5])
                ECVolDiffs.append(round(float(row[6]), 2))
                Well1Readings = row[7:]
                Well1Readings = [round(float(i), 2) for i in Well1Readings if i != '']

            if idx == 12:

                TargetName.append(row[4])
                WellResult.append(row[5])
                ECVolDiffs.append(round(float(row[6]), 2))
                Well2Readings = row[7:]   
                Well2Readings = [round(float(i), 2) for i in Well2Readings if i != '']

            if idx == 13:

                TargetName.append(row[4])
                WellResult.append(row[5])
                ECVolDiffs.append(round(float(row[6]), 2))
                Well3Readings = row[7:]
                Well3Readings = [round(float(i), 2) for i in Well3Readings if i != '']

            if idx == 14:

                TargetName.append(row[4])
                WellResult.append(row[5])
                ECVolDiffs.append(round(float(row[6]), 2))
                Well4Readings = row[7:]
                Well4Readings = [round(float(i), 2) for i in Well4Readings if i != '']

            if idx == 15:

                TargetName.append(row[4])
                WellResult.append(row[5])
                ECVolDiffs.append(round(float(row[6]), 2))
                Well5Readings = row[7:]
                Well5Readings = [round(float(i), 2) for i in Well5Readings if i != '']
            
            idx += 1

    dcoument["LysisTemp"] = LysisTemp
    dcoument["LysisTime"] = LysisTime
    dcoument["CartTemp"] = CartTemp
    dcoument["AdcTemp"] = AdcTemp
    dcoument["TargetName"] = TargetName
    dcoument["WellResult"] = WellResult
    dcoument["ECVolDiffs"] = ECVolDiffs
    dcoument["SampleId"] = SampleId

    dcoument["ReactTime"] = ReactTime
    dcoument["Well1Readings"] = Well1Readings
    dcoument["Well2Readings"] = Well2Readings
    dcoument["Well3Readings"] = Well3Readings
    dcoument["Well4Readings"] = Well4Readings
    dcoument["Well5Readings"] = Well5Readings

    return dcoument


def readTestlog(filename):
    
    collection = []
    with open(filename,'r') as csvfile:
        items = csv.reader(csvfile, delimiter=',')
        idx = 0
        for row in items:
            if idx == 0:
                headers = row
                idx += 1
                continue
            #print(row)
            docItem = {}
            for idx, header in enumerate(headers):
                # if header == 'TestDate':
                #     docItem[header] = datetime.strptime(row[idx], '%m/%d/%Y').date()
                #     continue
                docItem[header] = row[idx]
            collection.append(docItem)
    return collection

def colSearch(collcection):
    idxLkUp = {}
    for i, doc in enumerate(collcection):
        idxLkUp [doc['TestId']] = i
    return idxLkUp


# Merge dict1 to dict2, update in dict2
def Merge(dict1, dict2):
    return(dict2.update(dict1))

if __name__=='__main__':
    csvfoler = os.path.join(os.path.dirname(__file__), 'dataPool')
    filenames = sorted(glob.glob(os.path.join(csvfoler, '*.csv')))
    testlogFile = "S2R_testlog.csv"
    testlogCollection = readTestlog(testlogFile)
    idxLookUp = colSearch(testlogCollection)
    jsonFile = "S2R_testlog.json"
	
    with open(jsonFile,'w') as file:

        idx = 1
        objList = []
        for filename in filenames:
            testID = os.path.splitext(os.path.basename(filename))[0]
            print(str(idx) + ":" + testID)
            idx += 1
            testDocument = testlogCollection[idxLookUp[testID]]
            resultDocument = readTestRsult(csvfoler, filename)
            Merge(resultDocument, testDocument)
            objList.append(testDocument)
            
            
        json.dump(objList, file, indent = 2)