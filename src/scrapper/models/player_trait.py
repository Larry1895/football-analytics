# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.scrapper.base import Base


class PlayerTrait(Base):
    __tablename__ = 'fifa_player_trait'

    player_trait_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.player_id'))
    player = relationship("Player", backref="fifa_player_trait")

    trait_id = Column(Integer, ForeignKey('trait.trait_id'))
    trait = relationship("Trait", backref="fifa_player_trait")

    fifa_scrapper_execution_id = Column(Integer, ForeignKey('fifa_scrapper_execution.fifa_scrapper_execution_id'))
    fifa_scrapper_execution = relationship("FifaScrapperExecution", backref="fifa_player_trait")

    def __init__(self, player, trait, fifa_scrapper_execution):
        self.player = player
        self.trait = trait
        self.fifa_scrapper_execution = fifa_scrapper_execution
