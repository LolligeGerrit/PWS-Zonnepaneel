from math import sin as SIN
from math import radians as RADIANS
from math import cos as COS
from math import tan as TAN
from math import degrees as DEGREES
from math import atan2 as ATAN2
from math import asin as ASIN
from math import acos as ACOS
import datetime 
import julian
from var_dump import var_dump as vd

import numpy as np
from matplotlib import pyplot as plt



def getSunLoc(date, lat, long, timezone):
    julianDate = (julian.to_jd(date , fmt='jd')) #dit is de julian date, dat is het aantal dagen sinds 1 jan 
    
    timePastLocalMidnight = (date.hour + date.minute / 60) / 24
    julianDay = julianDate - timezone / 24

    julianCentury = (julianDay - 2451545) / 36525
    
    ## 280.46646 is exacte long van zon op 1 jan 2000, andere twee factoren zijn verstoring die jean meeus heeft toegevoegd
    geomMeanLongSun = (280.46646 + julianCentury * (36000.76983 + julianCentury * 0.0003032)) % 360
    geomMeanAnomSun = 357.52911 + julianCentury * (35999.05029 - 0.0001537 * julianCentury)
    
    eccentEartOrbit = 0.016708634 - julianCentury * (0.000042037 + 0.0000001267 * julianCentury)
    
    sunEqOfCrt =SIN(RADIANS(geomMeanAnomSun)) * (1.914602 - julianCentury * (0.004817 + 0.000014 * julianCentury)) + SIN(RADIANS(2 * geomMeanAnomSun)) * (0.019993 - 0.000101 * julianCentury) + SIN(RADIANS(3 * geomMeanAnomSun)) * 0.000289
    
    sunTrueLong = geomMeanLongSun + sunEqOfCrt
    
    '''
    sunTrueAnom=geomMeanAnomSun+sunEqOfCrt
    O3=(1.000001018*(1-eccentEartOrbit*eccentEartOrbit))/(1+eccentEartOrbit*COS(RADIANS(sunTrueAnom)))
    '''
    
    sunAppLong = sunTrueLong - 0.00569 - 0.00478 * SIN(RADIANS(125.04 - 1934.136 * julianCentury))
    meanObliqEcliptic = 23 + (26 + ((21.448 - julianCentury * (46.815 + julianCentury * (0.00059 - julianCentury * 0.001813)))) / 60) / 60
    obliqCorr = meanObliqEcliptic + 0.00256 * COS(RADIANS(125.04 - 1934.136 * julianCentury))
    sunRtAscent = DEGREES(ATAN2(COS(RADIANS(sunAppLong)) , COS(RADIANS(obliqCorr)) * SIN(RADIANS(sunAppLong))))
    sunDecline = DEGREES(ASIN(SIN(RADIANS(obliqCorr)) * SIN(RADIANS(sunAppLong))))
    varY = TAN(RADIANS(obliqCorr / 2)) * TAN(RADIANS(obliqCorr / 2))
    eot = 4 * DEGREES(varY * SIN(2 * RADIANS(geomMeanLongSun)) - 2 * eccentEartOrbit * SIN(RADIANS(geomMeanAnomSun)) + 4 * eccentEartOrbit * varY * SIN(RADIANS(geomMeanAnomSun)) * COS(2 * RADIANS(geomMeanLongSun)) - 0.5 * varY * varY * SIN(4 * RADIANS(geomMeanLongSun)) - 1.25 * eccentEartOrbit * eccentEartOrbit * SIN(2 * RADIANS(geomMeanAnomSun)))
    
    '''
    haSunrise=DEGREES(ACOS((COS(RADIANS(90.833))/(COS(RADIANS(lat))*COS(RADIANS(sunDecline)))-TAN(RADIANS(lat))*TAN(RADIANS(sunDecline)))))
    solarNoon=(720-4*long-eot+timezone*60)/1440
    sunriseTime=solarNoon-haSunrise*4/1440
    sunsetTime=solarNoon+haSunrise*4/1440
    sunlightDuration=8*haSunrise
    '''
    
    trueSolarTime = (timePastLocalMidnight * 1440 + eot + 4 * long - 60 * timezone) % 1440
    
    if trueSolarTime/4<0:
        hourAngle = trueSolarTime / 4 + 180
    else:
        hourAngle = trueSolarTime / 4 - 180
        solarZenithAngle = DEGREES(ACOS(SIN(RADIANS(lat)) * SIN(RADIANS(sunDecline)) + COS(RADIANS(lat)) * COS(RADIANS(sunDecline)) * COS(RADIANS(hourAngle))))
        solarElevationAngle = 90 - solarZenithAngle
        
    if solarElevationAngle > 85:
        approxAthmophericRefraction= 0  
   
    elif solarElevationAngle > 5:
        approxAthmophericRefraction = 58.1 / TAN(RADIANS(solarElevationAngle)) -0.07 / pow(TAN(RADIANS(solarElevationAngle)), 3) + 0.000086 / pow(TAN(RADIANS(solarElevationAngle)), 5)
        
    elif solarElevationAngle > -0.575:
        approxAthmophericRefraction = 1735 + solarElevationAngle * (-518.2 + solarElevationAngle * (103.4 + solarElevationAngle * (-12.79 + solarElevationAngle * 0.711)))
        
    else: 
        approxAthmophericRefraction = -20.772 / TAN(RADIANS(solarElevationAngle))
        

    approxAthmophericRefraction = approxAthmophericRefraction / 3600
    correctedSolarElevation = solarElevationAngle + approxAthmophericRefraction
 
    if hourAngle > 0:
        correctedSolarAzimuthAngle = (DEGREES(ACOS(((SIN(RADIANS(lat))*COS(RADIANS(solarZenithAngle)))-SIN(RADIANS(sunDecline)))/(COS(RADIANS(lat))*SIN(RADIANS(solarZenithAngle)))))+180)%360
    
    else:
        correctedSolarAzimuthAngle= (540-DEGREES(ACOS(((SIN(RADIANS(lat))*COS(RADIANS(solarZenithAngle)))-SIN(RADIANS(sunDecline)))/(COS(RADIANS(lat))*SIN(RADIANS(solarZenithAngle))))))%360


    return {'elevationAngle' : correctedSolarElevation, 'azimuthAngle' : correctedSolarAzimuthAngle}




date = datetime.datetime(year=2023, month= 9 , day= 11, hour=8, minute=30)


lat = 52.19355
long = 5.28939
timezone = 2

sunLoc = getSunLoc(date, lat, long, timezone)
vd(sunLoc)

#Matplotlib plot
'''
amountOfDays = 3
dayValues = []
dayValues2 = []
npValues = np.arange(0, 1440 * amountOfDays, 1)

for x in range(1440 * amountOfDays):
    sunLoc = getSunLoc(date, lat, long, timezone)
    date += datetime.timedelta(minutes=1)
    dayValues.append(sunLoc['elevationAngle'])
    dayValues2.append(sunLoc['azimuthAngle'])
    
plt.plot(npValues, dayValues)
plt.plot(npValues, dayValues2)

plt.show()
'''

