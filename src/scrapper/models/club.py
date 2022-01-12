# coding=utf-8

from sqlalchemy import Column, String, Integer, Boolean

from src.scrapper.base import Base


class Club(Base):
    __tablename__ = 'club'

    club_id = Column(Integer, primary_key=True)
    full_name = Column(String)
    city = Column(String)
    is_professional_club = Column(Boolean)

    def __init__(self, full_name, city, is_professional_club):
        self.full_name = full_name
        self.city = city
        self.is_professional_club = is_professional_club
