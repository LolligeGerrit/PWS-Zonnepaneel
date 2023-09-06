import datetime
import math as m
from var_dump import var_dump as vd
import time
import pytz


import matplotlib.pyplot as plt
import numpy as np


#//--Functions--\\#

#Functie die de declinatonAngle returned.
def getDeclinantionAngle(date:datetime.datetime):

    onlyDate = datetime.date(date.year, date.month, date.day)
    #get the days since 1-1-2000
    firstJanuary2000 = datetime.date(2000, 1, 1)


    dElapsedJulianDays = onlyDate - firstJanuary2000
    dElapsedJulianDays = dElapsedJulianDays.days

    ##--THE FOLLOWING CODE IS THE PSA ALGORITHM. THIS IS NOT MY CODE--##
    dOmega=2.1429-0.0010394594*dElapsedJulianDays
    dMeanLongitude = 4.8950630+ 0.017202791698*dElapsedJulianDays
    dMeanAnomaly = 6.2400600+ 0.0172019699*dElapsedJulianDays
    dEclipticLongitude = dMeanLongitude + 0.03341607*m.sin(dMeanAnomaly) + 0.00034894*m.sin(2*dMeanAnomaly)-0.0001134 -0.0000203*m.sin(dOmega)
    dEclipticObliquity = 0.4090928 - 6.2140e-9*dElapsedJulianDays +0.0000396*m.cos(dOmega)
    dSin_EclipticLongitude= m.sin(dEclipticLongitude)
    dY = m.cos(dEclipticObliquity) * dSin_EclipticLongitude
    dX = m.cos(dEclipticLongitude)
    dRightAscension = m.atan2( dY,dX ); 
    if( dRightAscension < 0.0 ):
        dRightAscension += m.pi*2
    dDeclination = m.asin(m.sin(dEclipticObliquity)*dSin_EclipticLongitude)
    return(m.degrees(dDeclination))


#Deze functie is momenteel niet in gebruik, maar berekent de accurateTimeZone
def getAccurateTimezone(long: float): #DEZE MAG WEG
    return(long * 4)/60


#deze functie berekent de localSolarTime en retuerned deze. Dit is een Float tussen -180 en 180.
def getLocalSolarTime(long: float, timezone: float | int, date: datetime.datetime, dayOfTheYear:int):
    greenwhichTime = date - datetime.timedelta(hours=timezone)
    correction = long * 4
    
    B = 360/365 * (dayOfTheYear - 81)
    equationOfTime = 9.87 * m.sin(m.radians(2 * B)) - 7.53 * m.cos(m.radians(B)) - 1.5 * m.sin(m.radians(B))
    
    localSolarTime = greenwhichTime + datetime.timedelta(minutes=correction) + datetime.timedelta(minutes=equationOfTime)
    
    localSolarTimeFloat = localSolarTime.hour*60 + localSolarTime.minute

    return(localSolarTimeFloat)




#Functie die een dictionary returned met daarin de elevationAngle en de azimuth. Als de includeInfo boolean True is zit er ook date, dayOfTheYear, declinationAngle, localSolarTime en localHourAngle in.
def getSunLocation(lat: float, long :float, timezone: float | int, date: datetime.datetime, time: list, daylightSavingTime: bool, includeInfo: bool = False):
    
    dayOfTheYear = date.timetuple().tm_yday
    declinationAngle = getDeclinantionAngle(date)
    localSolarTime = getLocalSolarTime(long, timezone, date, dayOfTheYear)
    localHourAngle = 15/60 * (localSolarTime - 12*60)
    #print("localHourAngle: " + str(localHourAngle), end="   |   ")
    elevationAngle = m.degrees(m.asin(m.sin(m.radians(declinationAngle)) * m.sin(m.radians(lat)) + m.cos(m.radians(declinationAngle)) * m.cos(m.radians(lat)) * m.cos(m.radians(localHourAngle))))


    #####print("DeclinationAngle: {0}\nLat: {1}\nElevationAngle: {2}".format(m.radians(declinationAngle), m.radians(lat), m.radians(elevationAngle)))
    #print(str(date) + "  |   " + str(round((m.sin(m.radians(declinationAngle)) * m.cos(m.radians(lat)) - m.cos(m.radians(declinationAngle)) * m.sin(m.radians(lat)) * m.cos(m.radians(localHourAngle))) / m.cos(m.radians(elevationAngle)),13)),end="   |   \n")
            #values.append((m.sin(m.radians(declinationAngle)) * m.cos(m.radians(lat)) - m.cos(m.radians(declinationAngle)) * m.sin(m.radians(lat)) * m.cos(m.radians(localHourAngle))) / m.cos(m.radians(elevationAngle)))

    print(str(date) + "  |  " + str(elevationAngle) + "  |  ")
    #print(localHourAngle)
    if localHourAngle < 0:
        #print("if", end="   |   ")
        
        x = round((m.sin(m.radians(declinationAngle)) * m.cos(m.radians(lat)) - m.cos(m.radians(declinationAngle)) * m.sin(m.radians(lat)) * m.cos(m.radians(localHourAngle))) / m.cos(m.radians(elevationAngle)),13)
        azimuth = m.degrees(m.acos(x))
        #the acos doesnt accept values under -1 and above 1
    elif localHourAngle >= 0:
        #print("elif", end="    |    ")
        
        x = round((m.sin(m.radians(declinationAngle)) * m.cos(m.radians(lat)) - m.cos(m.radians(declinationAngle)) * m.sin(m.radians(lat)) * m.cos(m.radians(localHourAngle))) / m.cos(m.radians(elevationAngle)),13)
        azimuth = 360 - m.degrees(m.acos(x))

    returnDict = {'elevationAngle':elevationAngle, 'azimuth':azimuth}
    
    if includeInfo:
        returnDict.update({'date': date, 'dayOfTheYear': dayOfTheYear, 'declinationAngle':declinationAngle, 'localSolarTime': localSolarTime, 'localHourAngle': localHourAngle})
        
    return(returnDict)
    

#Bereken het verschil tussen twee getSunLocation() dictionaries. Returns een dinctionary met de verschillen
def getSunLocDelta(sunLoc1, sunLoc2):
    deltaDict = {}
    for x in sunLoc:
        delta = abs(sunLoc1[x] - sunLoc2[x])
        deltaDict[x] = delta
    return deltaDict
    

#kijkt of DST geldt. Returned True of False
def checkDaylightSavingTime(date: datetime.datetime):
    dstTest = date.astimezone(pytz.timezone('Europe/Amsterdam'))

    if dstTest.dst() == datetime.timedelta(hours=1):
        return True
    else:
        return False



#//--input--\\#
lat = 52.23629
long = 5.21295

timezone = 1 #+ or -, keep in mind that in the summer our clock goes forward so the timezone in the Netherlands changes from +1 to +2

date = datetime.datetime(year=2023, month=9, day=11, hour=1, minute=0, second=0)
#--End of input--#


daylightSavingTime = checkDaylightSavingTime(date)

if daylightSavingTime:
    date -= datetime.timedelta(hours=1)



#voor elke maand, print een waarde. in dit geval sunLoc (binnen de vd())
'''
for x in range(12):
    print("##### {0} #####".format(date))
    sunLoc = getSunLocation(lat, long, timezone, date, time, daylightSavingTime, True)
    vd(sunLoc)
    try:
        date = date.replace(month=date.month + 1)
    except:
        pass
'''


#voor elke dag, print een waarde. in dit geval azimuth (binnen de vd())
'''
for x in range(365):
    
    try:
        sunLoc = getSunLocation(lat, long, timezone, date, time, daylightSavingTime, True)
        print(sunLoc["azimuth"])
        print("success")
    except:
        print("math domain error")
        exit("math error")

    date += datetime.timedelta(days=1)
    daylightSavingTime = checkDaylightSavingTime(date)
'''

#Krijg een enkele waarde op een moment

sunLoc = getSunLocation(lat, long, getAccurateTimezone(long), date, time, daylightSavingTime, True)   

vd(sunLoc)



#voor elke minuut in de dag (24 uur vanaf de tijd), pak een variable om te plotten.
'''
dayValues = []
valueToGet = "localSolarTime" #PAS DIT AAN ALS JE IETS ANDERS WIL PLOTTEN

#elevationAngle | azimuth ||||| date | DayOfTheYear | declinationAngle | localSolarTime | localHourAngle


for x in range(1440):
    try:    
        sunLoc = getSunLocation(lat, long, timezone, date, time, daylightSavingTime, True)
        dayValues.append(sunLoc[valueToGet])
        
    except:
        print("error")  
        dayValues.append(0)
    
    date += datetime.timedelta(minutes=1)



xpoints = np.arange(0, 1440, 1)
ypoints = np.array(dayValues)

plt.plot(xpoints, ypoints)
plt.xlabel("Minuten van de dag")
plt.ylabel(valueToGet + " waardes")
plt.title(valueToGet)
plt.show()
'''



'''
fig, axs = plt.subplots(2)
fig.suptitle(str(date.time()))
axs[0].set_title("Originele waardes")
axs[1].set_title("Genormalizeerde waardes",pad=-20)
axs[0].plot(xpoints, ypoints)
axs[1].plot(xpoints, valuesNormalized)
plt.show()
'''





##//ALLE CODE HIERONDER GEBRUIKEN WE NIET\\##

#de outde normalisatie functie (gebruiken we NIET)
''' Normalization (has to go)
valuesNp = np.array(values)
valuesNormalized = 2 * ((valuesNp - min(valuesNp)) / (max(valuesNp) - min(valuesNp))) - 1
'''


#de oude getLocalSolarTime functie (hoeven we niet meer te gebruiken)
'''
def getLocalSolarTime(long: float, dayOfTheYear: int, timezone: float | int, date: datetime.datetime):
    B = 360/365 * (dayOfTheYear - 81)
    equationOfTime = 9.87 * m.sin(m.radians(2 * B)) - 7.53 * m.cos(m.radians(B)) - 1.5 * m.sin(m.radians(B))
    localStandardTimeMeridian = 15 * timezone
    timeCorrectionFactor = 4 * (long - localStandardTimeMeridian) + equationOfTime
    localSolarTime = (date.hour*60 + date.minute) + (timeCorrectionFactor/60)
    vd(localSolarTime)
    return(localSolarTime)
'''


'''
important notes


daylight savings time is active in The Netherlands between:
Mar 26, 2023
Oct 29, 2023

less changes
even more changes

'''
