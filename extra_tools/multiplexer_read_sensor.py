import time
from ina260.controller import Controller
import tca9548a

# Define multiplexer
multiplexer = tca9548a.TCA9548A(0x70)


def multiplexer_disall():
	for x in range(8):
		multiplexer.set_channel(x, 0)
		
def multiplexer_solo(channel: int):
	if channel < 0 or channel > 7:
		exit("Invalid usage of multiplexer_solo(), " + str(channel) + " is not between 0 and 7")
	multiplexer_disall()
	multiplexer.set_channel(channel, 1)

# Just incase...
multiplexer_disall()
# This multiplexer_solo() call is nessasary. If not here there will be no '0x40' i2c device thus the next line will return an error.
multiplexer_solo(0)
sensor = Controller(address=0x40)

running = True

while running:
	try:
		multiplexer_solo(0)
		sensor_1_voltage = sensor.voltage()

		print(f"Sensor 1: {sensor_1_voltage}V")
		time.sleep(0.5)
	except KeyboardInterrupt:
		running = False
	except Exception:
		running = False

multiplexer_disall()
print("\nScript stopped!")
