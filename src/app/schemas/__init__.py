"""
    Pydentic schemas for handlers parameters.
"""

import datetime
from pydantic import BaseModel as PDBaseModel, field_validator


class IdGetSchema(PDBaseModel):
    """
        Basic id > 0 validation schema.
    """

    id: int

    @field_validator('id', mode='after')
    @classmethod
    def ge(cls, value: int) -> int:
        if value < 0:
            raise ValueError(f'{value} is less than zero')
        return value


class AuthorIdSchema(IdGetSchema):
    """
        General author identification schema.
    """

    pass


class ArticleDOISchema(PDBaseModel):
    """
        General article identification schema.
    """

    doi: str


class OrganisationIdSchema(IdGetSchema):
    """
        General organisation identification schema.
    """

    pass


class ArticleAuthorBindingSchema(PDBaseModel):
    """
        Article to author schema for delete handler purpose.
    """

    doi: str
    place: int

    @field_validator('place', mode='after')
    @classmethod
    def validate_place(cls, place: int) -> int:
        if place < 1:
            raise ValueError(f'{place} is less than 1')
        return place


class ArticleFullSchema(PDBaseModel):
    """
        Article schema: all fields.
    """

    doi: str
    title: str
    posting_date: str

    @field_validator('posting_date', mode='after')
    @classmethod
    def validate_place(cls, pd: str) -> int:
        try:
            datetime.datetime.strptime(pd, "%Y-%m-%d")
            return pd
        except Exception as _:
            raise ValueError(f'Wrong posting date format')


class OrganisationFullSchema(IdGetSchema):
    """
        Organisation schema: all fields.
    """

    title: str
    location: str


class AuthorFullSChema(IdGetSchema):
    """
        Author schema: all fields.
    """

    name: str
    affiliation_org_id: int
