# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.scrapper.base import Base


class ClubLeague(Base):
    __tablename__ = 'club_league'

    id = Column(Integer, primary_key=True)
    club_id = Column(Integer, ForeignKey('club.club_id'))
    club = relationship("Club", backref="club_league")

    league_id = Column(Integer, ForeignKey('league.league_id'))
    league = relationship("League", backref="club_league")

    season_id = Column(Integer, ForeignKey('season.season_id'))
    season = relationship("Season", backref="club_league")

    def __init__(self, club, league, season):
        self.club = club
        self.league = league
        self.season = season
