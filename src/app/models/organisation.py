"""
    ORM logic for 'organisation' table.
"""

from pydantic import BaseModel

class OrganisationModel(BaseModel):
    """
        Model of (scientific) organisation objects.
    """

    org_id: int
    title: str
    location: str | None
