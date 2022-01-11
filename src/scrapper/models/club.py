# coding=utf-8

from sqlalchemy import Column, String, Integer

from src.scrapper.base import Base


class Club(Base):
    __tablename__ = 'club'

    club_id = Column(Integer, primary_key=True)
    full_name = Column(String)
    city = Column(String)

    def __init__(self, full_name, city):
        self.full_name = full_name
        self.city = city
