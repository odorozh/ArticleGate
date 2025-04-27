from pydantic import BaseModel

class AuthorModel(BaseModel):
    author_id: int
    name: str
    affiliation_org_id: int | None
