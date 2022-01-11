# coding=utf-8

from sqlalchemy import Column, String, Integer

from src.scrapper.base import Base


class Nation(Base):
    __tablename__ = 'nation'

    nation_id = Column(Integer, primary_key=True)
    full_name = Column(String)
    abbreviation = Column(String)

    def __init__(self, full_name, abbreviation):
        self.full_name = full_name
        self.abbreviation = abbreviation
