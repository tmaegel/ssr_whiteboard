# -*- coding: utf-8 -*-
import datetime
import re
import time
from typing import Optional, Union


def is_float(value: str) -> bool:
    """Check for floating number."""
    if value is None:
        return False
    pattern = re.compile(r"[0-9]+[.]?[0-9]+")
    if pattern.fullmatch(value) is None:
        return False
    else:
        return True


def is_datetime(value: str) -> bool:
    """Check for datetime format (e.g. dd.mm.YYYY HH:MM)."""
    if value is None:
        return False
    pattern = re.compile(r"\d{1,2}.\d{1,2}.\d{4} \d{1,2}([:]\d{1,2}){1,2}")
    if pattern.fullmatch(value) is None:
        return False
    else:
        return True


def is_timestamp(value: str) -> bool:
    """Check for timestamp format (e.g. HH.MMM.SS)."""
    if value is None:
        return False
    pattern = re.compile(r"\d{1,2}(:\d{1,2}){1,2}")
    if pattern.fullmatch(value) is None:
        return False
    else:
        return True


def get_format_timestamp(datetime: Optional[int] = None) -> Union[str, bool]:
    """Convert unix timestamp in datetime format (e.g. dd.mm.YYYY HH:MM)."""
    if datetime is None:
        return time.strftime("%d.%m.%Y %H:%M", time.localtime(time.time()))
    elif str(datetime).isdigit():
        return time.strftime("%d.%m.%Y %H:%M", time.localtime(datetime))
    else:
        return False


# @todo Check the timezone
def timestamp_to_sec(value: str) -> Union[int, bool]:
    """Convert timestamp (HH:MM:SS) to seconds."""
    if value is None:
        return False
    if value.isdigit() is True:
        return int(value)
    if is_timestamp(value) is False:
        return False

    sec = 0
    ts_split = value.split(":")
    if len(ts_split) > 3:
        return False
    if len(ts_split) == 2:
        sec = int(ts_split[0]) * 60 * 60 + int(ts_split[1]) * 60
    if len(ts_split) == 3:
        sec = int(ts_split[0]) * 3600 + int(ts_split[1]) * 60 + int(ts_split[2])

    return sec


# @todo Check the timezone
def datetime_to_sec(value: str) -> Union[int, bool]:
    """Convert datetime (dd.mm.YYYY HH:MM) to seconds."""
    if value is None:
        return False
    if is_datetime(value) is False:
        return False

    dt_split = value.split(" ")
    if len(dt_split) > 2:
        return False

    d_split = dt_split[0].split(".")
    t_split = dt_split[1].split(":")
    if len(d_split) > 3:
        return False
    if len(t_split) > 3:
        return False

    day = int(d_split[0])
    month = int(d_split[1])
    year = int(d_split[2])
    hour = int(t_split[0])
    minutes = int(t_split[1])
    seconds = 0

    if len(t_split) == 3:
        seconds = int(t_split[2])
    sec = time.mktime(
        datetime.datetime(year, month, day, hour, minutes, seconds).timetuple()
    )

    return int(sec)
