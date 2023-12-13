# 'Github Copilot' was used as a tool whilst writing this code.

from matplotlib import pyplot as plt
from matplotlib import ticker
from matplotlib import dates as mdates
from matplotlib.widgets import Button

import datetime
import os

import numpy as np


# DISCLAIMER:
# This code will only work when the datafile has the following format:
# 2023-10-24 15:55:20.909942|1,31|2,31|3,31|4,31
# The first digit is voltage, the second is current


# Function that reads a file, and plots it if 'plot' is true
# The setup variable is a list that contains the setups you would like to process. If none, all setups will be processed
def read_file(path,
              plot: bool = False,
              setup: list = [1, 2, 3, 4],
              difference_toggle: bool = False,
              annotate_max: bool = False,
              plot_type: str = "w",
              start_date: datetime.datetime = datetime.datetime(1, 1, 1, 0, 0, 0),
              end_date: datetime.datetime = datetime.datetime.now()
              ):

    # Check if the file exists
    if not os.path.exists(path):
        print("INFO | Files not found, please run dataCollection.py first.")
    else:
        print("INFO | Data file found, reading it now.")

    time_values = []

    power_values = {}
    voltage_values = {}
    current_values = {}
    yield_values = {}

    difference_values = []
    difference_temp = []

    label_dict = {
        "w": {"label": "Vermogen (W)", "unit": "W"},
        "v": {"label": "Spanning (V)", "unit": "V"},
        "a": {"label": "Stroom (A)", "unit": "A"},
        "y": {"label": "Opbrengst (Wh)", "unit": "Wh"}
    }


    # Read the file
    file = open(path, "r")
    lines = file.readlines()
    line_number = 0
    error_lines = []

    # Make variable layout
    for i in setup:
        if plot_type == "all":
            power_values[f"setup_{i}"] = []
            voltage_values[f"setup_{i}"] = []
            current_values[f"setup_{i}"] = []
            yield_values[f"setup_{i}"] = [0]

        if plot_type == "y":
            power_values[f"setup_{i}"] = [0]
        else:
            power_values[f"setup_{i}"] = []

    # Make sure difference_toggle isn't true when there less or more than 2 setups selected
    if difference_toggle:
        if len(setup) != 2 or plot_type == "all":
            print("INFO | difference_toggle was set to false because there are more than 2 setup's selected.")
            difference_toggle = False

    # Process the file
    for line in lines:
        line_number += 1
        try:
            split_line = line.split("|")
        except:
            print(f"ERROR | Error splitting line {line_number} into sensors.")
            error_lines.append(line_number)
            continue

        try:

            # This is statement checks if the datapoint being checked is within the given time range
            if start_date <= datetime.datetime.strptime(split_line[0], "%Y-%m-%d %H:%M:%S.%f") <= end_date:
                # This if statement checks for "\n" at the end of the line, and removes it
                if "\n" in split_line[4]:
                    split_line[4] = split_line[4][:-1]

                # No try-except here because the if statement would have failed before this.
                # Add all the time values to the time_values list
                time_values.append(datetime.datetime.strptime(split_line[0], "%Y-%m-%d %H:%M:%S.%f"))

                # Add all the data to the corresponding lists
                for i in setup:
                    try:

                        values = split_line[i].split(",")
                        if plot_type == "all":
                            power_values[f"setup_{i}"].append(float(values[0]) * float(values[1]))
                            voltage_values[f"setup_{i}"].append(float(values[0]))
                            current_values[f"setup_{i}"].append(float(values[1]))

                            if time_values[-1].hour == 0 and time_values[-1].minute in [0, 1]:
                                yield_values[f"setup_{i}"].append(0 + ((float(values[0]) * float(values[1])) * 2*60 / 3600))

                            else:
                                yield_values[f"setup_{i}"].append(yield_values[f"setup_{i}"][-1] + ((float(values[0]) * float(values[1])) * 2*60 / 3600))

                        elif plot_type == "w":
                            power_values[f"setup_{i}"].append(float(values[0]) * float(values[1]))
                            if difference_toggle:
                                difference_temp.append(float(values[0]) * float(values[1]))

                        elif plot_type == "v":
                            power_values[f"setup_{i}"].append(float(values[0]))
                            if difference_toggle:
                                difference_temp.append(float(values[0]))

                        elif plot_type == "a":
                            power_values[f"setup_{i}"].append(float(values[1]))
                            if difference_toggle:
                                difference_temp.append(float(values[1]))

                        elif plot_type == "y":
                            if time_values[-1].hour == 0 and time_values[-1].minute in [0, 1]:
                                power_values[f"setup_{i}"].append(0 + ((float(values[0]) * float(values[1])) * 2 * 60 / 3600))
                                if difference_toggle:
                                    difference_temp.append(0 + ((float(values[0]) * float(values[1])) * 2 * 60 / 3600))

                            else:
                                power_values[f"setup_{i}"].append(power_values[f"setup_{i}"][-1] + ((float(values[0]) * float(values[1])) * 2 * 60 / 3600))
                                if difference_toggle:
                                    difference_temp.append(power_values[f"setup_{i}"][-1] + ((float(values[0]) * float(values[1])) * 2 * 60 / 3600))




                    except Exception as e:
                        print(f"ERROR | Error whilst getting the value from line {line_number} - {e}")
                        error_lines.append(line_number)
                        continue

                if difference_toggle:
                    difference_values.append(abs(difference_temp[0] - difference_temp[1]))
                    difference_temp = []

        except Exception as e:
            print(f"ERROR | Error whilst getting time from line {line_number} - {e}")
            error_lines.append(line_number)
            continue
        else:
            continue

    # Remove the first value from the yield_values list
    if plot_type in ["y", "all"]:
        for i in setup:
            if plot_type == "all":
                yield_values[f"setup_{i}"].pop(0)
            if plot_type == "y":
                power_values[f"setup_{i}"].pop(0)

    # Print error and other info
    print("INFO | Done reading file.")
    if len(error_lines) > 0:
        print(f"ERROR | Errors found on line(s) {error_lines}")
        exit("INFO | Errors found, exiting program.")

    else:
        print("INFO | No errors found!")
        print(f"INFO | {len(power_values[f'setup_{setup[0]}'])} lines processed.")


    # Print the total power yield per setup
    print("INFO | Total power yield:")
    total = {'setup_1': 0, 'setup_2': 0, 'setup_3': 0, 'setup_4': 0}
    for i in setup:
        for setup_power in power_values[f"setup_{i}"]:
            total[f"setup_{i}"] += (setup_power * 2*60) / 3600
    for i in total:
        if int(i[-1]) in setup:
            print(f" {i} | {round(total[i], 2)} Wh")

    # Plot the graph if 'plot' is true
    if plot:
        lines = []

        if plot_type == "all":
            fig, ax = plt.subplots(4)
            plot_count = 0
            for x in ["power_values", "voltage_values", "current_values", "yield_values"]:

                if x == "power_values":
                    values = power_values
                elif x == "voltage_values":
                    values = voltage_values
                elif x == "current_values":
                    values = current_values
                elif x == "yield_values":
                    values = yield_values
                for i in setup:
                    ax[plot_count].plot(time_values, values[f"setup_{i}"], label=f"Setup {i}")
                    ax[plot_count].set_title(x)

                    ##-- Create legend --##
                    leg = ax[plot_count].legend(fancybox=True, shadow=True)
                    leg.set_draggable(True)
                    ##-- End of create legend --##

                    
                plot_count += 1

            fig.tight_layout(pad=0.1)
            plt.show()

        else:
            fig, ax = plt.subplots()

            if 1 in setup:
                (setup_1,) = ax.plot(time_values, power_values["setup_1"], label=f"Setup 1 (fabriekshoek)")
                lines.append(setup_1)
            if 2 in setup:
                (setup_2,) = ax.plot(time_values, power_values["setup_2"], label=f"Setup 2 (seizoenshoek)")
                lines.append(setup_2)
            if 3 in setup:
                (setup_3,) = ax.plot(time_values, power_values["setup_3"], label=f"Setup 3 (draaien + fabriekshoek)")
                lines.append(setup_3)
            if 4 in setup:
                (setup_4,) = ax.plot(time_values, power_values["setup_4"], label=f"Setup 4 (draaien + seizoenshoek)")
                lines.append(setup_4)

            if difference_toggle:
                (difference,) = ax.plot(time_values, difference_values, label=f"Difference")
                lines.append(difference)

            ##--Plot formatting--##

            plt.title("PWS draaiende zonnepanelen")
            plt.xlabel("Tijd")
            plt.ylabel(label_dict[plot_type]["label"])

            # Rotate the tickers and make sure the placement is correct.
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right")
            # Make sure the tickers are equally spaced
            ax.xaxis.set_major_locator(ticker.LinearLocator())
            # Format the xaxis tickers to a nice day and time format
            xfmt = mdates.DateFormatter('%d-%m-%y %H:%M')
            # Apply the formatter from previous line
            ax.xaxis.set_major_formatter(xfmt)
            # Remove the whitespaces on the xaxis
            plt.margins(x=0.01)

            # Add a legend
            plt.legend(loc="upper left")

            ##--End of plot formatting--##

            ##-- Create legend --##
            leg = ax.legend(fancybox=True, shadow=True)
            map_legend_to_ax = {}  # Will map legend lines to original lines.
            pickradius = 5  # Points (Pt). How close the click needs to be to trigger an event.

            for legend_line, ax_line in zip(leg.get_lines(), lines):
                legend_line.set_picker(pickradius)  # Enable picking on the legend line.
                map_legend_to_ax[legend_line] = ax_line

            def on_pick(event):
                # On the pick event, find the original line corresponding to the legend
                # proxy line, and toggle its visibility.
                legend_line = event.artist

                # Do nothing if the source of the event is not a legend line.
                if legend_line not in map_legend_to_ax:
                    return

                ax_line = map_legend_to_ax[legend_line]
                visible = not ax_line.get_visible()
                ax_line.set_visible(visible)
                # Change the alpha on the line in the legend, so we can see what lines
                # have been toggled.
                legend_line.set_alpha(1.0 if visible else 0.2)
                fig.canvas.draw()

            fig.canvas.mpl_connect('pick_event', on_pick)

            # Works even if the legend is draggable. This is independent from picking legend lines.
            leg.set_draggable(True)

            ##-- End of create legend --##

            ##-- Annotate max values --##

            def annot_max(x, y, ax=None):
                xmax = x[np.argmax(y)]
                ymax = max(y)
                text = f"{round(ymax, 2)} {label_dict[plot_type]['unit']}"
                if not ax:
                    ax = plt.gca()
                arrowprops = dict(arrowstyle="->", alpha=0.5)
                kw = dict(xycoords='data', textcoords="offset points",
                          arrowprops=arrowprops, ha="left", va="bottom", alpha=0.5)
                ax.annotate(text, xy=(xmax, ymax), xytext=(0, 10), **kw)

            if annotate_max:
                for i in setup:
                    annot_max(time_values, power_values[f"setup_{i}"])
                if difference_toggle:
                    annot_max(time_values, difference_values)

            plt.show()

###--- Read the file ---###
# the file_path variable should be the path to the data file
file_path = r"./pws_data_7_dec_lc.txt"

# calls the read_file function
# plot_type can be the following:
#   w - plot the power values
#   v - plot the voltage values
#   a - plot the current values
#   y - plot the yield values
#   all - plot all of the above

read_file(file_path,
          plot=True,
          annotate_max=False,
          difference_toggle=True,
          setup=[1, 4],
          plot_type="all",
          # start_date=datetime.datetime(2023, 12, 7, 0, 0, 0),
          # end_date=datetime.datetime(2023, 12, 7, 23, 59, 59)
          )