import datetime


def get_timezone(timezone: int):
    if timezone == 0:
        return datetime.timezone.utc
    return datetime.timezone(datetime.timedelta(hours=timezone))


def get_datetime(s: str | datetime.datetime | None = None, timezone: int = 8):
    if s is None:
        return datetime.datetime.now(get_timezone(timezone))
    if isinstance(s, datetime.datetime):
        if s.tzinfo is None:
            s = s.replace(tzinfo=get_timezone(timezone))
        return s
    formats = [
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%S.%f%z",
    ]
    for f in formats:
        try:
            dt = datetime.datetime.strptime(s, f)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=get_timezone(timezone))
            return dt
        except ValueError:
            pass
    raise ValueError(f"Invalid time format {s}")


def get_humanize(dt: datetime.datetime, to: datetime.datetime):
    delta = dt - to
    sign = 1 if delta.total_seconds() > 0 else -1
    days = abs(delta.days)
    hours = abs(delta.seconds // 3600)
    minutes = abs(delta.seconds // 60 % 60)
    suffix = "后" if sign == 1 else "前"
    return f"{days}天{hours}小时{minutes}分钟{suffix}"
