# -*- coding: utf-8 -*-

import typing

if typing.TYPE_CHECKING:  # pragma: no cover
    import datemore.date  # noqa
    import datemore.datetime  # noqa


DateType = typing.TypeVar(
    "DateType", "datemore.datetime.Datetime", "datemore.date.Date"
)


class Daterange:
    @staticmethod
    def date_range(start: DateType, offset: int) -> typing.List[DateType]:
        """Returns a list of dates between a given start and offset"""
        return [start.add_days(d) for d in range(0, offset)]

    @staticmethod
    def dates_between(start: DateType, end: DateType) -> typing.List[DateType]:
        """Returns a list of dates between a given start and end date"""
        diff = end - start
        days = diff.days + (1 if diff.seconds > 0 else 0)
        return Daterange.date_range(start, offset=days)
