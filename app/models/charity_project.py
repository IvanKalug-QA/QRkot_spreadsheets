
from sqlalchemy import (
    Column, String, Text)

from app.models.base import AbstractBase


class CharityProject(AbstractBase):
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
