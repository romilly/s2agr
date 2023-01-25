import unittest

from hamcrest import assert_that, starts_with

from s2ag.librarian import Librarian, Researcher
from s2ag.retriever import WebRetriever


class S2AGTestCase(unittest.TestCase):
    def test_librarian_retrieves_unknown_paper(self):
        retriever = WebRetriever()
        pid = '649def34f8be52c8b66281af98ae884c09aef38b'
        librarian = Librarian(Researcher(retriever))
        paper = librarian.get_paper(pid)
        self.assertEqual(paper.paper_id, pid)
        self.assertEqual(paper.title, "Construction of the Literature Graph in Semantic Scholar")
        assert_that(paper.abstract, starts_with("We describe"))


if __name__ == '__main__':
    unittest.main()
