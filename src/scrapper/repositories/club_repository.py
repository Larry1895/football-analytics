# coding=utf-8

from src.scrapper.base import Session
from src.scrapper.models.club import Club


def save_or_update_club(new_club: Club):
    session = Session()

    record: Club = session.query(Club) \
        .filter(Club.full_name.ilike(new_club.full_name)) \
        .one_or_none()

    if record is None:
        # Save
        record = new_club
        session.add(record)

    session.commit()
    session.close()
    return record
