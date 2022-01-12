# coding=utf-8
from src.scrapper.base import Session
from src.scrapper.models.player_transfer_data import PlayerTransferData


def save_or_update_player_transfer_data(new_player_transfer_data: PlayerTransferData):
    session = Session()

    record: PlayerTransferData = session.query(PlayerTransferData) \
        .filter(PlayerTransferData.fifa_scrapper_execution_id == new_player_transfer_data.fifa_scrapper_execution_id) \
        .filter(PlayerTransferData.player_id == new_player_transfer_data.player_id) \
        .one_or_none()

    if record is not None:
        # Update
        record.rating = new_player_transfer_data.rating or record.rating
        record.potential = new_player_transfer_data.potential or record.potential
        record.value = new_player_transfer_data.value or record.value
        record.value_currency = new_player_transfer_data.value_currency or record.value_currency
        record.wage = new_player_transfer_data.wage or record.wage
        record.wage_currency = new_player_transfer_data.wage_currency or record.wage_currency
        record.international_reputation = new_player_transfer_data.international_reputation or record.international_reputation
    else:
        # Save
        record = new_player_transfer_data
        session.add(record)

    session.commit()
    session.close()
    return record
