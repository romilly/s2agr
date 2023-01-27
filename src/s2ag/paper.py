import re
from datetime import datetime
from typing import Any

CC_RE = pattern = re.compile(r'(?<!^)(?=[A-Z])')


def snake(name: str) -> str:
    return CC_RE.sub('_', name).lower()


PAPER_FIELDS = ','.join([
        'paperId',
        'externalIds',
        'url',
        'title',
        'abstract',
        'venue',
        'year',
        'referenceCount',
        'citationCount',
        'influentialCitationCount',
        'isOpenAccess',
        'openAccessPdf',
        'fieldsOfStudy',
        's2FieldsOfStudy',
        'publicationVenue',
        'publicationTypes',
        'publicationDate',
        'journal',
        'citationStyles',
        'authors',
        'citations', # by default, get
        # 'citations.year'
        # 'tldr',
        # 'embedding'
        ])


class Paper:
    paper_id: str
    title: str
    externalIds: Any
    url: str
    abstract: str
    venue: Any
    year: int
    reference_count: int
    citation_count: int
    influential_citation_count: int
    is_open_access: bool
    open_access_pdf: str
    fields_of_study: Any
    s2_fields_of_study: Any
    publication_venue: Any
    publication_types: Any
    publication_date: datetime
    citationStyles: Any
    authors: Any
    # tldr: str
    # embedding: Any

    def __init__(self, jason_dictionary: dict):
        self.jason_dictionary = jason_dictionary
        for key in self.jason_dictionary.keys():
            self.__setattr__(snake(key), self.jason_dictionary[key])
