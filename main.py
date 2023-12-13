# 'GitHub Copilot' was used as a tool whilst writing this code.

import asyncio
import os
import time

import message_service  # This is outside of the try except because it doesn't need packages, thus doesn't give an error.
    
try:
    import motor_controller
    import data_collection
    import daily_recap
    
except Exception as e:
    print("'main' | An error occurred in 'main.py' at an import statement, saving data and terminating the process: " + str(e))
    asyncio.run(message_service.send_message("FATAL ERROR in 'main.py'", str(e), "--EMAIL--"))
    exit()


# The main function, this function runs the motor controller, data collection and daily_recap at the same time.
async def main():
    await message_service.send_message("Program started", "The program has started.", "--EMAIL--")
    await asyncio.gather(data_collection.collect_data(), motor_controller.control_motor(), daily_recap.send_daily_recap())


# A function which creates a directory
def make_dir(path):
    if os.path.exists(path):
        return
    else:
        os.mkdir(path)


# A simple normalisation function
def normalize(value, old_min, old_max, new_min, new_max):
    # https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio

    return (((value - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min


# Input values, to be adjusted by the user
# Location values
lat = 52.193442
long = 5.289420
timezone = 1

# Timing and threshold values
motor_controller_delay = 5 * 60  # (in seconds)
data_collection_delay = 2 * 60  # (in seconds)
daily_recap_check_delay = 5 * 60  # (in seconds)
motor_threshold = 5  # (in percent)


# The following values are not to be adjusted by the user
running = True  # If this is False, no loop will run
daily_power_values = []  # The daily total yield of the solar panel, in kWh
daily_recap_send = False  # If this is True, a daily recap was be sent to the user, this is reset every night

# Define the data folder and file
make_dir("data")
file = open("./data/pws_data.txt", "a")  # The dot specifies the current directory

# Start the program
if __name__ == "__main__":
    try:
        time.sleep(10)  # This sleep makes sure an internet connection is established
        print("Starting motor control and data collection")
        asyncio.run(main())

    except KeyboardInterrupt:
        print("KeyboardInterrupt, file closed.")
        file.close()
        exit("Keyboard Interrupt")

    except Exception as e:
        print("'main' | An error occurred in 'main.py', saving data and terminating the process: " + str(e))
        file.close()
        asyncio.run(message_service.send_message("FATAL ERROR in 'main.py'", str(e)))

        exit(e)
