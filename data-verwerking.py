from matplotlib import pyplot as plt
import numpy as np
import datetime
import os


#Function that reads a file, and plots it if 'plot' is true.
def readFile(path, plot: bool = False):
    #read the file
    file = open(path, "r")
    lines = file.readlines()
    
    values = []
    
    #save all the lines in a list
    for line in lines:
        values.append(float(line))
    
    #plot the graph if 'plot' is true
    if plot:
        x = datetime.timedelta(days=1) / len(values)
        start = datetime.datetime(2023, 1, 1, 0, 0, 0)

        
        values2 = [start]
        for i in range(len(values)-1):  #-1 because a list starts at 0, and a .txt file doesnt.
            values2.append(values2[-1] + x)
        
        plt.plot(values2, values)
        plt.xticks(rotation=30) #rotate the x labels 30 
        plt.show()
    

    return values


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