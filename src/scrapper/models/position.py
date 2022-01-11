# coding=utf-8

from sqlalchemy import Column, String, Integer

from src.scrapper.base import Base


class Position(Base):
    __tablename__ = 'position'

    position_id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)

    def __init__(self, full_name, short_name):
        self.full_name = full_name
        self.short_name = short_name
