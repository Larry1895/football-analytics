# coding=utf-8

from src.scrapper.base import Session
from src.scrapper.models.player import Player


def save_or_update_player_by_sofifa_id(new_player: Player):
    session = Session()

    record: Player = session.query(Player) \
        .filter(Player.sofifa_id == new_player.sofifa_id) \
        .one_or_none()

    if record is not None:
        # Update
        record.full_name = new_player.full_name or record.full_name
        record.short_name = new_player.short_name or record.short_name
        record.image_link = new_player.image_link or record.image_link
        record.date_of_birth = new_player.date_of_birth or record.date_of_birth
        record.nationality = new_player.nationality or record.nationality
        record.preferred_foot = new_player.preferred_foot or record.preferred_foot
        # record.weight = new_player.weight or record.weight
        # record.height = new_player.height or record.height
    else:
        # Save
        record = new_player
        session.add(record)

    session.commit()
    session.close()
    return record
