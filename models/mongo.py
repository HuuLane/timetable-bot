from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId


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


def insert(collection: str, document: dict):
    '''
    insert one ducument(dict) into collection
    return ObjectId
    '''
    return db[collection].insert_one(document).inserted_id


def find(collection: str, query: dict = {}, field: dict = None, mult=False, sort=False):
    '''
    返回一条符合条件的 document
    '''
    args = (query,) if field is None else (query, field)
    if not mult:
        return db[collection].find_one(*args)
    if not sort:
        return db[collection].find(*args)
    return db[collection].find(*args).sort(sort, ASCENDING)


def find_by_id(collection: str, id: str) -> dict:
    return db[collection].find_one({"_id": ObjectId(id)})


def drop(*collections: str):
    '''
    remove all documents
    '''
    for c in collections:
        db[c].drop()
