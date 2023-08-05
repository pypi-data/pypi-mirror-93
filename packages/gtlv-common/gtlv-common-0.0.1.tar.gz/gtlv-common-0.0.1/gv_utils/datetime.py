#!/usr/bin/env python3

from datetime import datetime, timedelta, tzinfo
import re
from typing import Callable, Generator, Union

import pytz


LOCAL_TZ = pytz.timezone('Europe/Paris')
ISO_FORMAT_TZ = '%Y-%m-%dT%H:%M:%S%z'
ISO_FORMAT_MICRO_TZ = '%Y-%m-%dT%H:%M:%S.%f%z'
ISO_FORMAT = '%Y-%m-%dT%H:%M:%S'
ISO_FORMAT_MICRO = '%Y-%m-%dT%H:%M:%S.%f'
WEB_FORMAT = '%Y-%m-%d_%H-%M'
ISO_FORMATS = [WEB_FORMAT, ISO_FORMAT_TZ, ISO_FORMAT_MICRO_TZ, ISO_FORMAT, ISO_FORMAT_MICRO]
HTTP_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'


def split_in_minutes(fromdate: datetime, todate: datetime, freq: int = 1) -> Generator[datetime, None, None]:
    for startmin, endmin in _generate_time_serie(fromdate, todate, lambda x: x, timedelta(minutes=freq)):
        yield startmin
    yield todate.replace(second=0)


def split_in_days(fromdate: datetime, todate: datetime) -> Generator[datetime, None, None]:
    yield from _generate_time_serie(fromdate, todate, lambda x: x.replace(hour=0, minute=0, second=0), timedelta(1))


def _generate_time_serie(fromdate: datetime, todate: datetime, ndate_initializer: Callable[[datetime], datetime],
                         incr: timedelta) -> Generator[datetime, None, None]:
    if fromdate > todate:
        fromdate, todate = todate, fromdate
    cdate, ndate = fromdate, fromdate
    ndate = ndate_initializer(cdate + incr)
    while ndate < todate:
        yield cdate, ndate - timedelta(seconds=1)
        cdate = ndate
        ndate = cdate + incr
    yield cdate, todate


def add_one_week(d: datetime) -> datetime:
    return d + timedelta(days=7)


def add_one_month(d: datetime) -> datetime:
    try:
        nextmonth = (d.replace(day=28) + timedelta(days=7)).replace(day=d.day)
    except ValueError:  # assuming January 31 should return last day of February.
        nextmonth = (d + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    return nextmonth


def now(roundtominute: bool = False) -> datetime:
    date = datetime.now()
    return to_local(date, roundtominute)


def utcnow(roundtominute: bool = False) -> datetime:
    date = datetime.utcnow()
    return to_utc(date, roundtominute)


def from_timestamp(timestamp: int, roundtominute: bool = False) -> datetime:
    date = datetime.fromtimestamp(timestamp)
    return to_local(date, roundtominute)


def to_local(date: datetime, roundtominute: bool = False) -> datetime:
    return to_tz(date, LOCAL_TZ, roundtominute)


def to_utc(date: datetime, roundtominute: bool = False) -> datetime:
    return to_tz(date, pytz.utc, roundtominute)


def to_tz(date: datetime, tz: Union[pytz.tzinfo, tzinfo], roundtominute: bool = False) -> datetime:
    try:
        date = tz.localize(date)
    except ValueError:
        date = date.astimezone(tz)
    date = date.replace(microsecond=0)
    if roundtominute:
        date = round_to_minute(date)
    return date


def round_to_minute(date: datetime) -> datetime:
    return date.replace(second=0)


def encode_datetime(date: Union[datetime, str], strformat: str = ISO_FORMAT_TZ) -> str:
    if type(date) is str:
        return date

    return date.strftime(strformat)


def decode_datetime(string: Union[str, datetime], dateformat: str = None) -> datetime:
    if type(string) is datetime:
        return to_local(string)

    string = re.sub(r'([\+|\-][0-9]{2}):([0-9]{2})$', r'\1\2', string)  # handles .isoformat() output
    dateformats = ISO_FORMATS
    if dateformat is not None:
        dateformats = [dateformat, ] + dateformats

    for dateformat in dateformats:
        try:
            date = datetime.strptime(string, dateformat)
        except ValueError:
            pass
        else:
            return to_local(date)


def to_http_date(date: datetime) -> str:
    return date.strftime(HTTP_FORMAT)
