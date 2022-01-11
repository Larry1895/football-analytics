# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship

from src.scrapper.base import Base


class PlayerTransferData(Base):
    __tablename__ = 'player_transfer_data'

    player_transfer_data_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.player_id'))
    player = relationship("Player", backref="player_transfer_data")

    rating = Column(Integer)
    potential = Column(Integer)
    value = Column(Numeric(12, 2))
    value_currency = Column(String)
    wage = Column(Numeric(12, 2))
    wage_currency = Column(String)
    international_reputation = Column(Integer)

    fifa_scrapper_execution_id = Column(Integer, ForeignKey('fifa_scrapper_execution.fifa_scrapper_execution_id'))
    fifa_scrapper_execution = relationship("FifaScrapperExecution", backref="player_transfer_data")

    def __init__(self, player, rating, potential, value, value_currency, wage, wage_currency, international_reputation, fifa_scrapper_execution):
        self.player = player
        self.rating = rating
        self.potential = potential
        self.value = value
        self.value_currency = value_currency
        self.wage = wage
        self.wage_currency = wage_currency
        self.international_reputation = international_reputation
        self.fifa_scrapper_execution = fifa_scrapper_execution
