# coding=utf-8
from src.scrapper.base import Session
from src.scrapper.models.nation import Nation


def save_or_update_nation_by_name(new_nation: Nation):
    session = Session()

    record: Nation = session.query(Nation) \
        .filter(Nation.full_name.ilike(new_nation.full_name)) \
        .one_or_none()

    if record is not None:
        # Update
        record.full_name = new_nation.full_name or record.full_name
        record.abbreviation = new_nation.abbreviation or record.abbreviation
    else:
        # Save
        record = new_nation
        session.add(record)

    session.commit()
    session.close()
    return record
