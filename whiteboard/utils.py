import time
import datetime
import re


# Floating number regex check
# e.g. 123.45
def is_float(value):
    pattern = re.compile(r'[0-9]+[.]?[0-9]+')
    if pattern.fullmatch(value) is None:
        return False
    else:
        return True


# Datetime regex check (dd.mm.YYY HH:MM)
# e.g. 17.5.2019 19:21
def is_datetime(value):
    pattern = re.compile(r'\d{1,2}.\d{1,2}.\d{4} \d{1,2}([:]\d{1,2}){1,2}')
    if pattern.fullmatch(value) is None:
        return False
    else:
        return True


# Datetime regex check (dd.mm.YYY)
# e.g 19:21:23
def is_timestamp(value):
    pattern = re.compile(r'\d{1,2}(:\d{1,2}){1,2}')
    if pattern.fullmatch(value) is None:
        return False
    else:
        return True


# Get timestamp in specific format
# e.g. 01.12.1990 12:00
def get_format_timestamp(datetime=None):
    if datetime is None:
        return time.strftime("%d.%m.%Y %H:%M", time.localtime(time.time()))
    else:
        return time.strftime("%d.%m.%Y %H:%M", time.localtime(datetime))


# Convert timestamp (HH:MM:SS) to seconds
# @todo Check the timezone
def timestamp_to_sec(value):
    if is_timestamp(value) is True:
        sec = 0
        ts_split = value.split(":")
        if len(ts_split) > 3:
            return -1

        if len(ts_split) == 2:
            sec = int(ts_split[0])*60*60+int(ts_split[1])*60
        if len(ts_split) == 3:
            sec = int(ts_split[0])*3600+int(ts_split[1])*60+int(ts_split[2])

        return sec
    elif value.isdigit() is True or is_float(value) is True:
        return value
    else:
        return -1


# Convert datetime (DD.MM:YYYY HH:MM:SS) to seconds
# @todo Check the timezone
def datetime_to_sec(value):
    if is_datetime(value) is True:
        dt_split = value.split(" ")
        if len(dt_split) > 2:
            return -1

        d_split = dt_split[0].split(".")
        t_split = dt_split[1].split(":")
        if len(d_split) > 3:
            return -1

        if len(t_split) > 3:
            return -1

        day = int(d_split[0])
        month = int(d_split[1])
        year = int(d_split[2])
        hour = int(t_split[0])
        minutes = int(t_split[1])
        seconds = 0

        if len(t_split) == 3:
            seconds = int(t_split[2])
        sec = time.mktime(datetime.datetime(
            year, month, day, hour, minutes, seconds).timetuple())
        return int(sec)
    elif value.isdigit() is True or is_float(value) is True:
        return value
    else:
        return -1
