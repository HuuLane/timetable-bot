import json
from models.mongo import insert, find, drop


def load(path):
    """
    从一个文件中载入数据并转化为 list
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            s = f.read()
            print('读取课程数据')
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


class Subject:
    def __init__(self, **kwargs):
        '''
        格式:
        name(课程名) -> 统一建模语言uml
        teacher -> xx
        time_place(时间地点) -> [['Mon.', 3, 'a301'], ['Wed.', 2, 'a301']]
        span(哪几周) -> {'start': 1, 'end': 12}
        '''
        for k, v in kwargs.items():
            setattr(self, k, v)

    def info(self):
        for k, v in self.__dict__.items():
            print(f'{k} -> {v}')

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
            # 建立时间索引
            # 格式为 十位: (星期几-1), 个位: 第几节
            for tp in d['time_place']:
                i = week_day_to_num(tp[0]) * 10 + tp[1]
                insert('timetable', dict(
                    i=i,
                    info=str(obj_id),
                ))

    @classmethod
    def next(cls, time: tuple):
        '''
        查看下一节课
        time: 第几周/(星期几-1)/时/分
        '''
        pass

    @classmethod
    def all(cls) -> list:
        '''
        返回一个 list, 里面是所有实例化的课程
        '''
        modules = load('static/subjects.json')
        subjects = [cls(**m) for m in modules]
        return subjects
