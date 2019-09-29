from time import *
from datetime import datetime, timedelta, date


def dates_difference(date1, date2):
    d1, d2 = date(*date1), date(*date2)
    diff = d2-d1
    return diff.days


def now_date() -> tuple:
    t = localtime()
    return t.tm_year, t.tm_mon, t.tm_mday


def cet_countdown(time=None, cet_date=(2019, 12, 14)):
    if time is None:
        time = now_date()
    r = dates_difference(time, cet_date)
    return r


if __name__ == "__main__":
    benchmark = [
        (2019, 12, 13),
        (2019, 12, 14),
        (2019, 12, 15),
        now_date(),
    ]

    for b in benchmark:
        r = cet_countdown(b)
        print(r)
