__all__ = ['insert', 'order_collection', 'find_by_id', 'collection']

db = dict()


def obj_id() -> str:
    import uuid
    return str(uuid.uuid4())


def insert(collection: str, document: dict, key=None):
    '''
    insert one ducument(dict) into collection
    return ObjectId
    '''
    c = collection
    _id = key if key is not None else obj_id()
    if db.get(c, None) is None:
        # 新建一个表
        db[c] = dict()
    if db[c].get(_id, None) is None:
        # 新建一条记录
        db[c][_id] = document
    else:
        # 之前有记录, 则转化为 list 并 push 进去
        # 而一个点只有两种情况, '单周' '双周'
        db[c][_id] = [db[c][_id], document]
    return _id


def order_collection(c: str):
    from collections import OrderedDict
    db[c] = OrderedDict(sorted(db[c].items()))


def find_by_id(collection: str, _id: str) -> dict:
    r = db[collection].get(_id, None)
    if r is not None:
        return r.copy()


def collection(c: str):
    return db[c]
