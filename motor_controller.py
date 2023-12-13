# 'GitHub Copilot' was used as a tool whilst writing this code.

import asyncio
import datetime
import time

import main
import sunposition
import message_service

# Switch libraries
import RPi.GPIO as GPIO

# Defining switch variables.
switch1On = False
switch3On = False


# A function which turns a relay on or off
def switch_on(switch: int, on: bool):
    global switch1On, switch3On

    # Determine the switch channel
    match switch:
        case 1:
            switch_ch = 21
        case 2:
            switch_ch = 20
        case 3:
            switch_ch = 26
        case _:
            print("Invalid switch number.")
            raise Exception("'motor_controller' | Invalid switch number. (line 33)")

    # GPIO setup
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # Set the switch_gh gpio to be an output
    GPIO.setup(switch_ch, GPIO.OUT)

    # Turn the switch on or off
    if on is True:
        # Turn the switch on
        GPIO.output(switch_ch, GPIO.LOW)
        print("switch " + str(switch) + " turned on.")

        # Update the switch states
        if switch == 1:
            switch1On = True
        elif switch == 3:
            switch3On = True

    elif on is False:
        # Turn the switch off
        GPIO.output(switch_ch, GPIO.HIGH)
        print("switch " + str(switch) + " turned off.")

        # Update the switch states
        if switch == 1:
            switch1On = False
        elif switch == 3:
            switch3On = False


# A function which switches the polarity of the 12V power supply, this is done through the use of two relays
def switch_flow():
    # Step 1: turn the whole system off. (here we turn switch 2 on for a certain amount of seconds.)
    switch_on(2, False)

    time.sleep(0.1)

    # Step 2: Switch the states of switch 1 and 3
    if switch1On is True and switch3On is True:
        switch_on(1, False)
        switch_on(3, False)

    elif switch1On is False and switch3On is False:
        switch_on(1, True)
        switch_on(3, True)

    time.sleep(0.1)


# A function to calculate the percentage of time between sunrise and sunset that has passed (east = 0)
def get_sun_percentage(time_value):
    # Calculate the amount of seconds since midnight
    current_time_seconds = time_value.hour * 3600 + time_value.minute * 60 + time_value.second

    # Get the sunrise and sunset times
    sun_times = get_sun_times(time_value)
    sunrise_time = sun_times['sunrise_time']  # sunrise_time is in seconds since midnight
    sunset_time = sun_times['sunset_time']  # sunset_time is in seconds since midnight

    # day_seconds is the amount of seconds since midnight, capped at sunrise and sunset time.
    # This means the value will not be lower than sunrise time and not higher than sunset time.
    daylight_seconds = max(min(current_time_seconds, sunset_time), sunrise_time)

    return main.normalize(daylight_seconds, sunrise_time, sunset_time, 0, 100)


# A function which calculates and returns the sunrise and sunset times
def get_sun_times(time_value: datetime.datetime):
    time_value = time_value.replace(hour=12, minute=0, second=0, microsecond=0)
    sun_loc = sunposition.get_sun_loc(time_value, main.lat, main.long, main.timezone, True)

    return {"sunrise_time": sun_loc['sunrise_time'] * 86400, "sunset_time": sun_loc['sunset_time'] * 86400}


# The function called by main.py
# A function which controls the motor when necessary
async def control_motor():
    error = None
    current_motor_rotation = 0  #This value is 0 when facing east (0=no extention, 100=40cm extention (100%))
    night_mode = False

    while main.running:
        try:
            start_time = time.time()
            night_mode_start_time_diff = datetime.datetime.now() - datetime.datetime.now().replace(hour=20, minute=0, second=0, microsecond=0)
            night_mode_end_time_diff = datetime.datetime.now() - datetime.datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
            
            if abs(night_mode_start_time_diff) < datetime.timedelta(minutes=10):
                    if not night_mode:
                        night_mode = True
                        
                        # Switch the polarity of the 12V power supply
                        switch_flow()

                        # Move the solarpanel 50% back, so it is in the middle of its rotational capabilities
                        # This is the so called "Storm mode", this is better for preventing wind damage
                        flow_time = (50 * 4) / 14
                        
                        switch_on(2, True)
                        time.sleep(flow_time)
                        switch_on(2, False)

                        # Switch the polarity back, for future use
                        switch_flow()
                        
                        # Update current_motor_rotation variable
                        current_motor_rotation = 50
                    
                    
            if abs(night_mode_end_time_diff) < datetime.timedelta(minutes=10):
                    if night_mode:
                        night_mode = False
                        
                        # Switch the polarity of the 12V power supply
                        switch_flow()

                        # When it's 6 o'clock the solarpanel will return to it's start position. Because we can't trust the motor speed, the motor moves for 30 seconds
                        # This won't destroy anything because the motor has limit switches
                        switch_on(2, True)
                        time.sleep(30)
                        switch_on(2, False)

                        # Switch the polarity back, for future use
                        switch_flow()
                        
                        # Update current_motor_rotation variable
                        current_motor_rotation = 0
                    
            
            if not night_mode:
                
                current_datetime = datetime.datetime.now()
                
                # Get the location of the sun
                day_percentage = get_sun_percentage(current_datetime)
                angle_diff = abs(current_motor_rotation - day_percentage)

                # Check if the solar panel needs to be moved
                # At 24:00 the day_percentage will switch from 0 to 100
                if abs(current_motor_rotation - day_percentage) > main.motor_threshold:
                    
                    # Without switch_flow() on, the motor will extend.
                    if current_motor_rotation < day_percentage:  # The solarpanel is behind, extend motor to catch up.
                        flow_time = (angle_diff * 4) / 14
                        
                        switch_on(2, True)
                        time.sleep(flow_time)
                        switch_on(2, False)
                        
                        # Update current_motor_rotation variable
                        current_motor_rotation = day_percentage
                    
                    elif current_motor_rotation > day_percentage:  # The solarpanel is too far (end of day), retract motor to catch up.
                        # Switch the polarity of the 12V power supply
                        switch_flow()

                        flow_time = (angle_diff * 4) / 14
                        
                        switch_on(2, True)
                        time.sleep(flow_time)
                        switch_on(2, False)

                        # Switch the polarity back, for future use
                        switch_flow()
                        
                        # Update current_motor_rotation variable
                        current_motor_rotation = day_percentage
                    
                    else:
                        raise Exception("'motor_controller' | Error in line 158 (unexpected)")        
                        
                                
                    print(f"'motor_controller' | Motor controlled, difference: ({angle_diff})")
                else:
                    print(f"'motor_controller' | Motor not controlled, difference too small ({angle_diff})")

            await asyncio.sleep(main.motor_controller_delay - (time.time() - start_time))


        # Error handling
        # If another error occurs, the program stops and saves the file
        except Exception as e:
            # If one error is found, continue
            if error is None or datetime.datetime.now() - error >= datetime.timedelta(minutes=16):
                error = datetime.datetime.now()
                print("'motor_controller' | An error occurred in 'motor_controller.py', continuing: " + str(e))
                await message_service.send_message("ERROR", "ERROR in 'motor_controller.py'\n" + str(e))

            # If two errors occur within 5 minutes, the program stops.
            else:
                print("'motor_controller' | Two errors occurred within 15 minutes, terminating the process: " + str(e))

                await message_service.send_message("FATAL ERROR", "FATAL ERROR in 'motor_controller.py'\n" + str(e))
                main.running = False
