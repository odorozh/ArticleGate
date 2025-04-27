from pydantic import BaseModel, Field

class ArticleToAuthorModel(BaseModel):
    doi: str
    author_id: int
    place: int = Field(gt=0)
