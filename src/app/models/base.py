"""
    Base ORM class, that will store all ORM meta information.
"""

from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    """
        ORM base-class with all DB meta information
    """
