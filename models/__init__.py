import json


def load(path):
    """
    从一个文件中载入数据并转化为 list
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            s = f.read()
            print('成功读取课程数据')
            return json.loads(s)
    except FileNotFoundError:
        # 默认 list
        return []


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
    def all(cls) -> list:
        '''
        返回一个 list, 里面是所有实例化的课程
        '''
        modules = load('static/subjects.json')
        subjects = [cls(**m) for m in modules]
        return subjects
