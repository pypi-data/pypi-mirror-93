# -*- coding: utf-8 -*-

import datetime
import typing
from typing import TYPE_CHECKING

import datemore.daterange
import datemore.utils

if TYPE_CHECKING:  # pragma: no cover
    import datemore.datetime


DateType = typing.Union[datetime.date, "Date"]


class Date(datetime.date, datemore.daterange.Daterange):
    @classmethod
    def from_native(cls, _date: datetime.date) -> "Date":
        """Creates a wrapped Date instance from a native datetime date"""
        return cls(year=_date.year, month=_date.month, day=_date.day)

    @classmethod
    def today(cls) -> "Date":
        """Returns the today's date"""
        t = datetime.datetime.today().timestamp()
        return cls.fromtimestamp(t)

    def native(self) -> datetime.date:
        """Returns the underlying native datetime date instance"""
        return datetime.date(year=self.year, month=self.month, day=self.day)

    def add_days(self, days: int) -> "Date":
        """Adds some number of days to the current Date"""
        return self.from_native(datemore.utils.add_days(self, days))

    def range(self, offset: int) -> typing.List["Date"]:
        """Returns a range of dates within this Date and a given offset"""
        return self.date_range(self, offset=offset)

    def range_to(self, end: "Date") -> typing.List["Date"]:
        """Returns a range of dates between this Date and another Date"""
        return self.dates_between(start=self, end=end)
