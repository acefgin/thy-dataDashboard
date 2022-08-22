import pymongo
import sys
import numpy as np
from PyQt5 import QtCore, QtWidgets # import PyQt5 before matplotlib
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

matplotlib.use("Qt5Agg")

def connectDB(dbName, collectionName):
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client[dbName]
    collection = db[collectionName]
    return client, collection

def queryDB(collection, query):
    return collection.find_one(query)

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=24, height=6, dpi=40):
        fig = Figure(figsize=(width, height), dpi=dpi)
        #Tight layout
        fig.tight_layout()
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class dbPlotWidget(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(dbPlotWidget, self).__init__(parent)
        self.canvas = MplCanvas(self, width=24, height=6, dpi=40)
        plt.style.use('seaborn-bright')
        plt.rc('axes', linewidth=2)
        font = {'weight' : 'bold', 'size' : 21}
        plt.rc('font', **font)
        toolbar = NavigationToolbar(self.canvas, self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        # Create a placeholder widget to hold our toolbar and canvas.
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setLayout(layout)
        # self.scene = QtWidgets.QGraphicsScene(self.centralwidget)
        # self.setScene(self.scene)
        # self.show()
        self.curvesList = []

    def curvesPlot(self, testLog):
        print("run")
        self.curvesList = []
        self.canvas.axes.cla()
        CHANNELNUM = 5
        time = testLog['ReactTime']
        targetName = testLog['TargetName']
        testId = testLog['TestId']
        input = testLog['Input']
        reactDataNameLs = ['Well1Readings','Well2Readings','Well3Readings','Well4Readings','Well5Readings']
        PD1, PD2, PD3, PD4, PD5 = [], [], [], [], []
        chList = [PD1, PD2, PD3, PD4, PD5]
        smoothedSignals = []
        for i in range(CHANNELNUM):
            chList[i] = testLog[reactDataNameLs[i]]
            smoothedSignals.append(self.smooth(np.array(chList[i])))

        featList = np.zeros((5,4))
        lnColorLs = ['r', '#35ff35', '#3535ff', '#35ffff', '#ff35ff']
        for i in range(CHANNELNUM):
            _, diff, cp, stepWidth, avgRate= self.labelSteps(smoothedSignals[i])
            if diff == 0 and len(smoothedSignals[i]) >= 50:
                diff = round(self.consecutiveSum(np.diff(smoothedSignals[i]), 50), 1)
            featList[i] = [diff, cp, stepWidth, avgRate]
            ln = self.plot(time, chList[i], targetName[i], lnColorLs[i])
            # print(ln)
            self.curvesList.append(ln)

        # Add Title
        title = '{}_{}'.format(testId, input)
        self.canvas.axes.set_title(title, color='k', fontsize = 21, fontweight = 'bold')
        # Add Axis Labels
        
        self.canvas.axes.set_ylabel("SensorRead (mvs)", fontsize = 21, fontweight = 'bold')
        self.canvas.axes.set_xlabel("Time (secs)", fontsize = 21, fontweight = 'bold')
        
        #Add grid
        self.canvas.axes.grid(linestyle = '-.')
        #Add legend
        legend = self.canvas.axes.legend(loc='upper right',  ncol=5)
        
        #Set tickers
        self.canvas.axes.xaxis.set_major_locator(MultipleLocator(200))
        self.canvas.axes.xaxis.set_major_formatter('{x:.0f}')
        self.canvas.axes.xaxis.set_minor_locator(MultipleLocator(100))

        self.canvas.axes.yaxis.set_major_locator(MultipleLocator(100))
        self.canvas.axes.yaxis.set_major_formatter('{x:.0f}')
        self.canvas.axes.yaxis.set_minor_locator(MultipleLocator(50))
        #Set Range
        self.canvas.axes.set_xlim(0, 1800)
        self.canvas.axes.set_ylim(0, 600)

        self.canvas.draw()
        return featList
        
    def plot(self, x, y, plotname, color):
        ln, = self.canvas.axes.plot(x, y, color = color, linewidth = 2, label = plotname)
        print(ln)
        return ln
    
    def toggleCurve(self, status, index):
        if status:
            self.curvesList[index].set_alpha(1)
        else:
            self.curvesList[index].set_alpha(0)
        
        self.canvas.draw()

    def smooth(self, x,window_len=10,window='hanning'):

        if x.ndim != 1:
            raise ValueError("smooth only accepts 1 dimension arrays.")

        if x.size < window_len:
            raise ValueError("Input vector needs to be bigger than window size.")


        if window_len<3:
            return x


        if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
            raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")


        s = np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
        #print(len(s))
        if window == 'flat': #moving average
            w = np.ones(window_len,'d')
        else:
            w = eval('np.'+window+'(window_len)')

        y = np.convolve(w/w.sum(),s,mode='valid')
        return np.round(y, decimals = 3)

    def consecutiveSum(self, arr, window_len):
        if arr.ndim != 1:
            raise ValueError("smooth only accepts 1 dimension arrays.")

        arrSize = arr.size

        if arrSize < window_len:
            length = arrSize
        length = window_len
        maxSum = np.float64(1.0)
        for i in range(length):
            maxSum += arr[i]
        windowSum = maxSum
        for i in range(length,arrSize):
            windowSum += arr[i] - arr[i - length]
            maxSum = np.maximum(maxSum, windowSum)
        return maxSum

    def labelSteps(self, datas, startPt = 30, rateTh = 0.3, width_LB = 15, avgRate_LB = 0.8):
        
        #if len(datas) >= 10:
        #	datas = smooth(datas)
        dataDiffs = np.diff(datas)

        listOfSteps = []
        inStep = False
        stepL = 0
        stepR = 0
        
        for cnt, diff in enumerate(dataDiffs):
            if cnt < startPt:
                continue
            if not inStep and diff >= rateTh:
                stepL = cnt
                inStep = True
                continue
            if inStep and (diff < rateTh or (cnt == len(dataDiffs) - 1)):
                stepR = cnt
                inStep = False
                LAMPStepFL = False
                stepDiff = 0
                if (stepR - stepL) >= width_LB:
                    index = stepL
                    while index <= stepR:
                        stepDiff = stepDiff + dataDiffs[index]
                        index += 1
                    #print(stepDiff, stepR, stepL)
                    avgRate = stepDiff / (stepR - stepL + 1)
                    #print(avgRate)
                    LAMPStepFL = avgRate >= avgRate_LB
                step = [stepL, stepR, LAMPStepFL]
                stepL = cnt + 1
                listOfSteps.append(step)
                continue
        #print(listOfSteps)
        stepDiff = 0
        cp = 0
        maxDiff = 0
        maxIndex = 0
        stepWidth = 0
        for step in listOfSteps:
            if step[-1]:
                index = step[0] - 1
                stepWidth += step[1] - step[0] + 1

                # Accumulate signal increase of all Ture step as Step Diff
                while index < step[1] + 1:
                    stepDiff = stepDiff + dataDiffs[index]
                    # Capture time for highest diff as Cp
                    if dataDiffs[index] >= maxDiff:
                        maxDiff = dataDiffs[index]
                        maxIndex = index
                    index += 1
                if len(datas) > 10: cp = (maxIndex - datas[maxIndex + 1] / dataDiffs[maxIndex]) * 10 / 60 - 5
        avgRate = 0
        if stepWidth != 0: avgRate = stepDiff/stepWidth
        
        return listOfSteps, round(stepDiff, 1), round(cp, 1), round(stepWidth, 1), round(avgRate, 1)

def main():
    app = QtWidgets.QApplication(sys.argv)
    client, testLogs = connectDB('thy_testsDB', 's2r_testlog')
    testLog = queryDB(testLogs, {"TestId": "2022-06-22_NABITA010.10_3"})
    client.close()
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setGeometry(200, 200, 1280, 360)

    graphW = dbPlotWidget()
    MainWindow.setCentralWidget(graphW.centralwidget)

    
    graphW.curvesPlot(testLog)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()