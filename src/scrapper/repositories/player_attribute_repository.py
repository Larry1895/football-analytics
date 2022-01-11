# coding=utf-8
from src.scrapper.base import Session
from src.scrapper.models.fifa_scrapper_execution import FifaScrapperExecution
from src.scrapper.models.player_attribute import PlayerAttribute


def save_or_update_player_attribute(new_player_attribute: PlayerAttribute):
    session = Session()

    record: PlayerAttribute = session.query(PlayerAttribute) \
        .join(PlayerAttribute.fifa_scrapper_execution.of_type(FifaScrapperExecution)) \
        .filter(FifaScrapperExecution.data_from_timestamp
                == new_player_attribute.fifa_scrapper_execution.data_from_timestamp) \
        .filter(PlayerAttribute.player_id == new_player_attribute.player_id) \
        .filter(PlayerAttribute.attribute_id == new_player_attribute.attribute_id) \
        .one_or_none()

    if record is None:
        # Save
        record = new_player_attribute
        session.add(record)

    session.commit()
    session.close()
    return record
