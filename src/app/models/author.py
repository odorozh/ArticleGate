"""
    ORM logic for 'author' table.
"""

from pydantic import BaseModel

class AuthorModel(BaseModel):
    """
        Model of author objects.
    """

    author_id: int
    name: str
    affiliation_org_id: int | None
