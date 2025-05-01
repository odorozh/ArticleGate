"""
    Base ORM class, that will store all ORM meta information.
"""

from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    pass