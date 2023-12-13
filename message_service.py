# 'GitHub Copilot' was used as a tool whilst writing this code.

import requests
import asyncio


# A function that sends a message to the IFTTT API, which then sends a mail to specified people
async def send_message(notification_type: str, info: str = "No info provided", people=""):
    import main

    try:
        if people == "":
            people = "--EMAIL--"

        values = {"value1": info, "value2": notification_type, "value3": people}

        url = f"--URL--"
        request = requests.get(url, params=values)
        if request.status_code == 200:
            print("'message_service' | send successfully")
        else:
            print("'message_service' | Something went wrong calling the IFTTT API")
            # If the ifttt API can't be reached, try again in 60 seconds
            await asyncio.sleep(60)
            await send_message(notification_type, info)

    except Exception as e:
        print("'message_service' | Error in message_service: " + str(e))
        # If there is an error in the send_message() function, the program will stop.
        main.running = False
