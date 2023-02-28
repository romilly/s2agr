import unittest

from hamcrest import assert_that, equal_to

from s2agr.batch import batch


class MyTestCase(unittest.TestCase):
    def test_batch_returns_short_list(self):
        values = ['Car', 'Horse']
        batches = list(batch(values, batch_size=3))
        assert_that(batches, equal_to([['Car', 'Horse']]))

    def test_batch_returns_longer_list(self):
        values = ['Car', 'Horse', 'Hen', 'Dog']
        batches = list(batch(values, batch_size=3))
        assert_that(batches, equal_to([['Car', 'Horse', 'Hen'],['Dog']]))

    def test_batch_returns_multiple_lists(self):
        values = ['Car', 'Horse', 'Hen', 'Dog', 'Sheep']
        batches = list(batch(values, batch_size=2))
        assert_that(batches, equal_to([['Car', 'Horse'], ['Hen', 'Dog'], ['Sheep']]))


if __name__ == '__main__':
    unittest.main()
