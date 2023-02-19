import unittest

from hamcrest import assert_that, equal_to

from s2agr.entities import Author
from test.s2agr.helpers.samples import sample_02


class PaperTestCase(unittest.TestCase):
    def test_paper_json_includes_all_author_data(self):
        authors = sample_02.authors
        self.assertEqual(2, len(authors))
        first_author = Author(authors[0])
        assert_that(first_author.author_id, equal_to('48446534'))
        assert_that(first_author.name, equal_to('H. Ishimoto'))
        assert_that(first_author.h_index, equal_to(23))


if __name__ == '__main__':
    unittest.main()
