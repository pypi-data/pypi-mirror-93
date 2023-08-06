# -*- coding: utf-8 -*-

import datetime
import typing

import datemore.datetime

TimeType = typing.Union[datetime.time, "Time"]


class Time(datetime.time):
    @classmethod
    def from_native(cls, _time: datetime.time) -> "Time":
        """Creates a wrapped Time instance from a native datetime time"""
        return cls(
            _time.hour, _time.minute, _time.second, _time.microsecond, fold=_time.fold
        )

    @classmethod
    def delta(cls, t1: "Time", t2: "Time") -> datetime.timedelta:
        """Calculates the difference between two times"""
        return t2.as_date() - t1.as_date()

    def as_date(self) -> "datemore.datetime.Datetime":
        """Converts a Time instance to a Datetime instance using today's date"""
        return datemore.datetime.Datetime.from_native(
            datetime.datetime.combine(datetime.date.today(), self)
        )

    def native(self) -> datetime.time:
        """Returns the underlying native datetime time instance"""
        return datetime.time(
            self.hour, self.minute, self.second, self.microsecond, fold=self.fold
        )

    def add(self, **kwargs: int) -> "Time":
        """Returns a new Time instance shifted by given parameters"""
        dt = self.as_date().native()
        dt += datetime.timedelta(**kwargs)
        return datemore.datetime.Datetime.from_native(dt).time()
