import unittest

from hamcrest import assert_that, equal_to

from s2agr.persistence.parser import parse


class EnvParsingTestCase(unittest.TestCase):
    def test_parses_dbmate_environment_variable(self):
        env = "postgres://fred:secret_pw@127.0.0.1/test_db?sslmode=disable"
        expected = ('fred', 'secret_pw', '127.0.0.1', 'test_db')
        assert_that(parse(env), equal_to(expected))  # add assertion here


if __name__ == '__main__':
    unittest.main()
