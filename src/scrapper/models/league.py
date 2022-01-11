# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.scrapper.base import Base


class League(Base):
    __tablename__ = 'league'

    league_id = Column(Integer, primary_key=True)
    full_name = Column(String)
    nation_id = Column(Integer, ForeignKey('nation.nation_id'))
    nation = relationship("Nation", backref="league")

    def __init__(self, full_name, nation):
        self.full_name = full_name
        self.nation = nation
