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


class AuthorIdSchema(IdGetSchema):
    pass


class ArticleDOISchema(PDBaseModel):
    doi: str


class OrganisationIdSchema(IdGetSchema):
    pass


class ArticleAuthorBindingSchema(PDBaseModel):
    doi: str
    place: int

    @field_validator('place', mode='after')
    @classmethod
    def validate_place(cls, place: int) -> int:
        if place < 1:
            raise ValueError(f'{place} is less than 1')
        return place
