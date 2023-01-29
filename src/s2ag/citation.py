CITATION_FIELDS = [
    'paperId',
    'title',
    'isInfluential'
]


class Citation:
    def __init__(self, cited_id: str, citation: dict):
        self.cited_id = cited_id
        self.is_influential = citation['isInfluential'] if 'isInfluential' in citation else None
        self.citing_id = citation['paperId']
        self.title = citation['title']

    @classmethod
    def create_from(cls, pid, citation: dict):
        cd = citation['citingPaper']
        cd['isInfluential'] = citation['isInfluential']
        return Citation(pid, cd)
