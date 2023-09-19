from math import sin
from math import radians
from math import cos
from math import tan
from math import degrees
from math import atan2
from math import asin
from math import acos


import datetime 
import julian
from var_dump import var_dump as vd

#Nessacary for plotting
import numpy as np
from matplotlib import pyplot as plt



def getSunLoc(date :datetime.datetime, lat : float, long : float, timezone :int, includeInfo: bool):
    returnDict = {}
    julianDate = (julian.to_jd(date , fmt='jd')) #dit is de julian date, dat is het aantal dagen sinds 1 jan 
    
    timePastLocalMidnight = (date.hour + date.minute / 60) / 24
    julianDay = julianDate - timezone / 24

    julianCentury = (julianDay - 2451545) / 36525
    
    ## 280.46646 is exacte long van zon op 1 jan 2000, andere twee factoren zijn verstoring die jean meeus heeft toegevoegd
    geomMeanLongSun = (280.46646 + julianCentury * (36000.76983 + julianCentury * 0.0003032)) % 360
    geomMeanAnomSun = 357.52911 + julianCentury * (35999.05029 - 0.0001537 * julianCentury)
    
    eccentEartOrbit = 0.016708634 - julianCentury * (0.000042037 + 0.0000001267 * julianCentury)
    
    sunEqOfCrt = sin(radians(geomMeanAnomSun)) * (1.914602 - julianCentury * (0.004817 + 0.000014 * julianCentury)) + sin(radians(2 * geomMeanAnomSun)) * (0.019993 - 0.000101 * julianCentury) + sin(radians(3 * geomMeanAnomSun)) * 0.000289
    
    sunTrueLong = geomMeanLongSun + sunEqOfCrt
    
    
    sunAppLong = sunTrueLong - 0.00569 - 0.00478 * sin(radians(125.04 - 1934.136 * julianCentury))
    meanObliqEcliptic = 23 + (26 + ((21.448 - julianCentury * (46.815 + julianCentury * (0.00059 - julianCentury * 0.001813)))) / 60) / 60
    obliqCorr = meanObliqEcliptic + 0.00256 * cos(radians(125.04 - 1934.136 * julianCentury))
    sunRtAscent = degrees(atan2(cos(radians(sunAppLong)) , cos(radians(obliqCorr)) * sin(radians(sunAppLong))))
    sunDecline = degrees(asin(sin(radians(obliqCorr)) * sin(radians(sunAppLong))))
    varY = tan(radians(obliqCorr / 2)) * tan(radians(obliqCorr / 2))
    eot = 4 * degrees(varY * sin(2 * radians(geomMeanLongSun)) - 2 * eccentEartOrbit * sin(radians(geomMeanAnomSun)) + 4 * eccentEartOrbit * varY * sin(radians(geomMeanAnomSun)) * cos(2 * radians(geomMeanLongSun)) - 0.5 * varY * varY * sin(4 * radians(geomMeanLongSun)) - 1.25 * eccentEartOrbit * eccentEartOrbit * sin(2 * radians(geomMeanAnomSun)))
    
    
    
    
    trueSolarTime = (timePastLocalMidnight * 1440 + eot + 4 * long - 60 * timezone) % 1440
    
    if trueSolarTime/4<0:
        hourAngle = trueSolarTime / 4 + 180
    else:
        hourAngle = trueSolarTime / 4 - 180
        solarZenithAngle = degrees(acos(sin(radians(lat)) * sin(radians(sunDecline)) + cos(radians(lat)) * cos(radians(sunDecline)) * cos(radians(hourAngle))))
        solarElevationAngle = 90 - solarZenithAngle
        
    if solarElevationAngle > 85:
        approxAthmophericRefraction= 0  
   
    elif solarElevationAngle > 5:
        approxAthmophericRefraction = 58.1 / tan(radians(solarElevationAngle)) -0.07 / tan(radians(solarElevationAngle)) ** 3 + 0.000086 / tan(radians(solarElevationAngle)) ** 5
        
    elif solarElevationAngle > -0.575:
        approxAthmophericRefraction = 1735 + solarElevationAngle * (-518.2 + solarElevationAngle * (103.4 + solarElevationAngle * (-12.79 + solarElevationAngle * 0.711)))
        
    else: 
        approxAthmophericRefraction = -20.772 / tan(radians(solarElevationAngle))
        

    approxAthmophericRefraction = approxAthmophericRefraction / 3600
    correctedSolarElevation = solarElevationAngle + approxAthmophericRefraction
 
    if hourAngle > 0:
        correctedSolarAzimuthAngle = (degrees(acos(((sin(radians(lat))*cos(radians(solarZenithAngle)))-sin(radians(sunDecline)))/(cos(radians(lat))*sin(radians(solarZenithAngle)))))+180)%360
    
    else:
        correctedSolarAzimuthAngle= (540-degrees(acos(((sin(radians(lat))*cos(radians(solarZenithAngle)))-sin(radians(sunDecline)))/(cos(radians(lat))*sin(radians(solarZenithAngle))))))%360


    
    if includeInfo:
        haSunrise=degrees(acos((cos(radians(90.833))/(cos(radians(lat))*cos(radians(sunDecline)))-tan(radians(lat))*tan(radians(sunDecline)))))
        solarNoon=(720-4*long-eot+timezone*60)/1440
        sunriseTime=solarNoon-haSunrise*4/1440
        sunsetTime=solarNoon+haSunrise*4/1440
        sunlightDuration=8*haSunrise
        
        returnDict.update({"sunriseTime" : sunriseTime, "sunsetTime" : sunsetTime, "sunlightDuration" : sunlightDuration, "solarNoon":solarNoon})
    
    returnDict.update({'elevationAngle' : correctedSolarElevation, 'azimuthAngle' : correctedSolarAzimuthAngle})
    
    return returnDict


def getSeasonAngle(date, lat, long, timezone):
    date = date.replace(hour=12, minute=0, second=0)
    data = getSunLoc(date, lat, long, timezone, True)
    solarNoon = data['solarNoon']

    date = date.replace(hour=0, minute=0, second=0)
    date += datetime.timedelta(minutes=solarNoon*1440)
    seasonAngle = getSunLoc(date, lat, long, timezone, False)
    return seasonAngle['elevationAngle']


##// Input \\##
date = datetime.datetime(year=2023, month=1, day= 1, hour=12, minute=0)

lat = 52.19355
long = 5.28939
timezone = 2

##// End of input \\##


sunLoc = getSunLoc(date, lat, long, timezone, True)
vd(sunLoc)

print(getSeasonAngle(date, lat, long, timezone))


#Matplotlib plot
amountOfDays = 3
dayElevation = []
dayAzimuth = []
daySeasonAngle = []
npValues = np.arange(0, 24 * amountOfDays, 1)


#fill dayElevation and dayAzimuth with data
for x in range(24* amountOfDays):
    sunLoc = getSunLoc(date, lat, long, timezone, False)
    date += datetime.timedelta(hours=1)
    dayElevation.append(sunLoc['elevationAngle'])
    dayAzimuth.append(sunLoc['azimuthAngle'])
    daySeasonAngle.append(getSeasonAngle(date, lat, long, timezone))


fig, axs = plt.subplots(3)
fig.suptitle('Azimuth and Elevation Angle')

#plot data
axs[0].plot(npValues, dayAzimuth, color='orange')
axs[1].plot(npValues, dayElevation)
axs[2].plot(npValues, daySeasonAngle, color='green')

#set subplot titles
axs[0].set_title('Azimuth Angle')
axs[1].set_title('Elevation Angle')
axs[2].set_title('Season Angle')

fig.subplots_adjust(hspace=.5) #space between plots

plt.show()