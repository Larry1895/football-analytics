# coding=utf-8
from src.scrapper.base import Session
from src.scrapper.models.fifa_scrapper_execution import FifaScrapperExecution
from src.scrapper.models.player_trait import PlayerTrait


def save_or_update_player_trait(new_player_trait: PlayerTrait):
    session = Session()

    record: PlayerTrait = session.query(PlayerTrait) \
        .join(PlayerTrait.fifa_scrapper_execution.of_type(FifaScrapperExecution)) \
        .filter(FifaScrapperExecution.data_from_timestamp
                == new_player_trait.fifa_scrapper_execution.data_from_timestamp) \
        .filter(PlayerTrait.player_id == new_player_trait.player_id) \
        .filter(PlayerTrait.trait_id == new_player_trait.trait_id) \
        .one_or_none()

    if record is None:
        # Save
        record = new_player_trait
        session.add(record)

    session.commit()
    session.close()
    return record
