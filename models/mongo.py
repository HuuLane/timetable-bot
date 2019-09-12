from pymongo import MongoClient


def connect(mongodb_name: str) -> MongoClient:
    '''
    连接 mongodb
    '''
    # 连接 mongo 数据库, 主机是本机, 端口是默认的端口
    client = MongoClient('localhost', 27017)
    print('连接数据库成功')

    # 直接这样就使用数据库了，相当于一个字典
    return client[mongodb_name]


db = connect('class')


def insert(document: dict):
    '''
    insert one ducument(dict) into timetable collection
    '''
    db.timetable.insert_one(document)


def find(query: dict = {}, field: dict = None) -> dict:
    '''
    返回一条符合条件的 document
    '''
    if field is not None:
        r = db.timetable.find_one(query, field)
    else:
        r = db.timetable.find_one(query)
    return r
