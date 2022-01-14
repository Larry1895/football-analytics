# coding=utf-8
from src.scrapper.base import Session
from src.scrapper.models.player_position import PlayerPosition


def save_or_update_player_position(new_player_position: PlayerPosition):
    session = Session()

    record: PlayerPosition = session.query(PlayerPosition) \
        .filter(PlayerPosition.position_id == new_player_position.position.position_id) \
        .filter(PlayerPosition.player_id == new_player_position.player.player_id) \
        .one_or_none()

    if record is not None:
        # Update
        record.is_main_position = new_player_position.is_main_position or record.is_main_position
    else:
        # Save
        record = new_player_position
        session.add(record)

    session.commit()
    session.close()
    return record
