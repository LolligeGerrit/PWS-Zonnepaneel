import main
import message_service
import asyncio
import datetime
import time


# A function which send a daily recap to the user
async def send_daily_recap():
    error = None
    people = "---EMAIL---, ---EMAIL---, ..."

    while main.running:
        try:
            start_time = time.time()
            recap_time_difference = datetime.datetime.now() - datetime.datetime.now().replace(hour=21, minute=0, second=0, microsecond=0)
            reset_recap_time_difference = datetime.datetime.now() - datetime.datetime.now().replace(hour=23, minute=0, second=0, microsecond=0)

            # If the time is close to 23:00, reset the daily recap values
            if abs(reset_recap_time_difference) < datetime.timedelta(minutes=10):
                main.daily_recap_send = False
                main.daily_power_values = []

            # Check if the daily recap needs to be sent
            if abs(recap_time_difference) < datetime.timedelta(minutes=5) and main.daily_recap_send is False:
                main.daily_recap_send = True
                # Calculate today's total yield (kWh)
                total_yield = 0
                max_power_value = max(main.daily_power_values)

                for power_value in main.daily_power_values:
                    # power_value is in W, every value lasted for x (data_collection_delay) seconds
                    # Because W = J/s, multiplying power_value by data_collection_delay gives us Joules.
                    # Dividing by 3600000 gives us kWh.
                    total_yield += (power_value * main.data_collection_delay) / 3600000

                    # Send the message
                    await message_service.send_message("Daily recap", f"Today's total yield was {total_yield} kWh.\nThe maximum power value was {max_power_value} W.", people)
                    print("'daily_recap' | Daily recap sent")

            await asyncio.sleep(main.daily_recap_check_delay - (time.time() - start_time))

        except Exception as e:
            # If one error is found, continue
            if error is None or datetime.datetime.now() - error >= datetime.timedelta(minutes=16):
                error = datetime.datetime.now()
                print("'daily_recap' | An error occurred in 'daily_recap.py', continuing: " + str(e))
                await message_service.send_message("ERROR", "ERROR in 'motor_controller.py'\n" + str(e))

            # If two errors occur within 5 minutes, the daily_recap script stops.
            else:
                print("'daily_recap' | Two errors occurred within 15 minutes, terminating the process: " + str(e))

                await message_service.send_message("FATAL ERROR", "FATAL ERROR in 'daily_recap.py'. This means the daily_recap.py script will be terminated. The rest of the scripts will continue, don't worry." + str(e))
                exit("daily_recap error")
