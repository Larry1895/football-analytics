import datetime

import requests
from bs4 import BeautifulSoup as bs

from src.scrapper.models.fifa_scrapper_execution import FifaScrapperExecution
from src.scrapper.repositories.fifa_scrapper_execution_repository import save_new_fifa_scrapper_execution
from src.scrapper.services.sofifa_team_persistence_service import save_team_data


def soup_maker(url):
    r = requests.get(url)
    markup = r.content
    soup = bs(markup, 'lxml')
    return soup


def start_execution():
    # Creates an execution object and stores data such as the execution time and the date from which the data is from
    fifa_year_url_param = str(fifa_year) + '0001'
    url = 'http://sofifa.com/teams?offset=0&r=' + fifa_year_url_param + '&set=true'
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
    print("Started scrapping team data FIFA " + str(saved_execution.year_of_fifa) + " data from "
          + str(saved_execution.data_from_timestamp) + " started at " + str(saved_execution.executed_at))
    return saved_execution


def find_first_team_shortname(soup):
    table = soup.find('table', {'class': 'table table-hover persist-area'})
    tbody = table.find('tbody')
    all_rows = tbody.find_all('tr')
    name_column = all_rows[0].find('td', {'class': 'col-name-wide'})
    return name_column.find_all('a')[0].find('div').text


def scrap_data_from_all_teams():
    fifa_year_url_param = str(fifa_year) + '0001'
    url = 'http://sofifa.com/teams?offset=0&r=' + fifa_year_url_param + '&set=true'
    soup = soup_maker(url)

    first_team_shortname = find_first_team_shortname(soup)
    first_team_shortname_of_site = ""
    offset = 0
    # Iterate over pages till first player is shown again
    while first_team_shortname != first_team_shortname_of_site:
        # scrap data from this site
        print(offset)
        site_url = 'http://sofifa.com/teams?offset=' + str(offset) + '&r=' + fifa_year_url_param + '&set=true'
        soup = soup_maker(site_url)
        scrap_data_from_all_teams_of_one_page(soup)

        # Find first team from next site
        offset = offset + 60
        next_site_url = 'http://sofifa.com/teams?offset=' + str(offset) + '&r=' + fifa_year_url_param + '&set=true'
        next_site_soup = soup_maker(next_site_url)
        first_team_shortname_of_site = find_first_team_shortname(next_site_soup)


def scrap_data_from_all_teams_of_one_page(soup):
    table = soup.find('table', {'class': 'table table-hover persist-area'})
    tbody = table.find('tbody')

    all_rows = tbody.find_all('tr')

    # Iterate over all player
    for row in all_rows:
        name_column = row.find('td', {'class': 'col-name-wide'})
        team_a = name_column.find_all('a')[0]

        final_details = {'name': team_a.find('div').text,
                         'sofifa_id': team_a['href'].split('/')[2]}

        sofifa_id = team_a['href'].split('/')[2]

        fifa_year_url_param = str(fifa_year) + '0001'
        url_team_details = 'http://sofifa.com/team/' + sofifa_id \
                           + '/?r=' + fifa_year_url_param + '&set=true'
        soup_team_details = soup_maker(url_team_details)
        final_details.update(get_team_details(soup_team_details))

        # url_player_transfer = 'http://sofifa.com/player/' + sofifa_id + '/live?r=' + fifa_year_url_param + '&set=true'
        # soup_player_transfer = soup_maker(url_player_transfer)
        # final_details.update(get_player_transfer_data(soup_player_transfer))

        print(final_details)
        save_team_data(final_details, execution)


def get_team_details(soup):
    all_details = {}

    div_meta = soup.find('div', {'class': 'meta ellipsis'})
    country = div_meta.find('a', {'rel': 'nofollow'})['title']
    all_details['country'] = country

    return all_details


# ------------- MAIN -------------

fifa_year = 22
execution = start_execution()
scrap_data_from_all_teams()
