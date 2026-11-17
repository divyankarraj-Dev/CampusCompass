"""Current date and time."""
from datetime import datetime


def get_time():
    return "The time is " + datetime.now().strftime("%I:%M:%S %p")


def get_date():
    return "Today is " + datetime.now().strftime("%A, %d %B %Y")
