from pydantic import BaseModel

class ArticleModel(BaseModel):
    doi: str
    title: str
    posting_date: str
