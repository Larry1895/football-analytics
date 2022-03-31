import pandas as pd
from pyvis.network import Network
from scipy.spatial import distance
from sklearn.preprocessing import normalize
from sqlalchemy import text

from src.scrapper.base import Session

net = Network(height='1080px', width='100%', directed=True)
net.repulsion()

session = Session()

sql = text('SELECT player.player_id, player.full_name, rating, potential, value, wage, international_reputation, ' +
           'date_part(\'year\', age(date_of_birth)) as age ' +
           'from player ' +
           'left join player_transfer_data ptd on player.player_id = ptd.player_id '
           + 'Where player.player_id < 300 '
           + 'Order by player.player_id')
result = session.execute(sql).all()

all_player = []
names = []

for row in result:
    one_player = []
    dict_row = dict(row)
    # print(str(dict_row.get('player_id')))

    net.add_node(dict(row).get('player_id'),
                 label=dict_row.get('full_name'),
                 labelHighlightBold=True)

    names.append(dict_row.get('full_name'))
    one_player.append(dict_row.get('rating'))
    one_player.append(dict_row.get('potential'))
    one_player.append(dict_row.get('value'))
    one_player.append(dict_row.get('wage'))
    one_player.append(dict_row.get('age'))
    one_player.append(dict_row.get('international_reputation'))

    sql_attributes = text('select a.name, attribute_value from fifa_player_attribute ' +
                          'left join attribute a on a.attribute_id = fifa_player_attribute.attribute_id ' +
                          'WHERE player_id = ' + str(dict_row.get('player_id')))
    result_attributes = session.execute(sql_attributes).all()
    dict_result_attributes = dict(result_attributes)

    one_player.append(dict_result_attributes.get('crossing'))
    one_player.append(dict_result_attributes.get('finishing'))
    one_player.append(dict_result_attributes.get('heading_accuracy'))
    one_player.append(dict_result_attributes.get('short_passing'))
    one_player.append(dict_result_attributes.get('volleys'))
    one_player.append(dict_result_attributes.get('dribbling'))
    one_player.append(dict_result_attributes.get('curve'))
    one_player.append(dict_result_attributes.get('fk_accuracy'))
    one_player.append(dict_result_attributes.get('long_passing'))
    one_player.append(dict_result_attributes.get('ball_control'))
    one_player.append(dict_result_attributes.get('acceleration'))
    one_player.append(dict_result_attributes.get('sprint_speed'))
    one_player.append(dict_result_attributes.get('agility'))
    one_player.append(dict_result_attributes.get('reactions'))
    one_player.append(dict_result_attributes.get('balance'))
    one_player.append(dict_result_attributes.get('shot_power'))
    one_player.append(dict_result_attributes.get('jumping'))
    one_player.append(dict_result_attributes.get('stamina'))
    one_player.append(dict_result_attributes.get('strength'))
    one_player.append(dict_result_attributes.get('long_shots'))
    one_player.append(dict_result_attributes.get('aggression'))
    one_player.append(dict_result_attributes.get('interceptions'))
    one_player.append(dict_result_attributes.get('positioning'))
    one_player.append(dict_result_attributes.get('vision'))
    one_player.append(dict_result_attributes.get('penalties'))
    one_player.append(dict_result_attributes.get('composure'))
    one_player.append(dict_result_attributes.get('defensive_awareness'))
    one_player.append(dict_result_attributes.get('standing_tackle'))
    one_player.append(dict_result_attributes.get('sliding_tackle'))
    one_player.append(dict_result_attributes.get('gk_diving'))
    one_player.append(dict_result_attributes.get('gk_handling'))
    one_player.append(dict_result_attributes.get('gk_kicking'))
    one_player.append(dict_result_attributes.get('gk_positioning'))
    one_player.append(dict_result_attributes.get('gk_reflexes'))

    all_player.append(one_player)

session.close()

data_df = pd.DataFrame(all_player)

data_transposed_df = data_df.transpose()
data_transposed_scaled_df = pd.DataFrame(normalize(data_transposed_df))
data_scaled_df = data_transposed_scaled_df.transpose()

distance_matrix = []
player_id = 1

for index, player_values in data_scaled_df.iterrows():
    distances_for_one_row = []
    to_player_id = 1

    for index_2, distance_to_player_values in data_scaled_df.iterrows():
        euclidean_distance = distance.euclidean(player_values.values, distance_to_player_values.values)
        distances_for_one_row.append(euclidean_distance)

        # # Set edge
        # net.add_edge(width=euclidean_distance*10,
        #              source=player_id,
        #              to=to_player_id,
        #              physics=False,
        #              color='white')
        to_player_id = to_player_id + 1

    distance_matrix.append(distances_for_one_row)
    player_id = player_id + 1

# print(distance_matrix)

# Distance aller Spieler zu Spieler 0
current_player = 8
to_player_id = 1
for player_distance in distance_matrix[current_player-1]:
    net.add_edge(width=player_distance * 10,
                 source=current_player,
                 to=to_player_id,
                 physics=True,
                 color='white')
    to_player_id = to_player_id + 1

net.show_buttons(filter_=['physics'])
net.show('club_transfer_network.html')
