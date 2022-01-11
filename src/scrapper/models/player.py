# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from src.scrapper.base import Base


class Player(Base):
    __tablename__ = 'player'

    player_id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)
    image_link = Column(String)
    date_of_birth = Column(Date)
    nationality_id = Column(Integer, ForeignKey('nation.nation_id'))
    nationality = relationship("Nation", backref="player")
    preferred_foot = Column(String)
    weight = Column(Integer)
    height = Column(Integer)
    sofifa_id = Column(Integer)

    def __init__(self, full_name, short_name, image_link, date_of_birth, nationality, preferred_foot, weight, height, sofifa_id):
        self.full_name = full_name
        self.short_name = short_name
        self.image_link = image_link
        self.date_of_birth = date_of_birth
        self.nationality = nationality
        self.preferred_foot = preferred_foot
        self.weight = weight
        self.height = height
        self.sofifa_id = sofifa_id
