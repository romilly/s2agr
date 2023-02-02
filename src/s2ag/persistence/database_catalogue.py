import json
import os
import pathlib
import psycopg2

from s2ag.citation import Citation
from s2ag.paper import Paper
from s2ag.persistence.catalogue import Catalogue
from s2ag.persistence.parser import get_connection_string

env_loc = os.path.join(pathlib.Path(__file__).parent.resolve(), '.env')
def test_connection():
    return psycopg2.connect(
        get_connection_string('TEST_DB', env_loc))


def local_production_connection():
    return psycopg2.connect(
        get_connection_string('LOCAL_PROD_DB', env_loc))


class DatabaseCatalogue(Catalogue):

    INSERT_SQL = "INSERT into paper(paper_id, s2ag_json_text, title, pub_year)" \
                 " VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING"
    COUNT_SQL = "select count(paper_id) from paper where paper_id = (%s)"
    SELECT_SQL = "select s2ag_json_text from paper where paper_id = (%s)"
    PAPER_IDS_SQL = "select paper_id from paper"
    INSERT_CITATION_SQL = "INSERT into citation(citing_id, cited_id, is_influential)" \
                          " VALUES(%s, %s, %s) ON CONFLICT DO NOTHING"

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

    def write_citation(self, citation: Citation):
        with self.connection.cursor() as cursor:
            cursor.execute(self.INSERT_CITATION_SQL, (citation.cited_id, citation.citing_id, citation.is_influential))
            self.connection.commit()

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
        self.cursor.execute(self.SELECT_SQL, (paper_id,))
        data = self.cursor.fetchone()
        return data[0]

    def knows(self, paper_id : str):
        self.cursor.execute(self.COUNT_SQL, (paper_id,))
        data = self.cursor.fetchone()
        return data[0] == 1

    def close(self):
        self.connection.close()

    def read_paper(self, paper_id: str) -> Paper :
        return Paper(self.read_json(paper_id))

    def paper_ids(self):
        self.cursor.execute(self.PAPER_IDS_SQL)
        data = self.cursor.fetchall()
        return [row[0] for row in data]