from matplotlib import pyplot as plt
from matplotlib import ticker
import numpy as np
import datetime

import os
from var_dump import var_dump as vd


#Function that reads a file, and plots it if 'plot' is true.
def readFile(path, plot: bool = False):
    #read the file
    file = open(path, "r")
    lines = file.readlines()
    
    powerValues = []
    timeValues = []
    
    #save all the lines in a list
    for line in lines:
        splitLine = line.split(",")
        timeValues.append(datetime.datetime.strptime(splitLine[0], "%Y-%m-%d %H:%M:%S.%f"))
        powerValues.append(float(splitLine[1]))
        
    
    
    #plot the graph if 'plot' is true
    if plot:
        
        fix, ax = plt.subplots()
        ax.plot(timeValues, powerValues)
        plt.xticks(rotation=30) #rotate the x labels 30 
        ax.xaxis.set_major_locator(ticker.LinearLocator())
        
        
        plt.show()
    

    return {'timeValues': timeValues, 'powerValues': powerValues}


#this function checks if a path exists
def checkPathExistence(path):
    if os.path.exists(path):
        return True
    else:
        return False



###--- Read the file ---###
date = datetime.date(2023, 9, 20)


if checkPathExistence(str(date)):
    print("Files found for {0}, reading files now.".format(str(date)))


    filePath = r"C:\Users\Fabian\Documents\Visual studio projects\Python\reusable project\reusableProject\reusableProject\{0}\\".format(str(date))
    setup1 = filePath + "setup1.txt"
    readFile(setup1, True)
    
else:
    print("Files not found, please run dataCollection.py first.")