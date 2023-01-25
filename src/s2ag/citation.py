CITATION_FIELDS = [
    'paperId',
    'title',
    'isInfluential'
]


class Citation:
    def __init__(self, cited_id: str, citation: dict):
        self.cited_id = cited_id
        self.is_influential = citation['isInfluential']
        citing_paper = citation['citingPaper']
        self.citing_id = citing_paper['paperId']
        self.title = citing_paper['title']
