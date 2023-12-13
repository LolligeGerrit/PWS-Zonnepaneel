# 'GitHub Copilot' was used as a tool whilst writing this code.

import os
import time
import datetime
import asyncio

import main
import message_service

from ina260.controller import Controller
import tca9548a

# Define multiplexer
multiplexer = tca9548a.TCA9548A(0x70)


# A function to disable all channels on the multiplexer
def multiplexer_disall():
    for x in range(8):
        multiplexer.set_channel(x, 0)


# A function to enable a single channel on the multiplexer
def multiplexer_solo(channel: int):
    if channel < 0 or channel > 7:
        exit("Invalid usage of multiplexer_solo(), " + str(channel) + " is not between 0 and 7")
    multiplexer_disall()
    multiplexer.set_channel(channel, 1)


# Read all sensors and return a dictionary with the sensor data
def read_sensors():
    multiplexer_disall()  # Just incase...
    multiplexer_solo(0)  # if not here, there will be no '0x40' i2c device thus the next line will return an error
    sensor = Controller(address=0x40)
    sensor_data = {"time": datetime.datetime.now()}
    try:
        for channel in range(4):
            multiplexer_solo(channel)
            sensor_data["sensor_" + str(channel + 1)] = {"voltage": sensor.voltage(), "current": sensor.current()}
    except:
        # This try-except is here to give a more descriptive error message
        raise Exception("Error in 'data_collection.py' (line 37), could not read sensor data.")

    return sensor_data


# The function called by main.py
# This function will collect data and write it to the data file
async def collect_data():
    file = main.file
    error = None

    while main.running:
        try:
            start_time = time.time()
            sd = read_sensors()  # sd stands for sensor_data
            data_string = (
                f"{sd['time']}|"
                f"{sd['sensor_1']['voltage']},{sd['sensor_1']['current']}|"
                f"{sd['sensor_2']['voltage']},{sd['sensor_2']['current']}|"
                f"{sd['sensor_3']['voltage']},{sd['sensor_3']['current']}|"
                f"{sd['sensor_4']['voltage']},{sd['sensor_4']['current']}\n"
            )

            file.write(data_string)

            # Flush file to os buffer, and from os buffer to file on disk
            file.flush()
            os.fsync(file)

            print("'data_collection' | Datapoint collected!")

            # Calculate the current total power
            current_total_power = 0
            for x in range(4):
                current_total_power += sd["sensor_" + str(x + 1)]["voltage"] * sd["sensor_" + str(x + 1)]["current"]

            # Add the current total power to the daily power values
            main.daily_power_values.append(current_total_power)

            # Sleep for x seconds, remove the time taken by code to execute
            await asyncio.sleep(main.data_collection_delay - (time.time() - start_time))

        # Error handling
        # If another error occurs, the program stops and saves the file
        except Exception as e:
            # If one error is found, continue
            if error is None or datetime.datetime.now() - error >= datetime.timedelta(minutes=10):
                error = datetime.datetime.now()
                print("'data_collection' | An error occurred in 'data_collection.py', saving the file and continuing: " + str(e))
                file.flush()
                os.fsync(file)
                await message_service.send_message("ERROR", str(e))

            # If two errors occur within 5 minutes, the program stops
            else:
                print("'data_collection' | Two errors occurred in 'data_collection.py' within 10 minutes, saving data and terminating the process: " + str(e))
                file.close()
                print("'data_collection' | File closed successfully")

                await message_service.send_message("FATAL ERROR", "FATAL ERROR in 'data_collection.py'\n" + str(e))
                main.running = False
