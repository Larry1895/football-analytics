# coding=utf-8
from src.scrapper.base import Session
from src.scrapper.models.trait import Trait


def save_or_update_trait_by_name(new_trait: Trait):
    session = Session()

    record: Trait = session.query(Trait) \
        .filter(Trait.name.ilike(new_trait.name)) \
        .one_or_none()

    if record is None:
        # Save
        record = new_trait
        session.add(record)

    session.commit()
    session.close()
    return record
