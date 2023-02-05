import unittest

from hamcrest import assert_that, equal_to

from s2ag.entities import Paper, Author
from test.s2ag.helpers.samples import sample_02


class PaperTestCase(unittest.TestCase):
    def test_paper_json_includes_all_author_data(self):
        paper = sample_02()
        authors = paper.authors
        self.assertEqual(2, len(authors))
        first_author = Author(authors[0])
        assert_that(first_author.author_id, equal_to('48446534'))
        assert_that(first_author.name, equal_to('H. Ishimoto'))
        assert_that(first_author.h_index, equal_to(23))


if __name__ == '__main__':
    unittest.main()