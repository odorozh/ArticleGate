from pydantic import BaseModel

class OrganisationModel(BaseModel):
    org_id: int
    title: str
    location: str | None
