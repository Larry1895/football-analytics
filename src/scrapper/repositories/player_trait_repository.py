# coding=utf-8
from src.scrapper.base import Session
from src.scrapper.models.player_trait import PlayerTrait


def save_or_update_player_trait(new_player_trait: PlayerTrait):
    session = Session()

    record: PlayerTrait = session.query(PlayerTrait) \
        .filter(PlayerTrait.fifa_scrapper_execution_id == new_player_trait.fifa_scrapper_execution.fifa_scrapper_execution_id) \
        .filter(PlayerTrait.player_id == new_player_trait.player.player_id) \
        .filter(PlayerTrait.trait_id == new_player_trait.trait.trait_id) \
        .one_or_none()

    if record is None:
        # Save
        record = new_player_trait
        session.add(record)

    session.commit()
    session.close()
    return record
