sysconf = {}


def load_conf(file):
    import json
    from os import path
    if not(path.exists(file)):
        print(f"File not found: {file}")
        return {}
    with open(file, 'r') as f:
        js = json.load(f)
    return js


def conv_conf(fm, to={}):
    def __replace(src, to):
        import re
        rtn = src
        for k, v in to.items():
            if isinstance(v, dict):
                rtn = __replace(rtn, v)
            elif isinstance(v, int):
                rtn = re.sub("{{%s}}" % (k), str(v), rtn)
            elif isinstance(v, str):
                rtn = re.sub("{{%s}}" % (k), v, rtn)
        return rtn

    def __replace_dict(fm, to):
        c = fm
        if isinstance(c, dict):
            for k, v in c.items():
                if isinstance(v, dict):
                    v = __replace_dict(v, to)
                elif isinstance(v, list):
                    [__replace_dict(x, to) for x in v]
                elif isinstance(v, str):
                    v = __replace(v, to)
                c[k] = v
        return c
    fm = __replace_dict(fm, to)
    fm = __replace_dict(fm, fm)
    return fm


def add_env(env=[]):
    import os
    for e in env:
        val = os.getenv(f"PY_{e}", None)
        if val != None:
            sysconf[e.lower()] = val
    return sysconf


sysconf = load_conf("./conf/system.json")
sysconf = conv_conf(sysconf)
