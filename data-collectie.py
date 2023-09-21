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
filePath = r"C:\Users\Fabian\Documents\Visual studio projects\Python\reusable project\reusableProject\reusableProject\{0}\\".format("Data")

#filePath = r"D:\profy_progreumeur\Python\New folder\jemoeder\jemoeder\{0}\\".format("Data") #Fap's pc


pathExists = checkPathExistence(filePath)

if pathExists == False:
    makeDir(filePath)

setup1 = open(filePath + "setup1.txt", "w")
setup2 = open(filePath + "setup2.txt", "w")
setup3 = open(filePath + "setup3.txt", "w")
setup4 = open(filePath + "setup4.txt", "w")


#this is only for testing purposes
for x in range(1440):
    date += datetime.timedelta(minutes=1)
    setup1.write(str(str(date) + "," + str(random.randint(200, 300))) + "\n")
    setup2.write(str(str(date) + "," + str(random.randint(200, 300))) + "\n")
    setup3.write(str(str(date) + "," + str(random.randint(200, 300))) + "\n")
    setup4.write(str(str(date) + "," + str(random.randint(200, 300))) + "\n")


setup1.close()
setup2.close()
setup3.close()
setup4.close()




        

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