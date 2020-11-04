import time
import re


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
        return time.strftime("%d.%m.%Y %H:%M", time.gmtime(time.time()))
    else:
        return time.strftime("%d.%m.%Y %H:%M", time.gmtime(datetime))


# Convert timestamp to seconds
def timestamp_to_sec(timestamp):
    if is_timestamp(timestamp) is True:
        sec = 0
        ts_split = timestamp.split(":")
        if len(ts_split) > 3:
            return -1

        if len(ts_split) == 2:
            sec = int(ts_split[0])*60*60 + int(ts_split[1])*60
        if len(ts_split) == 3:
            sec = int(ts_split[0])*3600 + int(ts_split[1])*60 + int(ts_split[2])

        return sec
    else:
        return timestamp
