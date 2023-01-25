from abc import ABC, abstractmethod

import requests


class Retriever(ABC):
    @abstractmethod
    def get_paper_json(self, pid) -> dict:
        pass


class WebRetriever(Retriever):
    def get_paper_json(self, pid) -> dict:
        url = self.paper_url_for(pid)
        response = requests.get(url)
        return response.json()

    @staticmethod
    def paper_url_for(pid):
        return f"https://api.semanticscholar.org/graph/v1/paper/{pid}?fields=title,abstract"
