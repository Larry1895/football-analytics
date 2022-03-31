import matplotlib.pyplot as plt
import networkx as nx
from sqlalchemy import text

from src.scrapper.base import Session

colors = {
    '#000000', '#FFFF00', '#1CE6FF', '#FF34FF', '#FF4A46', '#008941', '#006FA6', '#A30059',
    '#FFDBE5', '#7A4900', '#0000A6', '#63FFAC', '#B79762', '#004D43', '#8FB0FF', '#997D87',
    '#5A0007', '#809693', '#FEFFE6', '#1B4400', '#4FC601', '#3B5DFF', '#4A3B53', '#FF2F80',
    '#61615A', '#BA0900', '#6B7900', '#00C2A0', '#FFAA92', '#FF90C9', '#B903AA', '#D16100',
    '#DDEFFF', '#000035', '#7B4F4B', '#A1C299', '#300018', '#0AA6D8', '#013349', '#00846F',
    '#372101', '#FFB500', '#C2FFED', '#A079BF', '#CC0744', '#C0B9B2', '#C2FF99', '#001E09',
    '#00489C', '#6F0062', '#0CBD66', '#EEC3FF', '#456D75', '#B77B68', '#7A87A1', '#788D66',
    '#885578', '#FAD09F', '#FF8A9A', '#D157A0', '#BEC459', '#456648', '#0086ED', '#886F4C',

    '#34362D', '#B4A8BD', '#00A6AA', '#452C2C', '#636375', '#A3C8C9', '#FF913F', '#938A81',
    '#575329', '#00FECF', '#B05B6F', '#8CD0FF', '#3B9700', '#04F757', '#C8A1A1', '#1E6E00',
    '#7900D7', '#A77500', '#6367A9', '#A05837', '#6B002C', '#772600', '#D790FF', '#9B9700',
    '#549E79', '#FFF69F', '#201625', '#72418F', '#BC23FF', '#99ADC0', '#3A2465', '#922329',
    '#5B4534', '#FDE8DC', '#404E55', '#0089A3', '#CB7E98', '#A4E804', '#324E72', '#6A3A4C',
    '#83AB58', '#001C1E', '#D1F7CE', '#004B28', '#C8D0F6', '#A3A489', '#806C66', '#222800',
    '#BF5650', '#E83000', '#66796D', '#DA007C', '#FF1A59', '#8ADBB4', '#1E0200', '#5B4E51',
    '#C895C5', '#320033', '#FF6832', '#66E1D3', '#CFCDAC', '#D0AC94', '#7ED379', '#012C58'
}

# Jede Node stellt einen Verein dar
# Ein Kante gerichtet ist der Transferweg zu einem anderen Verein
# Farbe des Pfeils färbt sich je nach durchschnittlich bezahlter Preis pro Spieler
# Die Farbe der Node entspricht der Nation(Liga macht keinen Sinn,
# da die Vereine zwischenzeitlich die Ligen gewechselt haben könnten)
# Die größe der Node sollte zwischen 0-1 liegen und stellt dar: ...
G = nx.Graph()

# some labels
labels = []

session = Session()
sql_all_clubs = text('SELECT club_id, full_name, nationality_id '
                     + 'FROM club '
                     + 'WHERE is_professional_club = TRUE')
result_all_clubs = session.execute(sql_all_clubs).all()

# Erstelle für jeden Verein eine Node
for row in result_all_clubs:
    G.add_node(dict(row).get('club_id'),
               # {"color": colors[int(dict(row).get('nationality_id'))]}
               )
    labels.append(dict(row).get('full_name'))

sql_all_transfers = text('SELECT c_from.club_id as from_club_id, c_from.full_name as from_full_name, '
                         + 'c_to.club_id as to_club_id, c_to.full_name as to_full_name, '
                         + 'avg(pct.fee) avg_fee_per_transfer '
                         + 'FROM player_club_transfer pct '
                         + 'LEFT JOIN club c_from on c_from.club_id = pct.from_club_id '
                         + 'LEFT JOIN club c_to on c_to.club_id = pct.to_club_id '
                         + 'WHERE (c_to.is_professional_club = TRUE AND c_from.is_professional_club = TRUE) '
                         + 'AND fee != 0 '
                           'GROUP BY c_from.club_id, c_to.club_id')
result_all_transfers = session.execute(sql_all_transfers).all()
session.close()

for row in result_all_transfers:
    G.add_edge(dict(row).get('from_club_id'), dict(row).get('to_club_id'))

plt.figure(1, figsize=(32, 24))
nx.circular_layout(G, scale=0.5, dim=2)
nx.draw_circular(G,
                 edge_color='#909090',
                 node_size=50,
                 arrows=True
                 # labels=labels
                 )
plt.show()
