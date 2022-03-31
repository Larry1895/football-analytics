from src.scrapper.models.club import Club
from src.scrapper.models.nation import Nation
from src.scrapper.repositories.club_repository import save_or_update_club
from src.scrapper.repositories.nation_repository import save_or_update_nation_by_name


def save_team_data(team_data, execution):
    nation = Nation(full_name=team_data['country'], abbreviation=None)
    saved_nation = save_or_update_nation_by_name(nation)

    new_club = Club(full_name=team_data['name'],
                    sofifa_id=team_data['sofifa_id'],
                    nationality=saved_nation,
                    city='',
                    is_professional_club=None)
    saved_club = save_or_update_club(new_club)
