# coding=utf-8
from src.scrapper.base import Session
from src.scrapper.models.club_league import ClubLeague


def save_or_update_club_league(new_club_league: ClubLeague):
    session = Session()

    record: ClubLeague = session.query(ClubLeague) \
        .filter(ClubLeague.season_id == new_club_league.season_id) \
        .filter(ClubLeague.club_id == new_club_league.club_id) \
        .filter(ClubLeague.league_id == new_club_league.league_id) \
        .one_or_none()

    if record is None:
        # Save
        record = new_club_league
        session.add(record)

    session.commit()
    session.close()
    return record
