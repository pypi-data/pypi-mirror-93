# -*- coding: utf-8 -*-

import datetime
import typing
from typing import TYPE_CHECKING

import pytz

import datemore.date
import datemore.daterange
import datemore.time
import datemore.utils

if TYPE_CHECKING:  # pragma: no cover
    import pytz.tzfile


DatetimeType = typing.Union["Datetime", datetime.datetime]
DatesType = typing.Union[
    "Datetime", "datemore.date.Date", datetime.datetime, datetime.date
]


class Datetime(datetime.datetime, datemore.daterange.Daterange):
    @classmethod
    def from_native(cls, _datetime: DatetimeType) -> "Datetime":
        """Creates a wrapped Datetime instance from a native datetime datetime"""
        ts = _datetime.timestamp()
        return cls.fromtimestamp(ts)

    @classmethod
    def now(cls, tz: typing.Optional[typing.Any] = None) -> "Datetime":
        """Returns the current local Datetime"""
        now = cls.from_native(super().now())
        return now.localize() or now

    @classmethod
    def today(cls) -> "Datetime":
        """Same as ``now()``"""
        return cls.now()

    def localize(
        self, timezone: pytz.tzfile = pytz.timezone("Europe/Berlin")
    ) -> typing.Optional["Datetime"]:
        """Returns a new Datetime instance that has been localized to a specific timezone"""
        try:
            localized = timezone.localize(self)
            return self.from_native(localized)
        except Exception as e:
            if "tzinfo is already set" in str(e):
                return self
        return None

    def add_days(self, days: int) -> "Datetime":
        """Returns a new Datetime instance shifted by a given number of days"""
        new_date = datemore.utils.add_days(self, days=days)
        if not isinstance(new_date, datetime.datetime):
            raise TypeError
        return self.from_native(new_date)

    def add(self, **kwargs: int) -> "Datetime":
        """Returns a new Datetime instance shifted by given parameters"""
        new_date = datemore.utils.add_offset(self, **kwargs)
        if not isinstance(new_date, datetime.datetime):
            raise TypeError
        return self.from_native(new_date)

    def native(self) -> datetime.datetime:
        """Returns the underlying native datetime datetime instance"""
        ts = self.timestamp()
        return datetime.datetime.fromtimestamp(ts)

    def date(self) -> "datemore.date.Date":
        """Returns the Datetime's date as a Date instance"""
        date = super().date()
        return datemore.date.Date(date.year, date.month, date.day)

    def time(self) -> "datemore.time.Time":
        """Returns the Datetime's time as a Time instance"""
        time = super().time()
        return datemore.time.Time(
            time.hour, time.minute, time.second, time.microsecond, fold=time.fold
        )

    def is_on_weekend(self) -> bool:
        """Returns whether this Datetime is on a weekend or not"""
        return datemore.utils.is_on_weekend(self)

    def range_to(self, end: "Datetime") -> typing.List["Datetime"]:
        """Returns a range of Datetime's between this Datetime and another Datetime"""
        return self.dates_between(start=self, end=end)
