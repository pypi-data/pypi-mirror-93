import datetime as dt


def get_current_datetime():
    return dt.datetime.now(tz=dt.timezone.utc).astimezone()
