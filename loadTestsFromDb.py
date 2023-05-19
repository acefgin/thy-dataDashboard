import subprocess, sys
import os, glob

from csv2json import *
from jsonWriteMongoDB import *

def fileSplitter(filename, devicePrefix, savePath):
    headers = []
    testInfos = []
    lysisData = []
    detectData = []

    with open(filename,'r') as multiTests:
        rows = csv.reader(multiTests, delimiter=',')
        status = 0
        invalidSet = set()
        headerDist = {}
        splitPrapFlag = False

        for row in rows:
            if not splitPrapFlag:
                for n, header in enumerate(row):
                    headerDist[header] = n
                splitPrapFlag = True
                print(headerDist)

            if len(row) == 0:
                status += 1
            elif row[0] == 'SampleId':
                headers.append(row)
                continue
            elif status == 0:
                if row[headerDist["OverallResult"]] == 'Unspecified':
                    invalidSet.add(row[headerDist["RunId"]])
                    continue
                testInfos.append(row)
            elif status == 1:
                if row[1] in invalidSet:
                    continue
                lysisData.append(row)
            elif status == 2:
                if row[1] in invalidSet:
                    continue
                detectData.append(row)

        for testNum in range(len(testInfos)):

            newFile = os.path.join(savePath, '{}_{}-{}-{}.csv'.format( \
                devicePrefix, testInfos[testNum][headerDist["RunId"]], \
                testInfos[testNum][headerDist["Barcode"]], \
                testInfos[testNum][headerDist["SampleId"]]))
            if os.path.isfile(newFile):
                continue
            with open(newFile,'w', newline = '') as slgTest:
                writer = csv.writer(slgTest)
                writer.writerow(headers[0])
                writer.writerow(testInfos[testNum])
                writer.writerow('\n')
                writer.writerow(headers[1])

                for i in range(2):
                    writer.writerow(lysisData[2 * testNum + i])
                writer.writerow('\n')
                writer.writerow(headers[2])
                for i in range(8):
                    writer.writerow(detectData[8 * testNum + i])



if __name__=='__main__':
    
    # dbFilePath = sys.argv[1]
    # cwd = os.path.dirname(dbFilePath)
    # cmd_str = f'.\\rET.exe {dbFilePath}'
    # print(cmd_str)
    # subprocess.run(cmd_str, shell=True)
    
    # fileList = sorted(glob.glob(os.path.join(cwd, '*.csv')))
    # filePath = fileList[0]
    
    # deviceNum = '001'
    # csvName = os.path.splitext(os.path.basename(filePath))[0]
    # nameTxt = csvName.split("_")
    # devicePrefix = 'NABITA{}'.format(deviceNum)
    # datetimePrefix = '{}'.format(nameTxt[1])
    
    # resultFolder = '{}_{}'.format(devicePrefix, datetimePrefix)
    # savePath = os.path.join(cwd, resultFolder)
    # if not os.path.isdir(savePath):
    #     os.mkdir(savePath)
    
    # fileSplitter(filePath, devicePrefix, savePath)
    savePath = 'C:\SynologyDrive\\repos\\Thy-resultDashboard\\NABITA001_202305191551'
    
    filenames = sorted(glob.glob(os.path.join(savePath, '*.csv')))
    
    # testlogFile = "S2R_testlog.csv"
    # testlogCollection = readTestlog(testlogFile)
    # idxLookUp = colSearch(testlogCollection)
    jsonFile = "test.json"
	
    with open(jsonFile,'w') as file:

        idx = 1
        objList = []
        for filename in filenames:
            testID = os.path.splitext(os.path.basename(filename))[0]
            print(str(idx) + ":" + testID)
            idx += 1
            # testDocument = testlogCollection[idxLookUp[testID]]
            resultDocument = readTestRsult(savePath, filename)
            # Merge(resultDocument, testDocument)
            # objList.append(testDocument)
            objList.append(resultDocument)
            
            
        json.dump(objList, file, indent = 2)
    writeMongoDB(jsonFile)

    


