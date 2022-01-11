# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey, Date, Boolean, Numeric, String
from sqlalchemy.orm import relationship

from src.scrapper.base import Base


class PlayerClubTransfer(Base):
    __tablename__ = 'player_club_transfer'

    id = Column(Integer, primary_key=True)
    from_club_id = Column(Integer, ForeignKey('club.club_id'))
    from_club = relationship("Club", foreign_keys=[from_club_id])

    to_club_id = Column(Integer, ForeignKey('club.club_id'))
    to_club = relationship("Club", foreign_keys=[to_club_id])

    player_id = Column(Integer, ForeignKey('player.player_id'))
    player = relationship("Player", backref="player_club_transfer")

    changed_at = Column(Date)

    fee = Column(Numeric(12, 2))

    fee_currency = Column(String)

    is_borrowed = Column(Boolean)

    def __init__(self, from_club, to_club, player, changed_at, fee, fee_currency, is_borrowed):
        self.from_club = from_club
        self.to_club = to_club
        self.player = player
        self.changed_at = changed_at
        self.fee = fee
        self.fee_currency = fee_currency
        self.is_borrowed = is_borrowed
