import json

from s2ag.paper import Paper


class Retriever:
    def get_paper(self, pid):
        js = '{"paperId": "649def34f8be52c8b66281af98ae884c09aef38b",' \
             '"title": "Construction of the Literature Graph in Semantic Scholar"}'
        d = json.loads(js)
        return Paper(d)


class Librarian:
    def __init__(self):
        self.retriever = Retriever()

    def get_paper(self, pid) -> Paper:
        return self.retriever.get_paper(pid)
