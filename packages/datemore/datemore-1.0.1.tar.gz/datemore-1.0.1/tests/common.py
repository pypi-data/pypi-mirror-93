#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Common testing functions for `datemore` package."""

import datetime
import typing

import datemore.datetime
import datemore.time


def _time_tuple(time: datemore.time.TimeType) -> int:
    """Return passed time of day in seconds """
    return time.hour * 60 * 60 + time.minute * 60 + time.second


def assert_almost_equal(
    d1: datemore.datetime.DatetimeType,
    d2: datemore.datetime.DatetimeType,
    tolerance: typing.Optional[int] = 1,
) -> None:
    if all(isinstance(n, datetime.datetime) for n in [d1, d2]):
        tolerance = tolerance or 1
        assert d1.date() == d2.date()
        assert abs(_time_tuple(d1.time()) - _time_tuple(d2.time())) < tolerance
    else:
        tolerance = tolerance or 1
        assert abs(d1.timetuple().tm_yday - d2.timetuple().tm_yday) < tolerance


def assert_correct_daterange(
    date_range: typing.List[typing.Any],
    days: typing.List[int],
    date_type: typing.Type[datemore.datetime.DatesType],
) -> None:
    assert isinstance(date_range, list)
    assert all(isinstance(x, date_type) for x in date_range)
    assert [d.day for d in date_range] == days
