# coding=utf-8

from sqlalchemy import Column, String, Integer

from src.scrapper.base import Base


class Trait(Base):
    __tablename__ = 'trait'

    trait_id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name
