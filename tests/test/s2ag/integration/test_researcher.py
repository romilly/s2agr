import unittest

import requests

from s2ag.researcher import Researcher, Retriever


class WebRetriever(Retriever):
    def get_paper_json(self, pid) -> dict:
        url = self.paper_url_for(pid)
        response = requests.get(url)
        return response.json()

    @staticmethod
    def paper_url_for(pid):
        return f"https://api.semanticscholar.org/graph/v1/paper/{pid}"


class ResearcherTestCase(unittest.TestCase):
    def test_researcher_can_get_paper_using_api(self):
        pid = '649def34f8be52c8b66281af98ae884c09aef38b'
        researcher = Researcher(WebRetriever())
        paper = researcher.get_paper(pid)
        self.assertEqual(paper.paper_id, pid)


if __name__ == '__main__':
    unittest.main()
