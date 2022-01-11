# coding=utf-8
from src.scrapper.base import Session
from src.scrapper.models.attribute import Attribute


def save_or_update_attribute_by_name(new_attribute: Attribute):
    session = Session()

    record: Attribute = session.query(Attribute) \
        .filter(Attribute.name.ilike(new_attribute.name)) \
        .one_or_none()

    if record is None:
        # Save
        record = new_attribute
        session.add(record)

    session.commit()
    session.close()
    return record
