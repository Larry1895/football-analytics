# coding=utf-8
from src.scrapper.base import Session
from src.scrapper.models.appearance import Appearance


def save_or_update_appearance(new_appearance: Appearance):
    session = Session()

    record: Appearance = session.query(Appearance) \
        .filter(Appearance.season_id == new_appearance.season_id) \
        .filter(Appearance.player_id == new_appearance.player_id) \
        .filter(Appearance.club_id == new_appearance.club_id) \
        .filter(Appearance.league_id == new_appearance.league_id) \
        .one_or_none()

    if record is not None:
        # Update
        record.minutes_played = new_appearance.minutes_played or record.minutes_played
        record.appearances = new_appearance.appearances or record.appearances
        record.lineups = new_appearance.lineups or record.lineups
        record.substitute_in = new_appearance.substitute_in or record.substitute_in
        record.substitute_out = new_appearance.substitute_out or record.substitute_out
        record.subs_on_bench = new_appearance.subs_on_bench or record.subs_on_bench
        record.appearance_type = new_appearance.appearance_type or record.appearance_type
    else:
        # Save
        record = new_appearance
        session.add(record)

    session.commit()
    session.close()
    return record
