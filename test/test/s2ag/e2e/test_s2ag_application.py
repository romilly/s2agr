import unittest

from s2ag.librarian import Librarian


class S2AGTestCase(unittest.TestCase):
    def test_librarian_retrieves_unknown_paper(self):
        librarian = Librarian()
        pid = '649def34f8be52c8b66281af98ae884c09aef38b'
        paper = librarian.get_paper(pid)
        self.assertEqual(paper.paper_id, pid)
        self.assertEqual(paper.title, "Construction of the Literature Graph in Semantic Scholar")


if __name__ == '__main__':
    unittest.main()
