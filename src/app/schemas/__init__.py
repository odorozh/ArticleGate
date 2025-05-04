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
        """
            Used identifiers must be greater or equal to zero
        """
        if value < 0:
            raise ValueError(f'{value} is less than zero')
        return value


class AuthorIdSchema(IdGetSchema):
    """
        General author identification schema.
    """


class ArticleDOISchema(PDBaseModel):
    """
        General article identification schema.
    """

    doi: str


class OrganisationIdSchema(IdGetSchema):
    """
        General organisation identification schema.
    """


class ArticleAuthorBindingSchema(PDBaseModel):
    """
        Article to author schema for delete handler purpose.
    """

    doi: str
    place: int

    @field_validator('place', mode='after')
    @classmethod
    def validate_place(cls, place: int) -> int:
        """
            Places indexing starts from 1
        """
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
        """
            Check date format
        """
        try:
            datetime.datetime.strptime(pd, "%Y-%m-%d")
            return pd
        except Exception as e:
            raise ValueError('Wrong posting date format') from e


class OrganisationFullSchema(IdGetSchema):
    """
        Organisation schema: all fields.
    """

    title: str
    location: str


class AuthorFullSchema(IdGetSchema):
    """
        Author schema: all fields.
    """

    name: str
    affiliation_org_id: int


class ArticleToAuthorFullSchema(PDBaseModel):
    """
        Article to author all binding fields.
    """

    doi: str
    author_id: int
    place: int

    @field_validator('author_id', mode='after')
    @classmethod
    def ge_author_id(cls, value: int) -> int:
        """
            Author IDs >= 0
        """
        if value < 0:
            raise ValueError(f'Author ID {value} is less than zero')
        return value

    @field_validator('place', mode='after')
    @classmethod
    def ge_place(cls, value: int) -> int:
        """
            Places indexing starts from 1
        """
        if value < 1:
            raise ValueError(f'Place {value} is less than zero')
        return value
