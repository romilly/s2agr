from abc import abstractmethod, ABC

from s2ag.paper import Paper


class Retriever(ABC):
    @abstractmethod
    def get_paper_json(self, pid) -> dict:
        pass


class Researcher:
    def __init__(self, retriever: Retriever):
        self.retriever = retriever

    def get_paper(self, pid):
        return Paper(self.retriever.get_paper_json(pid))
