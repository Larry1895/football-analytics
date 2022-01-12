# coding=utf-8
from src.scrapper.base import Session
from src.scrapper.models.season import Season


def save_or_update_season(new_season: Season):
    session = Session()

    record: Season = session.query(Season) \
        .filter(Season.start_year == new_season.start_year) \
        .filter(Season.end_year == new_season.end_year) \
        .one_or_none()

    if record is None:
        # Save
        record = new_season
        session.add(record)

    session.commit()
    session.close()
    return record
