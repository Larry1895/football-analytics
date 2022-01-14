# coding=utf-8
from sqlalchemy import or_

from src.scrapper.base import Session
from src.scrapper.models.player_club_transfer import PlayerClubTransfer


def find_transfers_for_club(club_id):
    session = Session()

    result = session.query(PlayerClubTransfer) \
        .filter(or_(PlayerClubTransfer.to_club_id == club_id, PlayerClubTransfer.from_club_id == club_id)) \
        .all()

    session.close()
    return result


def save_or_update_player_club_transfer(new_player_club_transfer: PlayerClubTransfer):
    session = Session()
    record: PlayerClubTransfer

    if new_player_club_transfer.changed_at is not None:
        record = session.query(PlayerClubTransfer) \
            .filter(PlayerClubTransfer.player_id == new_player_club_transfer.player.player_id) \
            .filter(PlayerClubTransfer.changed_at == new_player_club_transfer.changed_at) \
            .one_or_none()
    else:
        record = session.query(PlayerClubTransfer) \
            .filter(PlayerClubTransfer.player_id == new_player_club_transfer.player.player_id) \
            .filter(PlayerClubTransfer.changed_at.is_(None)) \
            .one_or_none()

    if record is None:
        # Save
        record = new_player_club_transfer
        session.merge(record)

    session.commit()
    session.close()
    return record
