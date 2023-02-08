import re
from datetime import datetime
from typing import Any, List, Generator

from s2agr.citation import Citation

CC_RE = pattern = re.compile(r'(?<!^)(?=[A-Z])')


def snake(name: str) -> str:
    return CC_RE.sub('_', name).lower()


class JsonEntity:
    def __init__(self, jason_dictionary: dict):
        self.jason_dictionary = jason_dictionary
        for key in self.jason_dictionary.keys():
            self.__setattr__(snake(key), self.jason_dictionary[key])


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
        'authors.authorId',
        'authors.url',
        'authors.name',
        'authors.aliases',
        'authors.affiliations',
        'authors.homepage',
        'authors.paperCount',
        'authors.citationCount',
        'authors.hIndex'
        ])


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
    open_access_pdf: str
    fields_of_study: Any
    s2_fields_of_study: Any
    publication_venue: Any
    publication_types: Any
    publication_date: datetime
    citationStyles: Any
    authors: Any
    citations: List[dict]


AUTHOR_FIELDS = ','.join([
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
])


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
