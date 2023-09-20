import datetime
import os
import random
import time
from var_dump import var_dump as vd


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