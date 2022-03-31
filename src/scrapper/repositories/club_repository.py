# coding=utf-8

from src.scrapper.base import Session
from src.scrapper.models.club import Club


def save_or_update_club(new_club: Club):
    session = Session()

    record: Club = session.query(Club) \
        .filter(Club.full_name.ilike(new_club.full_name)) \
        .one_or_none()

    if record is not None:
        # Update
        record.sofifa_id = new_club.sofifa_id or record.sofifa_id
        record.nationality = new_club.nationality or record.nationality
        record.city = new_club.city or record.city
        record.is_professional_club = new_club.is_professional_club or record.is_professional_club
    else:
        # Save
        record = new_club
        session.add(record)

    session.commit()
    session.close()
    return record
