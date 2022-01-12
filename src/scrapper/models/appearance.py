# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.scrapper.base import Base


class Appearance(Base):
    __tablename__ = 'appearance'

    appearance_id = Column(Integer, primary_key=True)

    player_id = Column(Integer, ForeignKey('player.player_id'))
    player = relationship("Player", backref="appearance")

    club_id = Column(Integer, ForeignKey('club.club_id'))
    club = relationship("Club", backref="appearance")

    league_id = Column(Integer, ForeignKey('league.league_id'))
    league = relationship("League", backref="appearance")

    season_id = Column(Integer, ForeignKey('season.season_id'))
    season = relationship("Season", backref="appearance")

    minutes_played = Column(Integer)
    appearances = Column(Integer)
    lineups = Column(Integer)
    substitute_in = Column(Integer)
    substitute_out = Column(Integer)
    subs_on_bench = Column(Integer)

    def __init__(self, player, club, league, season, minutes_played, appearances, lineups, substitute_in,
                 substitute_out, subs_on_bench):
        self.player = player
        self.club = club
        self.league = league
        self.season = season
        self.minutes_played = minutes_played
        self.appearances = appearances
        self.lineups = lineups
        self.substitute_in = substitute_in
        self.substitute_out = substitute_out
        self.subs_on_bench = subs_on_bench
