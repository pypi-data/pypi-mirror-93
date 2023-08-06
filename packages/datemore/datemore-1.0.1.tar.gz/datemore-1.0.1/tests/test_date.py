#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `datemore` package."""

import datetime

import datemore.date
import datemore.datetime
import tests.common as c


def test_conversion_from_native() -> None:
    native = datetime.datetime(2019, 12, 10, hour=22, minute=12, second=59)
    assert datemore.datetime.Datetime.from_native(native).native() == native


def test_conversion_to_native() -> None:
    non_native = datemore.datetime.Datetime(2019, 12, 10, hour=22, minute=12, second=59)
    assert non_native.native() == datetime.datetime(
        2019, 12, 10, hour=22, minute=12, second=59
    )


def test_today() -> None:
    c.assert_almost_equal(datemore.date.Date.today().native(), datetime.date.today())


def test_add() -> None:
    mock_date = datemore.date.Date(2019, 10, 10)
    assert mock_date.add_days(2).add_days(-2) == mock_date
    assert mock_date.add_days(2) == datemore.date.Date(2019, 10, 12)


def test_range_to() -> None:
    mock_start_date = datemore.date.Date(2019, 10, 10)
    mock_end_date = datemore.date.Date(2019, 10, 15)
    date_range = mock_start_date.range_to(mock_end_date)
    c.assert_correct_daterange(
        date_range, days=[10, 11, 12, 13, 14], date_type=datemore.date.Date
    )


def test_range_offset() -> None:
    mock_start_date = datemore.date.Date(2019, 10, 10)
    date_range = datemore.date.Date.date_range(mock_start_date, offset=5)
    c.assert_correct_daterange(
        date_range, days=[10, 11, 12, 13, 14], date_type=datemore.date.Date
    )
