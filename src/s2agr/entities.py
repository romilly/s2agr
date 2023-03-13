import re
from datetime import datetime
from typing import Any, List

CC_RE = pattern = re.compile(r'(?<!^)(?=[A-Z])')

AUTHOR_FIELDS = [
    'authorId',
    'externalIds',
    'url',
    'name',
    'aliases',
    'affiliations',
    'homepage',
    'paperCount',
    'citationCount',
    'hIndex'
]

BASE_PAPER_FIELDS = [
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
        ]

EXTENDED_PAPER_FIELDS = BASE_PAPER_FIELDS + [f'authors.{subfield}' for subfield in AUTHOR_FIELDS]
PAPER_FIELDS_WITH_CITATIONS = BASE_PAPER_FIELDS + ['citations', 'references']


def snake(name: str) -> str:
    return CC_RE.sub('_', name).lower()


class JsonEntity:
    def __init__(self, jason_dictionary: dict):
        self.jason_dictionary = jason_dictionary
        for key in self.jason_dictionary.keys():
            self.__setattr__(snake(key), self.jason_dictionary[key])


class Paper(JsonEntity):
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
    open_access_pdf: dict
    pdf_url: str
    fields_of_study: Any
    s2_fields_of_study: Any
    publication_venue: Any
    publication_types: Any
    publication_date: datetime
    citationStyles: Any
    authors: Any
    citations: List[dict]
    references: List[dict]

    def __init__(self, jason_dictionary: dict):
        JsonEntity.__init__(self, jason_dictionary )
        if 'isOpenAccess' not in jason_dictionary:
            self.is_open_access = False
        if 'title' not in jason_dictionary:
            self.title = None
        if 'year' not in jason_dictionary:
            self.year = None
        if 'authors' not in jason_dictionary:
            self.authors = []
        self.pdf_url = self.open_access_pdf['url'] if self.is_open_access else None


class Author(JsonEntity):
    author_id: str
    external_ids: Any
    url: str
    name: str
    aliases: Any
    affiliations: List[str]
    homepage: str
    paper_count: int
    citation_count: int
    h_index: int
