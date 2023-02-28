import json
import os
import pathlib
import psycopg2
from psycopg2.sql import SQL, Identifier

from s2agr.citation import Citation
from s2agr.entities import Paper, Author
from s2agr.persistence.catalogue import Catalogue
from s2agr.persistence.parser import get_connection_string

env_loc = os.path.join(pathlib.Path(__file__).parent.resolve(), '.env')


class DatabaseCatalogueException(Exception):
    pass


def test_connection():
    return psycopg2.connect(
        get_connection_string('TEST_DB', env_loc))


def local_production_connection():
    return psycopg2.connect(
        get_connection_string('LOCAL_PROD_DB', env_loc))


def production_connection():
    return psycopg2.connect(
        get_connection_string('PROD_DB', env_loc))


def count_rows(cursor, id_col, table, value):
    # noinspection SyntaxError
    s = SQL("select count(*) from {table} where {field} = %s").format(
        table=Identifier(table),
        field=Identifier(id_col))
    cursor.execute(
        s,
        (value,))
    return cursor.fetchall()[0][0]


class DatabaseCatalogue(Catalogue):
    INSERT_PAPER_SQL = "INSERT into paper(s2ag_json_text, title, pub_year, pdf_url, paper_id)" \
                       " VALUES (%s, %s, %s, %s, %s) ON CONFLICT (paper_id) DO"\
                       " UPDATE SET (s2ag_json_text, title, pub_year, pdf_url, updated)" \
                       " = (EXCLUDED.s2ag_json_text, EXCLUDED.title, EXCLUDED.pub_year, EXCLUDED.pdf_url, DEFAULT)"
    INSERT_AUTHOR_SQL = "INSERT into author(author_id, s2ag_json_text, author_name)" \
                        " VALUES (%s, %s, %s) ON CONFLICT DO NOTHING"
    COUNT_SQL = "select count(paper_id) from paper where paper_id = (%s)"
    SELECT_SQL = "select s2ag_json_text from paper where paper_id = (%s)"
    PAPER_IDS_SQL = "select paper_id from paper"
    INSERT_CITATION_SQL = "INSERT into citation(citing_id, cited_id, is_influential)" \
                          " VALUES(%s, %s, %s) ON CONFLICT (citing_id, cited_id) DO" \
                          " UPDATE SET is_influential = EXCLUDED.is_influential"
    INSERT_WROTE_SQL = "INSERT into wrote(paper_id, author_id) VALUES(%s, %s)" \
                       "ON CONFLICT DO NOTHING"

    def __init__(self, connection=None):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def set_pdf_location(self, paper_id: str, pdf_location: str):
        pass

    def write_paper(self, paper: Paper):
        self._write_paper(paper.paper_id,
                          json.dumps(paper.jason_dictionary),
                          paper.title,
                          paper.year,
                          paper.pdf_url,
                          )

    def write_author(self, author):
        self._write_author(author.author_id,
                           json.dumps(author.jason_dictionary),
                           author.name
                           )

    def write_wrote(self, paper_id, author_id):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(self.INSERT_WROTE_SQL,
                               (paper_id, author_id))
                self.connection.commit()
            except Exception as e:
                self.connection.rollback()
                raise DatabaseCatalogueException from e

    def write_citation(self, citation: Citation):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(self.INSERT_CITATION_SQL,
                               (citation.citing_id, citation.cited_id, citation.is_influential))
                self.connection.commit()
            except Exception as e:
                self.connection.rollback()
                raise DatabaseCatalogueException from e


    def _write_paper(self,
                     paper_id: str,
                     paper_json_text: str,
                     title=None,
                     year=None,
                     pdf_url=None,
                     ):
        with self.connection.cursor() as cursor:
            cursor.execute(self.INSERT_PAPER_SQL, (paper_json_text, title, year, pdf_url, paper_id))
            self.connection.commit()

    def _write_author(self, author_id: str,
                      author_json_text: str,
                      name: str):
        with self.connection.cursor() as cursor:
            cursor.execute(self.INSERT_AUTHOR_SQL, (author_id,
                                                    author_json_text,
                                                    name))
            self.connection.commit()

    def read_json(self, table: str, id_col: str, item_id: str):
        # noinspection SyntaxError
        s = SQL("select s2ag_json_text from {table} where {field} = %s").format(
            table=Identifier(table),
            field=Identifier(id_col))
        self.cursor.execute(s, (item_id,))
        data = self.cursor.fetchone()
        return data[0]

    def knows(self, item_id: str, table: str, id_col: str):
        count = count_rows(self.cursor, id_col, table, item_id)
        return count == 1

    def close(self):
        self.connection.close()

    def read_paper(self, paper_id: str) -> Paper:
        return Paper(self.read_json('paper', 'paper_id', paper_id))

    def read_author(self, author_id):
        return Author(self.read_json('author', 'author_id', author_id))

    def paper_ids(self):
        self.cursor.execute(self.PAPER_IDS_SQL)
        data = self.cursor.fetchall()
        return [row[0] for row in data]

    def query(self, sql, *parameters):
        self.cursor.execute(sql, parameters)
        data = self.cursor.fetchall()
        return (row for row in data)

    def total_row_count_for(self, table):
        self.cursor.execute(
            SQL("select count(*) from ") + (Identifier(table)))
        actual_count = self.cursor.fetchall()[0][0]
        return actual_count



