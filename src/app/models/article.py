"""
    ORM logic for 'article' table.
"""

from pydantic import BaseModel

class ArticleModel(BaseModel):
    """
        Model of article objects.
    """

    doi: str
    title: str
    posting_date: str
