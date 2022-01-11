# coding=utf-8

from src.scrapper.base import Session
from src.scrapper.models.fifa_scrapper_execution import FifaScrapperExecution


def save_new_fifa_scrapper_execution(new_execution: FifaScrapperExecution):
    session = Session()

    record: FifaScrapperExecution = session.query(FifaScrapperExecution) \
        .filter(FifaScrapperExecution.year_of_fifa == new_execution.year_of_fifa) \
        .filter(FifaScrapperExecution.data_from_timestamp == new_execution.data_from_timestamp) \
        .one_or_none()

    if record is not None:
        # Update
        record.data_from_timestamp = new_execution.data_from_timestamp or record.data_from_timestamp
    else:
        # Save
        record = new_execution
        session.add(record)

    session.expunge(record)
    session.commit()
    session.close()
    return record
