CITATION_FIELDS = [
    'paperId',
    'title',
    'isInfluential'
]


class Citation:
    def __init__(self, cited_id: str, citing_id, title: str, is_influential: bool):
        self.cited_id = cited_id
        self.citing_id = citing_id
        self.title = title
        self.is_influential = is_influential

    @classmethod
    def create_citation_from(cls, cited_id, citation: dict):
        cd = citation['citingPaper']
        title = cd['title']
        is_influential = citation['isInfluential'] if 'isInfluential' in citation else None
        citing_id = cd['paperId']
        return Citation(cited_id, citing_id, title, is_influential)

    @classmethod
    def create_reference_from(cls, citing_id, reference: dict):
        cd = reference['citedPaper']
        is_influential = reference['isInfluential'] if 'isInfluential' in reference else None
        title = cd['title']
        cited_id = cd['paperId']
        return Citation(cited_id, citing_id, title, is_influential)

