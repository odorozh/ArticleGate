"""
    ORM logic for 'article_to_author' table.
"""

from sqlalchemy import Column, Integer, String
from .base import BaseModel


class ArticleToAuthorModel(BaseModel):
    """
        Model of bindings between scientific paper (article)
        and one of its authors.
    """

    __tablename__ = "article_to_author"

    doi = Column(String, primary_key=True)
    author_id = Column(Integer, nullable=False)
    place = Column(Integer, nullable=False)
