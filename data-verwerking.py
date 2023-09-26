from matplotlib import pyplot as plt
from matplotlib import ticker
from matplotlib import dates as mdates
import numpy as np
import datetime

import os
from var_dump import var_dump as vd


# Function that reads a file, and plots it if 'plot' is true.
def readFile(path, plot: bool = False, startDate: datetime.datetime = datetime.datetime(1, 1, 1, 0, 0, 0), endDate: datetime.datetime = datetime.datetime.now()):
    # read the file
    file = open(path, "r")
    lines = file.readlines()

    powerValues = []
    timeValues = []

    # save all the lines in a list

    for line in lines:

        splitLine = line.split(",")
        if startDate <= datetime.datetime.strptime(splitLine[0], "%Y-%m-%d %H:%M:%S.%f") <= endDate:
            timeValues.append(datetime.datetime.strptime(splitLine[0], "%Y-%m-%d %H:%M:%S.%f"))
            powerValues.append(float(splitLine[1]))

    # plot the graph if 'plot' is true
    if plot:
        fix, ax = plt.subplots()
        ax.plot(timeValues, powerValues)

        ##--Plot formatting--##

        plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right")  # rotate the tickers and make sure the placement is correct.
        ax.xaxis.set_major_locator(ticker.LinearLocator())  # make sure the tickers are equally spaced
        xfmt = mdates.DateFormatter('%d-%m-%y %H:%M')  # format the xaxis tickers to a nice day and time format
        ax.xaxis.set_major_formatter(xfmt)  # apply the formatter from previous line
        plt.margins(x=0.01)  # remove the whitespaces on the xaxis

        ##--End of plot formatting--##

        plt.show()

    return {'timeValues': timeValues, 'powerValues': powerValues}


# this function checks if a path exists
def checkPathExistence(path):
    if os.path.exists(path):
        return True
    else:
        return False


###--- Read the file ---###
filePath = r"C:\Users\Fabian\Documents\Visual studio projects\Python\reusable project\reusableProject\reusableProject\{0}\\".format("Data")  # Fap's laptop
# filePath = r"D:\profy_progreumeur\Python\New folder\jemoeder\jemoeder\{0}\\".format("Data") #Fap's pc

if checkPathExistence(filePath):
    print("Files found for {0}, reading files now.")

    setup1 = filePath + "setup1.txt"
    readFile(setup1, True, startDate=datetime.datetime(23, 9, 21, 0, 0, 0), endDate=datetime.datetime(2023, 9, 22, 0, 0, 0))


else:
    print("Files not found, please run dataCollection.py first.")
