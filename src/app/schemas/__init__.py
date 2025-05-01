"""
    Pydentic schemas for handlers parameters.
"""

from pydantic import BaseModel as PDBaseModel, ValidationError, field_validator


class IdGetSchema(PDBaseModel):
    id: int

    @field_validator('id', mode='after')
    @classmethod
    def ge(cls, value: int) -> int:
        if value < 0:
            raise ValueError(f'{value} is less than zero')
        return value


class AuthorGetSchema(IdGetSchema):
    pass


class ArticleGetSchema(PDBaseModel):
    doi: str


class OrganisationGetSchema(IdGetSchema):
    pass
