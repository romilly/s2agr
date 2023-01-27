import json

from psycopg2._psycopg import connection

from s2ag.paper import Paper
from s2ag.persistence.catalogue import Catalogue
from s2ag.persistence.parser import get_connection_string


def test_connection():
    return connection(
        get_connection_string('TEST_DB', '/home/romilly/git/active/s2ag/sql/.env'))


class DatabaseCatalogue(Catalogue):

    INSERT_SQL = "INSERT into paper(paper_id, s2ag_json_text, title, pub_year)" \
                 " VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING"
    COUNT_SQL = "select count(paper_id) from paper where paper_id = '%s'"
    SELECT_SQL = "select s2ag_json_text from paper where paper_id = '%s'"

    def __init__(self, connection=None):
        self.connection = connection
        self.cursor = self.connection.cursor()


    def set_pdf_location(self, paper_id: str, pdf_location: str):
        pass

    def write_paper(self, paper: Paper):
        self._write(paper.paper_id,
                    json.dumps(paper.jason_dictionary),
                    paper.authors,
                    paper.title,
                    paper.year,
                    )

    def _write(self, paper_id : str,
               paper_json_text : str,
               authors,
               title = None,
               year = None,
               ):
        with self.connection.cursor() as cursor:
            cursor.execute(self.INSERT_SQL, (paper_id, paper_json_text, title, year))
            self.connection.commit()

    def read_json(self, paper_id : str):
        self.cursor.execute(self.SELECT_SQL % paper_id)
        data = self.cursor.fetchone()
        return data[0]

    def knows(self, paper_id : str):
        self.cursor.execute(self.COUNT_SQL % paper_id)
        data = self.cursor.fetchone()
        return data[0] == 1

    def close(self):
        self.connection.close()

    def read_paper(self, paper_id: str) -> Paper :
        return Paper(self.read_json(paper_id))