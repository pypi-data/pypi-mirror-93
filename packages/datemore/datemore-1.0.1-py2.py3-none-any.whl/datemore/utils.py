# -*- coding: utf-8 -*-

import datetime
import typing

import pytz

import datemore

if typing.TYPE_CHECKING:  # pragma: no cover
    import pytz.tzfile

    import datemore.datetime
    import datemore.time


DateType = typing.TypeVar(
    "DateType",
    "datemore.datetime.Datetime",
    "datemore.date.Date",
    datetime.datetime,
    datetime.date,
)


def to_local_time(
    date: datetime.datetime, tz: pytz.tzfile = pytz.timezone("Europe/Berlin")
) -> datetime.datetime:
    """Returns a given date converted to local time"""
    localized = tz.localize(date)
    if not isinstance(localized, datetime.datetime):
        raise ValueError
    return localized


def is_on_weekend(date: datetime.datetime) -> bool:
    """Returns if a given date is a sunday or saturday"""
    weekday = to_local_time(date).strftime("%A")
    return weekday.lower() in ["saturday", "sunday"]


def add_offset(
    date: DateType, **kwargs: int
) -> typing.Union[datetime.datetime, datetime.date]:
    """Adds a delta offset to a given datetime date object"""
    new_date = date + datetime.timedelta(**kwargs)
    return new_date


def add_days(
    date: DateType, days: int
) -> typing.Union[datetime.datetime, datetime.date]:
    """Adds a number of days to a given datetime date object"""
    return add_offset(date, days=days)


def subtract_days(
    date: DateType, days: int
) -> typing.Union[datetime.datetime, datetime.date]:
    """Subtracts a number of dates from a given datetime date object"""
    return add_days(date, -days)


def yesterday(date: DateType) -> typing.Union[datetime.datetime, datetime.date]:
    """Returns the date one day before the given date"""
    return subtract_days(date, 1)


def tomorrow(date: DateType) -> typing.Union[datetime.datetime, datetime.date]:
    """Returns the date one day after the given date"""
    return add_days(date, 1)


def closest_future_date(
    date: "datemore.datetime.DatetimeType", time: "datemore.time.TimeType"
) -> "datemore.datetime.DatesType":
    """Returns the closest date for a future date with a given hour"""
    future_date = date if date.time() < time else tomorrow(date)
    if isinstance(future_date, datemore.datetime.Datetime):
        future_date = future_date.native()
    return datemore.datetime.Datetime.from_native(
        datetime.datetime.combine(future_date, time)
    )


def next_full_hour(date: datetime.datetime) -> datetime.datetime:
    """Returns the closest date at full hour"""
    return date.replace(hour=date.hour + 1, minute=0, second=0, microsecond=0)
