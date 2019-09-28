from ._internal_utils import *


def find_by_rankWeek(w: int, i: int) -> list:
    '''
    功能见 _real_next
    '''
    clas = collection('timetable')
    for k, c in clas.items():
        if k >= i:
            if not isinstance(c, list):
                if c['start'] <= w and c['end'] >= w:
                    return c
            else:
                week = "双周" if w % 2 == 0 else "单周"
                for cla in c:
                    if cla['week'] == week and cla['start'] <= w and cla['end'] >= w:
                        return cla
    else:
        return None


schooltime = []


def load_schooltime(path):
    global schooltime
    n = now_date()
    date_num = n[1] * 100 + n[2]
    sche = '夏季' if date_num > 501 and date_num < 1001 else '冬季'
    ds = load_json(path)
    schooltime = ds.get(sche)


class Timetable:
    '''
    默认返回下一节课
    '''

    def __init__(self, time: tuple = None):
        '''
        参数 time: 第几周/(星期几-1)/时 * 100 + 分
        '''
        if time is None:
            time = now()
        self.week = time[0]
        self.day = time[1]
        self.clock = time[2] * 100 + time[3]
        self.class_ordinal = 0
        self.info = self._getinfo()

    def __repr__(self):
        r = ''
        for k, v in self.__dict__.items():
            r += f'{k} -> {v}\n'
        return r

    def _fake_next(self) -> tuple:
        '''
        假设课程全满, 求出下一节课, 是今天第几节课或明天第一节课\n
        返回 (星期几-1), (第几节课-1)
        '''
        day, clock = self.day, self.clock

        class_ordinal = 0
        for i, t in enumerate(schooltime):
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

    def _real_next(self, day: int, class_ordinal: int):
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
        log('课程排位', i)
        r = find_by_rankWeek(week, i)
        if r is None:
            # 说明是下一周啦~
            self.week += 1
            r = find_by_rankWeek(self.week, 0)
        if r is None:
            # 啊, 下周还是没课? 那应该是没有课了吧~
            return None
        # 取出 排位, 写回 self
        rank_index = r.get('i')
        self.day, self.class_ordinal = str(rank_index + 11)
        return self.query_info(r)

    def _getinfo(self):
        '''
        返回下一节课的 info
        '''
        # 先得出理想情况下的下一节课, 然后求真实的
        fake = self._fake_next()
        return self._real_next(*fake)

    @classmethod
    def query_info(cls, result):
        '''
        根据索引表的结果, 返回 info 表的内容, 并去掉没用的 kv
        '''
        r = result
        # 取出 info id, 以及上课地点
        _id = r.get('info')
        place = r.get('place')
        info = find_by_id('info', _id)
        # clear 一些没用的 items
        useless = ("time_place", "span")
        delkey(info, *useless)
        info["place"] = place
        return info

    @classmethod
    def load(cls, subjects, routine):
        '''
        读取课程信息.
        '''
        # 加载作息
        load_schooltime(routine)
        # 加载 时间索引(timetable), 课程信息(info)
        ds = load_json(subjects)
        for d in ds:
            obj_id = insert('info', d)
            # 建立索引表, 格式如下
            # i -> 十位: (星期几-1), 个位: (第几节-1)
            # start & end -> 开始 & 结束于第几周
            # place -> 上课地点
            # week -> 单周上课还是双周, 默认每周
            for tp in d['time_place']:
                i = week_day_to_num(tp[0]) * 10 + tp[1] - 1
                insert('timetable', dict(
                    i=i,
                    start=d['span'][0],
                    end=d['span'][1],
                    place=tp[2],
                    week=tp[3] if 3 < len(tp) else "每周",
                    info=obj_id,
                ), key=i)
            order_collection('timetable')

    @classmethod
    def now(cls, time=None):
        n = now() if time is None else time
        hm = n[2] * 100 + n[3]
        flag = 0
        for i, t in enumerate(schooltime):
            # 进位
            end_time = t + 140
            if end_time % 100 >= 60:
                end_time += (100-60)
            if hm >= t and hm <= end_time:
                flag = i
                break
        else:
            # 根本没在上课时间段
            return
        # 根据课程排位来找课
        index = n[1] * 10 + flag
        r = find_by_id('timetable', index)
        if r is None:
            return
        # 有些点的课分单双周的话返回的是一个list
        if not isinstance(r, list):
            return cls.query_info(r)
        else:
            week = "双周" if n[0] % 2 == 0 else "单周"
            for c in r:
                if c['week'] == week:
                    return cls.query_info(c)

    @classmethod
    def schooltime(cls, time=None):
        t = time if time is not None else now()
        return pretty_now(t)

    @classmethod
    def debug(cls):
        log('info:', collection('info'))
        log('timetable:', collection('timetable'))
