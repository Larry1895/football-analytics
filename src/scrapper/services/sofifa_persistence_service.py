from src.scrapper.models.appearance import Appearance
from src.scrapper.models.attribute import Attribute
from src.scrapper.models.club import Club
from src.scrapper.models.club_league import ClubLeague
from src.scrapper.models.league import League
from src.scrapper.models.nation import Nation
from src.scrapper.models.player import Player
from src.scrapper.models.player_attribute import PlayerAttribute
from src.scrapper.models.player_club_transfer import PlayerClubTransfer
from src.scrapper.models.player_position import PlayerPosition
from src.scrapper.models.player_trait import PlayerTrait
from src.scrapper.models.player_transfer_data import PlayerTransferData
from src.scrapper.models.position import Position
from src.scrapper.models.season import Season
from src.scrapper.models.trait import Trait
from src.scrapper.repositories.appearance_repository import save_or_update_appearance
from src.scrapper.repositories.attribute_repository import save_or_update_attribute_by_name
from src.scrapper.repositories.club_league_repository import save_or_update_club_league
from src.scrapper.repositories.club_repository import save_or_update_club
from src.scrapper.repositories.league_repository import save_or_update_league
from src.scrapper.repositories.nation_repository import save_or_update_nation_by_name
from src.scrapper.repositories.player_attribute_repository import save_or_update_player_attribute
from src.scrapper.repositories.player_club_transfer_repository import save_or_update_player_club_transfer
from src.scrapper.repositories.player_position_repository import save_or_update_player_position
from src.scrapper.repositories.player_repository import save_or_update_player_by_sofifa_id
from src.scrapper.repositories.player_trait_repository import save_or_update_player_trait
from src.scrapper.repositories.player_transfer_data_repository import save_or_update_player_transfer_data
from src.scrapper.repositories.position_repository import save_or_update_position_by_short_name
from src.scrapper.repositories.season_repository import save_or_update_season
from src.scrapper.repositories.trait_repository import save_or_update_trait_by_name


def save_data(player_data, execution):
    nation = Nation(full_name=player_data['nationality'], abbreviation=None)
    saved_nation = save_or_update_nation_by_name(nation)

    player = Player(full_name=player_data['full_name'],
                    short_name=player_data['short_name'],
                    image_link=player_data['image'],
                    date_of_birth=player_data['dob'],
                    nationality=saved_nation,
                    preferred_foot=player_data['preferred_foot'],
                    weight=player_data['weight'],
                    height=player_data['height'],
                    sofifa_id=player_data['sofifa_id'])
    saved_player = save_or_update_player_by_sofifa_id(player)

    save_position_data(player_data, saved_player)
    save_attribute_data(player_data, saved_player, execution)
    save_traits(player_data, saved_player, execution)
    save_transfer_data(player_data, saved_player, execution)
    save_transfer_history(player_data, saved_player)
    save_appearance_and_club_league_data(player_data, saved_player)


def save_appearance_and_club_league_data(player_data, saved_player):
    appearances = player_data['appearances']

    for appearance in appearances:
        if "/" in appearance['season']:
            season_start_year = appearance['season'].split('/')[0].strip()
            season_end_year = appearance['season'].split('/')[1].strip()
        else:
            season_start_year = appearance['season'].strip()
            season_end_year = appearance['season'].strip()

        new_season = Season(start_year=season_start_year,
                            end_year=season_end_year,
                            designation=appearance['season'])
        saved_season = save_or_update_season(new_season)

        new_club = Club(full_name=appearance['team'], city='', is_professional_club=None)
        saved_club = save_or_update_club(new_club)

        new_league = League(full_name=appearance['competition'],
                            nation=None,
                            competition_type=appearance['competition_type'])
        saved_league = save_or_update_league(new_league)

        new_appearance = Appearance(player=saved_player,
                                    club=saved_club,
                                    league=saved_league,
                                    season=saved_season,
                                    minutes_played=appearance['minutes_played'],
                                    appearances=appearance['appearances'],
                                    lineups=appearance['lineups'],
                                    substitute_in=appearance['substitute_in'],
                                    substitute_out=appearance['substitute_out'],
                                    subs_on_bench=appearance['subs_on_bench'])
        save_or_update_appearance(new_appearance)

        new_club_league = ClubLeague(club=saved_club,
                                     league=saved_league,
                                     season=saved_season)
        save_or_update_club_league(new_club_league)


def save_transfer_history(player_data, saved_player):
    transfer_history = player_data['transfer_history']

    for transfer_entry in transfer_history:
        transfer = transfer_history[transfer_entry]

        new_club_from = Club(full_name=transfer['club_from'], city='', is_professional_club=True)
        saved_club_from = save_or_update_club(new_club_from)
        new_club_to = Club(full_name=transfer['club_to'], city='', is_professional_club=True)
        saved_club_to = save_or_update_club(new_club_to)

        new_player_club_transfer = PlayerClubTransfer(from_club=saved_club_from,
                                                      to_club=saved_club_to,
                                                      player=saved_player,
                                                      changed_at=transfer['date'],
                                                      fee=transfer['fee'],
                                                      fee_currency=transfer['fee_currency'],
                                                      is_borrowed=transfer['loan'])
        save_or_update_player_club_transfer(new_player_club_transfer)


def save_transfer_data(player_data, saved_player, execution):
    new_player_transfer_data = PlayerTransferData(player=saved_player,
                                                  rating=player_data['rating'],
                                                  potential=player_data['potential'],
                                                  value=player_data['value'],
                                                  value_currency=player_data['value_currency'],
                                                  wage=player_data['wage'],
                                                  wage_currency=player_data['wage_currency'],
                                                  international_reputation=player_data['international_reputation'],
                                                  fifa_scrapper_execution=execution)
    save_or_update_player_transfer_data(new_player_transfer_data)


def save_attribute_data(player_data, saved_player, execution):
    attributes = player_data['attributes']
    for attribute in attributes:
        new_attribute = Attribute(name=attribute)
        saved_attribute = save_or_update_attribute_by_name(new_attribute)

        new_player_attribute = PlayerAttribute(player=saved_player,
                                               attribute=saved_attribute,
                                               attribute_value=attributes[attribute],
                                               fifa_scrapper_execution=execution)
        save_or_update_player_attribute(new_player_attribute)


def save_traits(player_data, saved_player, execution):
    traits = player_data['traits']
    if traits:
        traits = traits.split(', ')
        for trait in traits:
            new_trait = Trait(name=trait)
            saved_trait = save_or_update_trait_by_name(new_trait)

            new_player_trait = PlayerTrait(player=saved_player, trait=saved_trait, fifa_scrapper_execution=execution)
            save_or_update_player_trait(new_player_trait)


def save_position_data(player_data, saved_player):
    pref_position = Position(full_name=None, short_name=player_data['pref_pos'])
    saved_pref_position = save_or_update_position_by_short_name(pref_position)

    pref_player_position = PlayerPosition(position=saved_pref_position,
                                          player=saved_player,
                                          is_main_position=True)
    save_or_update_player_position(pref_player_position)

    positions = player_data['all_pref_pos'].split(', ')
    for position in positions:
        new_position = Position(full_name=None, short_name=position)
        saved_new_position = save_or_update_position_by_short_name(new_position)
        new_player_position = PlayerPosition(position=saved_new_position,
                                             player=saved_player,
                                             is_main_position=False)
        save_or_update_player_position(new_player_position)
