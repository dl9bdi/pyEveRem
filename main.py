"""
Event Reminder

Reads a list of events stored in a separate file and reads out all event dates.
Checks if one of the events in the lists occurs around today.
If so a pop-up will show the event.
"""

from datetime import datetime as dt
from tkinter import *
from tkinter import messagebox
import pandas
from playsound import playsound

event_filename = "eventdates.txt"
today = dt.now().date()

today_tuple = (today.month, today.day)
try:
    tmp_data = pandas.read_csv(event_filename)
except FileNotFoundError:
    messagebox.showerror(title="File not found", message="Could not open file " + event_filename)
    exit(1)

data = tmp_data.to_dict(orient="records")


def day_difference(date1, date2):
    """
    Calculates the shortes distance between two dates in days. Important at year roll-over.
    It checks difference for days in the same year as well as to one year ahead and one year back.
    :param date1: first date
    :param date2: second date
    :return: difference in days
    """
    short_difference = 600
    tmp_date = date2.replace(date1.year)
    if abs((tmp_date - date1).days) < abs(short_difference):
        short_difference = (tmp_date - date1).days

    tmp_date = date2.replace(date1.year - 1)
    if abs((tmp_date - date1).days) < abs(short_difference):
        short_difference = (tmp_date - date1).days

    tmp_date = date2.replace(date1.year + 1)
    if abs((tmp_date - date1).days) < abs(short_difference):
        short_difference = (tmp_date - date1).days
    return short_difference


active_events = {}
dict_entry = 0
for data_row in data:
    try:
        event_date = dt.strptime(data_row["date"].strip(), "%d.%m.%Y").date()
    except ValueError as errormessage:
        messagebox.showerror(title="Data format error ", message=f"Could not convert to date format:\n {errormessage}")
        exit(2)

    diff_event_today = day_difference(today, event_date)
    reminder_str = ""
    if abs(diff_event_today) < 3:
        #print("shortdiff: ", day_difference(today, event_date))
        if diff_event_today == -2:
            reminder_str = f"{data_row["name"].strip()} hatte vorgestern {data_row["event"].strip()}."
        if diff_event_today == -1:
            reminder_str = f"{data_row["name"].strip()} hatte gestern {data_row["event"].strip()}."
        if diff_event_today == 0:
            reminder_str = f"{data_row["name"].strip()} hat heute {data_row["event"].strip()}."
        if diff_event_today == 1:
            reminder_str = f"{data_row["name"].strip()} hat morgen {data_row["event"].strip()}."
        if diff_event_today == 2:
            reminder_str = f"{data_row["name"].strip()} hat übermorgen {data_row["event"].strip()}."
        # active_events.append(reminder_str)
        active_events[dict_entry] = {}
        active_events[dict_entry]['diff'] = diff_event_today
        active_events[dict_entry]['event'] = reminder_str
        dict_entry += 1

#print(active_events)
sorted_events = sorted(active_events.items(), key=lambda x: x[1]["diff"])
#print(sorted_events)


# Buttons
def click_exit():
    exit(0)


if len(sorted_events) > 0:
    window = Tk()
    window.title("Aktuelle Ereignisse")
    window.minsize(width=600, height=420)
    window.configure(background="lightblue")

    # info_label = Label(text="Found events").grid(column=0, row=0)
    exit_button = (Button(width=15, height=2, text="Ende", command=click_exit))
    exit_button.grid(column=1, row=2, pady=10)
    event_list = Text(window, height=20, width=70, font=("Arial", 12, "normal"))
    event_list.grid(column=1, row=1, padx=20, pady=10)
    event_list.focus()
    event_list.tag_config("warning", background="yellow", foreground="black")
    event_list.tag_config("alert", background="red", foreground="white")
    for single_event in sorted_events:

        marker = ""
        #print(single_event[1]["diff"])
        if (abs(int(single_event[1]["diff"]))) == 1:
            marker = "warning"
        if (abs(int(single_event[1]["diff"]))) == 0:
            marker = "alert"

        event_list.insert(END, single_event[1]["event"] + "\n", marker)
        #print(single_event[1]["event"])
    event_list.config(state=DISABLED)
    window.update()
    playsound('./alert_sound.mp3')

    window.mainloop()
