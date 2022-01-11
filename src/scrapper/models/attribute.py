# coding=utf-8

from sqlalchemy import Column, String, Integer

from src.scrapper.base import Base


class Attribute(Base):
    __tablename__ = 'attribute'

    attribute_id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name
