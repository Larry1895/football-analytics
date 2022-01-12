# coding=utf-8

from sqlalchemy import Column, Integer, String

from src.scrapper.base import Base


class Season(Base):
    __tablename__ = 'season'

    season_id = Column(Integer, primary_key=True)
    start_year = Column(Integer)
    end_year = Column(Integer)
    designation = Column(String)

    def __init__(self, start_year, end_year, designation):
        self.start_year = start_year
        self.end_year = end_year
        self.designation = designation
