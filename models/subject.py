import json
from models.mongo import insert, find, drop, find_by_id
from utils import *


def load(path) -> list:
    """
    从一个文件中载入数据并转化为 list
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            s = f.read()
            print(f'读取{path}数据')
            return json.loads(s)
    except FileNotFoundError:
        # 默认 list
        return []


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


def find_by_rankWeek(w: int, i: int) -> list:
    '''
    功能见 _real_next
    '''
    week = "双周" if w % 2 == 0 else "单周"
    return list(find('timetable', {
        'i': {"$gte": i, },
        "start": {"$lte": w},
        "end": {"$gte": w},
        "$or": [{"week": week}, {"week": "每周"}],
    }, mult=True, sort='i'))


schooltime_cache = []


def schooltime() -> list:
    r = schooltime_cache
    if len(r) > 0:
        return r
    # 第一次运行, 载入到内存
    d = list(filter(lambda d: d.get('title', None) ==
                    "夏季", load('static/routine.json')))[0]
    r = d.get('schooltime')
    _schooltime = r
    return r


class Subject:
    def __init__(self, time: tuple):
        '''
        参数 time: 第几周/(星期几-1)/时/分
        '''
        self.week = time[0]
        self.day = time[1]
        self.clock = time[2] * 100 + time[3]
        self.class_ordinal = 0
        self.info = self.__getinfo()

    def __fake_next(self) -> tuple:
        '''
        假设课程全满, 求出下一节课, 是今天第几节课或明天第一节课\n
        返回 (星期几-1), (第几节课-1)
        '''
        day, clock = self.day, self.clock

        class_ordinal = 0
        for i, t in enumerate(schooltime()):
            if clock < t:
                class_ordinal = i
                break
        else:
            # 返回下一个工作日的第一节课..
            day = day + 1
            # 礼拜六或礼拜天就改为礼拜一, 周数加一
            if (day + 1) == 6 or 7:
                self.week += 1
                day = 0
        return day, class_ordinal

    def __real_next(self, day: int, class_ordinal: int):
        '''
        接收 '下一节课' (星期几-1, 第几节课-1)
        将其转化为 课程排位(数据库索引), 寻找大于等于它的第一个存在
        若不存在, 设课程排位为0, 重新搜索.
        返回一个 含有课程信息的 dict,
        如果没课了 返回 None
        '''
        week = self.week
        # 转化成课程表时间索引
        i = day * 10 + class_ordinal
        print('课程排位', i)
        r = find_by_rankWeek(week, i)
        if len(r) == 0:
            # 说明是下一周啦~
            self.week += 1
            r = find_by_rankWeek(self.week, 0)
        if len(r) == 0:
            # 啊, 下周还是没课? 那应该是没有课了吧~
            return None
        # 取出 排位, 写回 self
        rank_index = r[0].get('i')
        self.day, self.class_ordinal = str(rank_index + 11)
        # 取出 info id, 以及上课地点
        obj_id = r[0].get('info')
        place = r[0].get('place')
        info = find_by_id('info', obj_id)
        # clear 一些没用的 items
        useless = ("time_place", "span", "_id")
        delkey(info, *useless)
        info["place"] = place
        return info

    def __getinfo(self):
        '''
        返回下一节课的 info
        '''
        # 先得出理想情况下的下一节课, 然后求真实的
        fake = self.__fake_next()
        return self.__real_next(*fake)

    @classmethod
    def update(cls):
        '''
        读取 json, 删除之前的所有数据后写入数据库.
        写入 时间索引(timetable), 课程信息(info)
        '''
        drop('timetable', 'info')

        ds = load('static/subjects.json')
        for d in ds:
            obj_id = insert('info', d)
            # 建立索引表, 格式如下
            # i -> 十位: (星期几-1), 个位: (第几节-1)
            # start & end -> 开始 & 结束于第几周
            # place -> 上课地点
            # week -> 单周上课还是双周
            for tp in d['time_place']:
                i = week_day_to_num(tp[0]) * 10 + tp[1] - 1
                insert('timetable', dict(
                    i=i,
                    start=d['span'][0],
                    end=d['span'][1],
                    place=tp[2],
                    week=tp[3] if 3 < len(tp) else "每周",
                    info=str(obj_id),
                ))
