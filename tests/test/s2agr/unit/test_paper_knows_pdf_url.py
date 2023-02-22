import unittest

from s2agr.entities import Paper
from test.s2agr.helpers.samples import paper_01


class PaperPdfTestCase(unittest.TestCase):
    def test_paper_knows_pdf_url(self):
        paper = paper_01
        self.assertEqual(paper.pdf_url,
                         'https://www.aclweb.org/anthology/N18-3011.pdf')


if __name__ == '__main__':
    unittest.main()
