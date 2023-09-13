from math import sin as SIN
from math import radians as RADIANS
from math import cos as COS
from math import tan as TAN
from math import degrees as DEGREES
from math import atan2 as ATAN2
from math import asin as ASIN
from math import acos as ACOS

from var_dump import var_dump as vd

def getSunLoc(date, timePastLocalMidnight, long, lat):
    B3 = long
    B4 = lat
    B5 = 2
    B7 = 0 
    tplm = 0
    E3 = 0.5
    i = 0
    if E3 == 0.5:
        E3 = 0.5
        F3 = date + 2415018.5+E3-B5/24
        G3 = (F3-2451545)/36525
        I3 =(280.46646+G3*(36000.76983 + G3*0.0003032))%360
        J3 = 357.52911+G3*(35999.05029 - 0.0001537*G3)
        K3 =0.016708634-G3*(0.000042037+0.0000001267*G3)
        L3 =SIN(RADIANS(J3))*(1.914602-G3*(0.004817+0.000014*G3))+SIN(RADIANS(2*J3))*(0.019993-0.000101*G3)+SIN(RADIANS(3*J3))*0.000289
        M3=I3+L3
        N3=J3+L3
        O3=(1.000001018*(1-K3*K3))/(1+K3*COS(RADIANS(N3)))
        P3 = M3-0.00569-0.00478*SIN(RADIANS(125.04-1934.136*G3))
        Q3 =23+(26+((21.448-G3*(46.815+G3*(0.00059-G3*0.001813))))/60)/60
        print(Q3)
        R3=Q3+0.00256*COS(RADIANS(125.04-1934.136*G3))
        S3 =DEGREES(ATAN2(COS(RADIANS(P3)),COS(RADIANS(R3))*SIN(RADIANS(P3))))
        T3=DEGREES(ASIN(SIN(RADIANS(R3))*SIN(RADIANS(P3))))
        U3=TAN(RADIANS(R3/2))*TAN(RADIANS(R3/2))
        V3=4*DEGREES(U3*SIN(2*RADIANS(I3))-2*K3*SIN(RADIANS(J3))+4*K3*U3*SIN(RADIANS(J3))*COS(2*RADIANS(I3))-0.5*U3*U3*SIN(4*RADIANS(I3))-1.25*K3*K3*SIN(2*RADIANS(J3)))
        W3=DEGREES(ACOS((COS(RADIANS(90.833))/(COS(RADIANS(B3))*COS(RADIANS(T3)))-TAN(RADIANS(B3))*TAN(RADIANS(T3)))))
        X3=(720-4*B4-V3+B5*60)/1440
        Y3=X3-W3*4/1440
        Z3=X3+W3*4/1440
        AA3=8*W3
        AB3=(E3*1440+V3+4*B4-60*B5)%1440
  
        if (AB3/4<0):
            AC3 = AB3/4+180
   
        else:
            AC3 = AB3/4-180
   
        AD3=DEGREES(ACOS(SIN(RADIANS(B3))*SIN(RADIANS(T3))+COS(RADIANS(B3))*COS(RADIANS(T3))*COS(RADIANS(AC3))))
        AE3=90-AD3
        if (AE3>85):
            AF3= 0
   
        elif (AE3>5):
            AF3=     58.1/TAN(RADIANS(AE3))-0.07/pow(TAN(RADIANS(AE3)),3)+ 0.000086/pow(TAN(RADIANS(AE3)),5)
   
        elif (AE3>-0.575):
            AF3 = 1735+AE3*(-518.2+AE3*(103.4+AE3*(-12.79+AE3*0.711)))
   
        else: 
            AF3 = -20.772/TAN(RADIANS(AE3))
        
        AF3= AF3/3600
        AG3=AE3+AF3
 
        if (AC3>0):
            AH3 = (DEGREES(ACOS(((SIN(RADIANS(B3))*COS(RADIANS(AD3)))-SIN(RADIANS(T3)))/(COS(RADIANS(B3))*SIN(RADIANS(AD3)))))+180)%360
        else:
            AH3= (540-DEGREES(ACOS(((SIN(RADIANS(B3))*COS(RADIANS(AD3)))-SIN(RADIANS(T3)))/(COS(RADIANS(B3))*SIN(RADIANS(AD3))))))%360
        
        return {'elevation':AG3, 'azimuth':AH3}


date = 45180
timePastLocalMidnight = 0

long = 52.19355
lat = 5.28939

sunLoc = getSunLoc(date, timePastLocalMidnight, long, lat)
vd(sunLoc)