import datetime

import pytest

from app.utils.datetime import get_datetime, get_timezone


@pytest.mark.parametrize(
    ["s", "expected"],
    [
        ("2006/01/02 15:04", datetime.datetime(2006, 1, 2, 15, 4, tzinfo=get_timezone(8))),
        ("2006/01/02 15:04:05", datetime.datetime(2006, 1, 2, 15, 4, 5, tzinfo=get_timezone(8))),
        ("2006-01-02 15:04:05", datetime.datetime(2006, 1, 2, 15, 4, 5, tzinfo=get_timezone(8))),
        ("2006-01-02T15:04:05", datetime.datetime(2006, 1, 2, 15, 4, 5, tzinfo=get_timezone(8))),
        ("2006-01-02T15:04:05.123456+08:00", datetime.datetime(2006, 1, 2, 15, 4, 5, 123456, tzinfo=get_timezone(8))),
        ("2006-01-02T15:04:05.123+08:00", datetime.datetime(2006, 1, 2, 15, 4, 5, 123000, tzinfo=get_timezone(8))),
        ("2006-01-02T15:04:05+07:00", datetime.datetime(2006, 1, 2, 15, 4, 5, tzinfo=get_timezone(7))),
    ],
)
def test_get_time(s, expected):
    assert get_datetime(s) == expected
