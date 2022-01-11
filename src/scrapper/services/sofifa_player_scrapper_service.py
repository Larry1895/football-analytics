import re

from numpy.core import long
from sqlalchemy import null

fifa_stats = ['Crossing', 'Finishing', 'Heading Accuracy',
              'Short Passing', 'Volleys', 'Dribbling', 'Curve',
              'Free Kick Accuracy', 'Long Passing', 'Ball Control',
              'Acceleration', 'Sprint Speed', 'Agility', 'Reactions',
              'Balance', 'Shot Power', 'Jumping', 'Stamina', 'Strength',
              'Long Shots', 'Aggression', 'Interceptions', 'Positioning',
              'Vision', 'Penalties', 'Composure', 'Marking', 'Standing Tackle',
              'Sliding Tackle', 'GK Diving', 'GK Handling', 'GK Kicking',
              'GK Positioning', 'GK Reflexes']


# Get club transfers for player
def find_player_club_transfers(soup):
    player_data = {}
    transfers = {}

    attribute_header = "Transfers"
    blocks = soup.find_all('div', {'class': 'card double-spacing'})
    for block in blocks:
        header = block.find('h5')
        if header:
            if header.text == attribute_header:
                rows = block.find_all('tr')
                # Check if the player has yet made any transfers
                if rows:
                    number_of_transfer = len(rows) - 1
                    for row in rows:
                        colums = row.find_all('td')
                        if colums:
                            # If the Club cannot be found. For example Juventus because of denied rights 2021
                            if (colums[0].find('a') is not None and colums[1].find('a') is not None) \
                                    and (colums[0].find('a') != colums[1].find('a')):
                                transfer = {}
                                transfer['club_from'] = colums[0].find('a').text
                                transfer['club_to'] = colums[1].find('a').text
                                transfer['date'] = colums[3].text

                                fee_string = colums[2].text
                                if has_numbers(fee_string):
                                    transfer['fee'] = extract_numeric_value(fee_string)
                                    transfer['fee_currency'] = extract_currency(fee_string)
                                    transfer['loan'] = False
                                elif fee_string == 'loan':
                                    transfer['fee'] = 0.0
                                    transfer['fee_currency'] = '€'
                                    transfer['loan'] = True
                                else:
                                    transfer['fee'] = 0.0
                                    transfer['fee_currency'] = '€'
                                    transfer['loan'] = False

                                transfers[number_of_transfer] = transfer
                                number_of_transfer = number_of_transfer - 1

                                if number_of_transfer == 0:
                                    first_transfer = {}
                                    first_transfer['club_from'] = 'Youth / Amateurs'
                                    first_transfer['club_to'] = colums[0].find('a').text
                                    first_transfer['date'] = None
                                    first_transfer['fee'] = 0.0
                                    first_transfer['fee_currency'] = '€'
                                    first_transfer['loan'] = False
                                    transfers[number_of_transfer] = first_transfer

                            else:
                                number_of_transfer = number_of_transfer - 1

                # if the player has not yet made any transfers
                else:
                    side_nav = soup.find('div', {'class': 'col col-4'})
                    side_nav_cards = side_nav.find_all('div', {'class': 'card player-card grey'})

                    # if the player has currently a club, where he is playing.
                    # Clubs that are not listed in FIFA will be excluded, e.g. Al Ain FC.
                    if len(side_nav_cards) > 1:
                        first_transfer = {}
                        first_transfer['club_from'] = 'Youth / Amateurs'
                        first_transfer['club_to'] = side_nav_cards[1].find('a').text
                        first_transfer['date'] = None
                        first_transfer['fee'] = 0.0
                        first_transfer['fee_currency'] = '€'
                        first_transfer['loan'] = False
                        transfers[0] = first_transfer

    player_data['transfer_history'] = transfers
    return player_data


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


# Get Player infos like eg. name, nationality and positions
def find_player_info(soup):
    player_data = {}
    player_data['image'] = soup.find('img')['data-src']
    player_data['full_name'] = soup.find('h1').text.split(' (')[0]
    player_data['nationality'] = soup.find('a')['title'].strip()
    player_data['pref_pos'] = soup.find('span', {'class': 'pos'}).text.strip()

    info_line = soup.find('div', {'class': 'meta ellipsis'}).text
    start_dob = info_line.find('y.o.') - 2
    player_data['all_pref_pos'] = info_line[0:start_dob].strip().replace(' ', ', ')

    # Remove positions
    info_line = info_line[start_dob:len(info_line)]

    # Extract date of birth
    dob = re.search('(\(.*)\)', info_line).group(0)
    player_data['dob'] = dob.replace('(', '').replace(')', '')
    infos = info_line.replace(dob + ' ', '').split(' ')

    player_data['age'] = infos[0].replace('y.o.', '')
    player_data['height'] = infos[1].replace('cm', '')
    player_data['weight'] = infos[2].replace('kg', '')
    return player_data


# Get Fifa rating, potential rating, transfer value and wage
def find_player_stats(soup):
    player_data = {}
    sections = soup.find('section', {'class': 'card spacing'})
    blocks = sections.find_all('div', {'class': 'block-quarter'})

    player_data['rating'] = int(blocks[0].find('span').text)
    player_data['potential'] = int(blocks[1].find('span').text)
    player_data['value'] = extract_numeric_value(blocks[2].find('div').text.replace('Value', ''))
    player_data['value_currency'] = extract_currency(blocks[2].find('div').text)
    player_data['wage'] = extract_numeric_value(blocks[3].find('div').text.replace('Wage', ''))
    player_data['wage_currency'] = extract_currency(blocks[3].find('div').text)
    return player_data


def extract_currency(text):
    if '£' in text:
        return '£'
    elif '$' in text:
        return '$'
    else:
        return '€'


def extract_numeric_value(text):
    text = text.upper()
    text = text.replace('€', '')
    text = text.replace('£', '')
    text = text.replace('$', '')
    pre_decimal_place = '0'
    decimal_place = '0'

    if 'M' in text:
        decimal_place = '000000'
        text = text.replace('M', '')

    elif 'K' in text:
        decimal_place = '000'
        text = text.replace('K', '')

    if '.' in text:
        split = text.split('.')
        pre_decimal_place = split[0]
        decimal_place = split[1] + decimal_place[len(split[1]):len(decimal_place)]
    else:
        pre_decimal_place = text

    return float(pre_decimal_place + decimal_place)


def find_player_secondary_info(soup):
    player_data = {}
    player_data['pref_foot'] = soup.find('label', text='Preferred Foot') \
        .parent.contents[2].strip('\n ')

    player_data['international_reputation'] = soup.find('label', text='International Reputation') \
        .parent.text.strip('\n ')

    player_data['club'] = soup.find_all('ul')[1].find('a').text
    player_data['club_pos'] = soup.find('label', text='Position') \
        .parent.find('span').text
    player_data['club_jersey'] = soup.find('label', text='Jersey number') \
        .parent.contents[2].strip('\n ')
    if soup.find('label', text='Joined'):
        player_data['club_joined'] = soup.find('label', text='Joined') \
            .parent.contents[2].strip('\n ')
    player_data['contract_valid'] = soup.find(
        'label', text='Contract valid until') \
        .parent.contents[2].strip('\n ')
    if len(soup.find_all('ul')) > 2:
        player_data['country'] = soup.find_all('ul')[2].find('a').text
    return player_data


# Get Fifa traits and attributes
def find_fifa_info(soup):
    player_data = {'traits': ""}
    attributes = {}
    attribute_header = ["Attacking", "Skill", "Movement", "Power", "Mentality", "Defending", "Goalkeeping"]
    blocks = soup.find_all('div', {'class': 'block-quarter'})
    for block in blocks:
        header = block.find('h5')
        if header:
            if header.text in attribute_header:
                lis = block.find_all('li')
                for li in lis:
                    attribute_value = int(li.find('span', {'class': 'p'}).text)
                    attribute_name = li.text[li.text.index(' '):len(li.text)].strip().lower().replace(' ', '_')
                    attributes[attribute_name] = attribute_value

            elif 'Traits' in header.text:
                lis = block.find_all('li')
                traits = ""
                for li in lis:
                    traits = traits + ", " + li.text.strip()

                if traits.startswith(','):
                    traits = traits[1:len(traits)].strip()

                player_data['traits'] = traits

            elif 'Profile' in header.text:
                li_id = block.find('label', text='ID').parent
                player_data['sofifa_id'] = li_id.text.replace('ID', '').strip()

                li_foot = block.find('label', text='Preferred Foot').parent
                player_data['preferred_foot'] = li_foot.text.replace('Preferred Foot', '').strip()

                player_data['international_reputation'] = block.find('label', text='International Reputation') \
                    .parent.text.split(' ')[0]

    player_data['attributes'] = attributes
    return player_data
