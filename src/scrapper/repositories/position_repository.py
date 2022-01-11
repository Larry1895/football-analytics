# coding=utf-8
from pprint import pprint

from sqlalchemy import text

from src.scrapper.base import Session
from src.scrapper.models.position import Position


def find_number_of_players_per_position():
    session = Session()

    sql = text('SELECT position.short_name AS PositionName, count(pp) AS NumberOfPlayer ' +
               'FROM  position ' +
               'LEFT JOIN player_position pp on position.position_id = pp.position_id ' +
               'WHERE pp.is_main_position = true ' +
               'GROUP BY position.short_name ' +
               'ORDER BY count(pp)')
    result = session.execute(sql).fetchall()

    session.close()
    return result


def save_or_update_position_by_short_name(new_position: Position):
    session = Session()

    record: Position = session.query(Position) \
        .filter(Position.short_name.ilike(new_position.short_name)) \
        .one_or_none()

    if record is not None:
        # Update
        record.full_name = new_position.full_name or record.full_name
        record.short_name = new_position.short_name or record.short_name
    else:
        # Save
        record = new_position
        session.add(record)

    session.commit()
    session.close()
    return record
