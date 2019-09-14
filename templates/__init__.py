from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

temp_cache = dict()


def template(filename: str):
    '''
    带有缓存功能的模板
    '''
    # 读取缓存
    t = temp_cache.get(filename, None)
    if t is not None:
        return t
    t = env.get_template(f'{filename}.jinja')
    temp_cache[filename] = t
    return t


def render(filename: str, **kwargs):
    '''
    渲染相应文字
    '''
    t = template(filename)
    return t.render(**kwargs)
