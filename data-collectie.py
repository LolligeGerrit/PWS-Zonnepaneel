import datetime
import os
import time
import random
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import var_dump as vd

###--- Write the file ---###
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

        
        values2 = []
        values2.append(start)
        for i in range(1439):
            values2.append(values2[-1] + x)
            
        vd.var_dump(values2)

        plt.plot(values2, values)
        plt.xticks(rotation=45) #rotate the x labels 45 degrees
        plt.show()
    
    return values


#this function checks if a path exists
def checkPathExistence(path):
    if os.path.exists(path):
        return True
    else:
        return False
    

#this function creates a directory
def makeDir(path):
    os.mkdir(path)
    


date = datetime.datetime.now()

#the 'r' before the string is needed to make the string a raw string, so that the backslashes are not interpreted as escape characters
filePath = r"C:\Users\Fabian\Documents\Visual studio projects\Python\reusable project\reusableProject\reusableProject\{0}\\".format(date.date())

pathExists = checkPathExistence(filePath)
print(pathExists)

if pathExists == False:
    makeDir(filePath)

testFile1 = open(filePath + "testFile.txt", "w")
testFile2 = open(filePath + "testFile2.txt", "w")

for x in range(1440):
    testFile1.write(str(random.randint(200, 300)) + "\n")
    testFile2.write(str(random.randint(200, 300)) + "\n")




testFile1.close()
testFile2.close()

###--- Read the file ---###

    
    


filePath = r"C:\Users\Fabian\Documents\Visual studio projects\Python\reusable project\reusableProject\reusableProject\{0}\\".format(date.date())
    
filePathTest1 = filePath + "testFile.txt"
readFile(filePathTest1, True)
        

#run something indefinitely every second.
'''
starttime = time.time()
running = True
while running:
    print("tick")
    print(time.time())
    
    #remove the time taken by code to execute
    time.sleep(1 - ((time.time() - starttime) % 1))
'''