#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `datemore` package."""

import datemore.datetime
import datemore.utils


def test_is_on_weekend() -> None:
    """Test checking dates if they are on weekends"""
    mock_date = datemore.datetime.Datetime(2019, 10, 11, hour=15)  # Friday in berlin
    for i in range(10):
        mock_date = mock_date.add_days(i * 7)
        assert mock_date.add_days(0).is_on_weekend() == False
        assert mock_date.add_days(1).is_on_weekend() == True
        assert mock_date.add_days(2).is_on_weekend() == True
        assert mock_date.add_days(3).is_on_weekend() == False
        assert mock_date.add_days(4).is_on_weekend() == False
        assert mock_date.add_days(5).is_on_weekend() == False
        assert mock_date.add_days(6).is_on_weekend() == False


def test_closest_future_date() -> None:
    """Test calculation of the closest future date (today or tomorrow) with the given hour"""
    mock_datetime = datemore.datetime.Datetime(2019, 10, 10, 15)
    mock_time = mock_datetime.time()
    # Just shy of not enough of the current date
    assert datemore.utils.closest_future_date(
        mock_datetime, mock_time
    ) == mock_datetime.add_days(1)
    # Perfectly in time
    assert (
        datemore.utils.closest_future_date(mock_datetime.replace(hour=14), mock_time)
        == mock_datetime
    )
    # The next day
    assert datemore.utils.closest_future_date(
        mock_datetime.replace(hour=17), mock_time
    ) == mock_datetime.add_days(1)


def test_next_full_hour() -> None:
    """Test calculation of the closest full hour"""
    assert datemore.utils.next_full_hour(
        datemore.datetime.Datetime(1999, 10, 10, hour=13, minute=22)
    ) == datemore.datetime.Datetime(1999, 10, 10, hour=14)


def test_tomorrow_yesterday() -> None:
    """Test calculation of the closest full hour"""
    assert datemore.utils.tomorrow(
        datemore.datetime.Datetime(1999, 10, 10, hour=13, minute=22)
    ) == datemore.datetime.Datetime(1999, 10, 11, hour=13, minute=22)
    assert datemore.utils.yesterday(
        datemore.datetime.Datetime(1999, 10, 10, hour=13, minute=22)
    ) == datemore.datetime.Datetime(1999, 10, 9, hour=13, minute=22)
