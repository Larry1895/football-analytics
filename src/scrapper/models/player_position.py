# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.scrapper.base import Base


class PlayerPosition(Base):
    __tablename__ = 'player_position'

    player_position_id = Column(Integer, primary_key=True)
    position_id = Column(Integer, ForeignKey('position.position_id'))
    position = relationship("Position", backref="player_position")

    player_id = Column(Integer, ForeignKey('player.player_id'))
    player = relationship("Player", backref="player_position")

    is_main_position = Column(Boolean)

    def __init__(self, position, player, is_main_position):
        self.position = position
        self.player = player
        self.is_main_position = is_main_position
