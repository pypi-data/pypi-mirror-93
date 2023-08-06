#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `datemore` package."""

import datetime

import datemore.time
import tests.common as c


def test_conversion_from_native() -> None:
    native = datetime.time(hour=22, minute=12, second=59)
    assert datemore.time.Time.from_native(native).native() == native


def test_conversion_to_native() -> None:
    non_native = datemore.time.Time(hour=22, minute=12, second=59)
    assert non_native.native() == datetime.time(hour=22, minute=12, second=59)


def test_delta() -> None:
    t1 = datemore.time.Time(hour=22, minute=12, second=59)
    t2 = datemore.time.Time(hour=23, minute=14, second=59)
    assert (
        datemore.time.Time.delta(t1, t2).total_seconds()
        == datetime.timedelta(hours=1, minutes=2).total_seconds()
    )


def test_add() -> None:
    mock_time = datemore.time.Time(hour=22, minute=12, second=59)
    assert mock_time.add(hours=2).add(hours=-2) == mock_time
    assert mock_time.add(hours=1) == datemore.time.Time(hour=23, minute=12, second=59)
