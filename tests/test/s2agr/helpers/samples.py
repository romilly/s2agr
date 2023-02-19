import json

from s2agr.entities import Paper


def read(filename):
    with open(filename) as f:
        return f.read()


sample_01 = Paper(json.loads(read('test/s2agr/data/samples/sample_01.json')))


sample_01_id = sample_01.paper_id


sample_02 = Paper(json.loads(read('test/s2agr/data/samples/sample_02.json')))


sample_02_id = sample_02.paper_id
