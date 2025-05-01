"""
    ORM logic for 'article' table.
"""

from sqlalchemy import Column, String
from .base import BaseModel

class ArticleModel(BaseModel):
    """
        Model of article objects.
    """

    __tablename__ = "article"

    doi = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    posting_date = Column(String, nullable=False)
