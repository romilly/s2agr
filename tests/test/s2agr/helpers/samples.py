import json

from s2agr.entities import Paper


def read(filename):
    with open(filename) as f:
        return f.read()


def sample_01():
    jd = json.loads(read('test/s2agr/data/samples/sample_01.json'))
    return Paper(jd)


def sample_02():
    jd = json.loads(read('test/s2agr/data/samples/sample_02.json'))
    return Paper(jd)