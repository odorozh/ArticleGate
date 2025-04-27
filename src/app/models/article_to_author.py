"""
    ORM logic for 'article_to_author' table.
"""

from pydantic import BaseModel, Field

class ArticleToAuthorModel(BaseModel):
    """
        Model of bindings between scientific paper (article)
        and one of its authors.
    """

    doi: str
    author_id: int
    place: int = Field(gt=0)
