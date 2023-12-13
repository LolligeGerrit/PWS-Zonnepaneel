import time
import RPi.GPIO as GPIO
from datetime import date

switch1On = False
switch3On = False
motorAngle = 90





def turnTenDegrees():
    switchOn(2, True)
    time.sleep(0.01)
    switchOn(2, False)



def turnMotor(angle: int):
    global motorAngle

    if angle < 0:
        switchFlow()
        #motor turns 540degrees/second

        #in 2/3 seconds draaid hij 1 rondje

        switchOn(2, True)
        angle *= -1
        time.sleep(angle/540)

        switchFlow()
        motorAngle -= angle
    else:
        #turn the motor x degrees.

        switchOn(2, True)
        time.sleep(angle/540)

        motorAngle += angle



def switchFlow():
    #step 1: turn the whole system off.     (here we turn switch 2 on for a certain amount of seconds.)
    switchOn(2, False)
    
    time.sleep(0.1)

    #step 2: Switch the states of switch 1 and 3
    if switch1On == True and switch3On == True:
        switchOn(1, False)
        switchOn(3, False)

    elif switch1On == False and switch3On == False:
        switchOn(1, True)
        switchOn(3, True)

    time.sleep(0.1)



def switchOn(switch: int, on: bool):
    global switch1On
    global switch3On
    
    if switch == 1:
        switchCh = 21
    elif switch == 2:
        switchCh = 20
    elif switch == 3:
        switchCh = 26
    else:
        print("Invalid switch number.")
        exit("Invalid switch number.")

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(switchCh, GPIO.OUT)

    if on == True:
        GPIO.output(switchCh, GPIO.LOW)
        print("switch " + str(switch) + " turned on.")

        if switch == 1:
            switch1On = True
        elif switch == 3:
            switch3On = True

    elif on == False:
        GPIO.output(switchCh, GPIO.HIGH)
        print("switch " + str(switch) + " turned off.")

        if switch == 1:
            switch1On = False
        elif switch == 3:
            switch3On = False

def updateMotors():
    toTurnAngle = calculateAngle(motorAngle)
    turnMotor(toTurnAngle)

switchFlow()
for x in range(6):
    turnTenDegrees()
    time.sleep(1)
    
switchFlow()

GPIO.cleanup()

