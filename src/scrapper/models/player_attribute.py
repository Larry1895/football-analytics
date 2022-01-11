# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.scrapper.base import Base


class PlayerAttribute(Base):
    __tablename__ = 'fifa_player_attribute'

    player_attribute_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.player_id'))
    player = relationship("Player", backref="fifa_player_attribute")

    attribute_id = Column(Integer, ForeignKey('attribute.attribute_id'))
    attribute = relationship("Attribute", backref="fifa_player_attribute")

    attribute_value = Column(Integer)

    fifa_scrapper_execution_id = Column(Integer, ForeignKey('fifa_scrapper_execution.fifa_scrapper_execution_id'))
    fifa_scrapper_execution = relationship("FifaScrapperExecution", backref="fifa_player_attribute")

    def __init__(self, player, attribute, attribute_value, fifa_scrapper_execution):
        self.player = player
        self.attribute = attribute
        self.attribute_value = attribute_value
        self.fifa_scrapper_execution = fifa_scrapper_execution
