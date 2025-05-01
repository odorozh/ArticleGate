"""
    ORM logic for 'organisation' table.
"""

from sqlalchemy import Column, Integer, String
from .base import BaseModel

class OrganisationModel(BaseModel):
    """
        Model of (scientific) organisation objects.
    """

    __tablename__ = "organisation"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    location = Column(String, nullable=True)
