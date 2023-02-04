from unittest import TestCase

from hamcrest import assert_that, equal_to
from psycopg2.sql import SQL, Identifier


from psycopg2.extensions import connection, cursor

from s2ag.persistence.database_catalogue import test_connection, DatabaseCatalogue, count_rows


class DatabaseTest(TestCase):
    connection: connection
    cursor: cursor
    TABLES = ['paper', 'citation', 'author']

    @classmethod
    def setUpClass(cls):
        cls.connection = test_connection()
        cls.cursor = cls.connection.cursor()
        cls.connection.commit()

    @classmethod
    def tearDownClass(cls):
        cls.cursor.close()
        del cls.cursor
        cls.connection.close()
        del cls.connection

    def setUp(self):
        self.catalogue = DatabaseCatalogue(test_connection())
        for table in reversed(self.TABLES):
            self.delete_all_rows_from(table)

    def tearDown(self):
        self.catalogue.close()

    # noinspection SqlWithoutWhere
    def delete_all_rows_from(self, *tables):
        for table in tables:
            self.cursor.execute(SQL("delete from ")+Identifier(table))
        self.connection.commit()

    def check_row_count(self, table, id_col, value, expected_count):
        count = count_rows(self.cursor, id_col, table, value)
        assert_that(count, equal_to(expected_count))

    def check_total_row_count(self, table, expected_count):
        self.cursor.execute(
            SQL("select count(*) from ") +(Identifier(table)))
        rs = self.cursor.fetchall()
        assert_that(rs[0][0], equal_to(expected_count))



