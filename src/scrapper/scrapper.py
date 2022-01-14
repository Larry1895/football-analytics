import datetime

import requests
from bs4 import BeautifulSoup as bs

from src.scrapper.models.fifa_scrapper_execution import FifaScrapperExecution
from src.scrapper.repositories.fifa_scrapper_execution_repository import save_new_fifa_scrapper_execution
from src.scrapper.services.sofifa_persistence_service import save_data
from src.scrapper.services.sofifa_player_scrapper_service import find_player_info, find_player_stats, find_fifa_info, \
    find_player_club_transfers, find_player_appearances


def soup_maker(url):
    r = requests.get(url)
    markup = r.content
    soup = bs(markup, 'lxml')
    return soup


def start_execution():
    # Creates an execution object and stores data such as the execution time and the date from which the data is from
    fifa_year_url_param = str(fifa_year) + '0001'
    url = 'http://sofifa.com/players?offset=0&r=' + fifa_year_url_param + '&set=true'
    soup = soup_maker(url)

    h2 = soup.find('h2')
    all_menus = h2.find_all('span', {'class': 'bp3-button-text'})
    data_from_date_string = ''
    for menu in all_menus:
        if 'FIFA' not in menu.text:
            data_from_date_string = menu.text

    execution = FifaScrapperExecution(year_of_fifa=fifa_year,
                                      data_from_timestamp=data_from_date_string,
                                      executed_at=datetime.datetime.now())
    saved_execution = save_new_fifa_scrapper_execution(execution)
    print("Started scrapping FIFA " + str(saved_execution.year_of_fifa) + " data from "
          + str(saved_execution.data_from_timestamp) + " started at " + str(saved_execution.executed_at))
    return saved_execution


def find_first_player_shortname(soup):
    table = soup.find('table', {'class': 'table table-hover persist-area'})
    tbody = table.find('tbody')
    all_a_names = tbody.find_all('a', {'role': 'tooltip'})
    return all_a_names[0].find('div').text


def scrap_data_from_all_player():
    fifa_year_url_param = str(fifa_year) + '0001'
    url = 'http://sofifa.com/players?offset=0&r=' + fifa_year_url_param + '&set=true'
    soup = soup_maker(url)

    first_player_shortname = find_first_player_shortname(soup)
    first_player_shortname_of_site = ""
    offset = 0
    # Iterate over pages till first player is shown again
    while first_player_shortname != first_player_shortname_of_site:
        # scrap data from this site
        print(offset)
        site_url = 'http://sofifa.com/players?offset=' + str(offset) + '&r=' + fifa_year_url_param + '&set=true'
        soup = soup_maker(site_url)
        scrap_data_from_all_player_of_one_page(soup)

        # Find first player from next site
        offset = offset + 60
        next_site_url = 'http://sofifa.com/players?offset=' + str(offset) + '&r=' + fifa_year_url_param + '&set=true'
        next_site_soup = soup_maker(next_site_url)
        first_player_shortname_of_site = find_first_player_shortname(next_site_soup)


def scrap_data_from_all_player_of_one_page(soup):
    table = soup.find('table', {'class': 'table table-hover persist-area'})
    tbody = table.find('tbody')
    all_a_names = tbody.find_all('a', {'role': 'tooltip'})

    # Iterate over all player
    for player in all_a_names:
        final_details = {'short_name': player.find('div').text}

        sofifa_id = player['href'].split('/')[2]

        fifa_year_url_param = str(fifa_year) + '0001'
        url_player_details = 'http://sofifa.com/player/' + sofifa_id + '/' + fifa_year_url_param
        soup_player_details = soup_maker(url_player_details)
        final_details.update(get_player_details(soup_player_details))

        url_player_transfer = 'http://sofifa.com/player/' + sofifa_id + '/live?r=' + fifa_year_url_param + '&set=true'
        soup_player_transfer = soup_maker(url_player_transfer)
        final_details.update(get_player_transfer_data(soup_player_transfer))

        print(final_details)
        save_data(final_details, execution)


def get_player_details(soup):
    all_details = {}
    soup_player_info = soup.find('div', {'class': 'player'})

    all_details.update(find_player_info(soup_player_info))
    all_details.update(find_player_stats(soup_player_info))
    all_details.update(find_fifa_info(soup))
    return all_details


def get_player_transfer_data(soup):
    all_details = {}
    all_details.update(find_player_club_transfers(soup))
    all_details.update(find_player_appearances(soup))
    return all_details


# ------------- MAIN -------------

fifa_year = 22
execution = start_execution()
scrap_data_from_all_player()
