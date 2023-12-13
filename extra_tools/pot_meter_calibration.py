import board
import busio

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0)

#The actual calibration
print("Rotate the potentiometer to the lowest possible value. ")
input1 = float(input("Measure the angle of the solarpanel (in degrees): "))

# abs() is used for edge cases where rounding makes the value -0.0
lowest_pot = max(min(chan.value, 26350), 0)


print("-------------------------------\nRotate the potentiometer to the higest possible value. ")

input2 = float(input("Measure the angle of the solarpanel (in degrees): "))

higest_pot = max(min(chan.value, 26350), 0)


print(f"Lowest: {lowest_pot} with angle '{input1}', higest: {higest_pot} with angle '{input2}'.")
