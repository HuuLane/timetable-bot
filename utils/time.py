from time import *
from datetime import datetime, timedelta, date


def weeks(day, term_begins=(2019, 9, 2)) -> int:
    '''
    calculate difference between two dates in weeks
    '''
    d1 = date(*term_begins)
    d2 = date(*day)

    monday1 = (d1 - timedelta(days=d1.weekday()))
    monday2 = (d2 - timedelta(days=d2.weekday()))

    return int((monday2 - monday1).days / 7 + 1)


def now() -> tuple:
    '''
    格式:
    第几周/(星期几-1)/时/分
    '''
    t = localtime()
    w = weeks((t.tm_year, t.tm_mon, t.tm_mday))
    return w, t.tm_wday, t.tm_hour, t.tm_min


if __name__ == "__main__":
    n = now()
    print(n)