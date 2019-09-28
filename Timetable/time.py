__all__ = ['now', 'day_num_to_cn', 'pretty_now', 'now_date', 'week_day_to_num']

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


def now_date() -> tuple:
    t = localtime()
    return t.tm_year, t.tm_mon, t.tm_mday


def now() -> tuple:
    '''
    相对于开学
    格式:
    第几周/(星期几-1)/时/分
    '''
    t = localtime()
    w = weeks((t.tm_year, t.tm_mon, t.tm_mday))
    return w, t.tm_wday, t.tm_hour, t.tm_min


week_cn = ('一', '二', '三', '四', '五', '六', '天')


def week_day_to_num(day: str) -> int:
    d = dict(
        mon=0,
        tue=1,
        wed=2,
        thu=3,
        fri=4,
        sat=5,
        sun=6
    )
    return d.get(day, 0)


def day_num_to_cn(num: int) -> str:
    return week_cn[num]


def pretty_now(now: tuple) -> tuple:
    h = str(now[2]).zfill(2)
    m = str(now[3]).zfill(2)
    return now[0], day_num_to_cn(now[1]), h, m


if __name__ == "__main__":
    n = pretty_now(now())
    print(n)
