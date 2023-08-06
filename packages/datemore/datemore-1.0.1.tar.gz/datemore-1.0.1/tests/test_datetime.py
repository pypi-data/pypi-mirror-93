#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `datemore` package."""

import datetime

import pytz

import datemore.date
import datemore.datetime
import tests.common as c

timezone = pytz.timezone("Europe/Berlin")


def test_conversion_from_native() -> None:
    native = datetime.date(2019, 12, 10)
    assert datemore.date.Date.from_native(native).native() == native


def test_conversion_to_native() -> None:
    non_native = datemore.date.Date(2019, 12, 10)
    assert non_native.native() == datetime.date(2019, 12, 10)


def test_now() -> None:
    c.assert_almost_equal(
        datemore.datetime.Datetime.now().native(),
        timezone.localize(datetime.datetime.now()),
    )


def test_today() -> None:
    c.assert_almost_equal(
        datemore.datetime.Datetime.today().native(),
        timezone.localize(datetime.datetime.today()),
    )


def test_date() -> None:
    assert datemore.datetime.Datetime(
        2019, 10, 10, hour=12
    ).date() == datemore.date.Date(2019, 10, 10)


def test_add() -> None:
    mock_date = datemore.datetime.Datetime(2019, 10, 10, hour=12)
    assert mock_date.add_days(2).add_days(-2) == mock_date
    assert mock_date.add_days(2) == datemore.datetime.Datetime(2019, 10, 12, hour=12)
    assert mock_date.add(seconds=2).add(seconds=-2) == mock_date
    assert mock_date.add(hours=-1) == datemore.datetime.Datetime(2019, 10, 10, hour=11)


def test_range_to() -> None:
    mock_start_date = datemore.datetime.Datetime(2019, 10, 10, hour=12)
    mock_end_date = datemore.datetime.Datetime(2019, 10, 15, hour=9)
    date_range = mock_start_date.range_to(mock_end_date)
    c.assert_correct_daterange(
        date_range, days=[10, 11, 12, 13, 14], date_type=datemore.datetime.Datetime
    )


def test_range_offset() -> None:
    mock_start_date = datemore.datetime.Datetime(2019, 10, 10, hour=12)
    date_range = datemore.datetime.Datetime.date_range(mock_start_date, offset=5)
    c.assert_correct_daterange(
        date_range, days=[10, 11, 12, 13, 14], date_type=datemore.datetime.Datetime
    )
