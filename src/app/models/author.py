"""
    ORM logic for 'author' table.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from .base import BaseModel


class AuthorModel(BaseModel):
    """
        Model of author objects.
    """

    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    affiliation_org_id = Column(String, ForeignKey("organisation.id"), nullable=False)
