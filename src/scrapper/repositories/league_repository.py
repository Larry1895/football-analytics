# coding=utf-8
from src.scrapper.base import Session
from src.scrapper.models.league import League


def save_or_update_league(new_league: League):
    session = Session()

    record: League = session.query(League) \
        .filter(League.full_name == new_league.full_name) \
        .one_or_none()

    if record is None:
        # Save
        record = new_league
        session.add(record)

    session.commit()
    session.close()
    return record
