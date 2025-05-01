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
