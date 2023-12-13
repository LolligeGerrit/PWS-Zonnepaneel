import time
import RPi.GPIO as GPIO

switch1On = False
switch3On = False


def switch_flow():
    # Step 1: turn the whole system off.     (here we turn switch 2 on for a certain amount of seconds.)
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


def switch_on(switch: int, on: bool):
    global switch1On, switch3On

    # declare switch_ch to be the channel of the switch
    match switch:
        case 1:
            switch_ch = 21
        case 2:
            switch_ch = 20
        case 3:
            switch_ch = 26
        case _:
            print("Invalid switch number.")
            exit("Invalid switch number.")

    print(switch_ch)
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


def main():
    while True:
        try:
            motor_time = input("Motor runtime, in seconds. (negative means backwards)")
            try:
                motor_time = int(motor_time)
            except Exception:
                print("Invalid input.")
                continue

            if motor_time < 0:
                motor_time = abs(motor_time)
                switch_flow()
                switch_on(2, True)
                time.sleep(motor_time)
                switch_on(2, False)
                switch_flow()

            else:
                switch_on(2, True)
                time.sleep(motor_time)
                switch_on(2, False)

        except KeyboardInterrupt:
            GPIO.cleanup()
            exit("Keyboard Interrupt")
        except Exception as e:
            GPIO.cleanup()
            exit(e)


if __name__ == "__main__":
    main()
