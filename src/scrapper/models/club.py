# coding=utf-8

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.scrapper.base import Base


class Club(Base):
    __tablename__ = 'club'

    club_id = Column(Integer, primary_key=True)
    full_name = Column(String)
    sofifa_id = Column(String)

    nationality_id = Column(Integer, ForeignKey('nation.nation_id'))
    nationality = relationship("Nation", backref="club")

    city = Column(String)
    is_professional_club = Column(Boolean)

    def __init__(self, full_name, sofifa_id, nationality, city, is_professional_club):
        self.full_name = full_name
        self.sofifa_id = sofifa_id
        self.nationality = nationality
        self.city = city
        self.is_professional_club = is_professional_club
