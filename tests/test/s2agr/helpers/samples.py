import json

from s2agr.entities import Paper, Author


def read(filename):
    with open(filename) as f:
        return f.read()


# Construction of the Literature Graph in Semantic Scholar
paper_01 = Paper(json.loads(read('test/s2agr/data/samples/paper_01.json')))
paper_01_id = paper_01.paper_id


# Molecular and neural mechanisms regulating sexual motivation of virgin female Drosophila
paper_02 = Paper(json.loads(read('test/s2agr/data/samples/paper_02.json')))
paper_02_id = paper_02.paper_id

# Eva Berlot
author_01 = Author(json.loads(read('test/s2agr/data/samples/author_01.json')))
author_01_id = author_01.author_id


