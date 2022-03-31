from _plotly_utils.colors.sequential import Turbo
from pyvis.network import Network
from sqlalchemy import text

from src.scrapper.base import Session

# Jede Node stellt einen Verein dar
# (Evtl. einen Cycling Graphen nehmen)
# Ein Kante gerichtet ist der Transferweg zu einem anderen Verein
# Farbe des Pfeils färbt sich je nach durchschnittlich bezahlter Preis pro Spieler
# Die Farbe der Node entspricht der Nation(Liga macht keinen Sinn,
# da die Vereine zwischenzeitlich die Ligen gewechselt haben könnten)
# Die größe der Node sollte zwischen 0-1 liegen und stellt dar: ...
net = Network(height='1080px', width='100%', directed=True)
net.repulsion(node_distance=1000,
              central_gravity=0.2,
              spring_length=30000,
              spring_strength=0.05,
              damping=0.09)

session = Session()
sql_all_clubs = text('SELECT club_id, full_name, nationality_id, '

                     + 'coalesce(number_of_to_transfers, 0) as number_of_to_transfers, '
                     + 'coalesce(number_of_from_transfers, 0) as number_of_from_transfers '
                     + 'FROM club club '
                     + 'LEFT JOIN '
                     + '(SELECT c_to.club_id as to_club_id, COUNT(*) as number_of_to_transfers, c_to.is_professional_club '
                     + 'FROM player_club_transfer pct '
                     + 'LEFT JOIN club c_to on c_to.club_id = pct.to_club_id '
                     + 'WHERE c_to.is_professional_club = TRUE AND fee != 0 '
                     + 'GROUP BY c_to.club_id) as to_club_infos on to_club_infos.to_club_id = club_id '
                     + 'LEFT JOIN '
                     + '(SELECT c_from.club_id as from_club_id, COUNT(*) as number_of_from_transfers, c_from.is_professional_club '
                     + 'FROM player_club_transfer pct '
                     + 'LEFT JOIN club c_from on c_from.club_id = pct.from_club_id '
                     + 'WHERE c_from.is_professional_club = TRUE AND fee != 0 '
                     + 'GROUP BY c_from.club_id) as from_club_infos on from_club_infos.from_club_id = club_id  '
                     + 'WHERE (number_of_to_transfers > 0 OR number_of_from_transfers > 0) '
                     + 'AND club.is_professional_club = TRUE')
result_all_clubs = session.execute(sql_all_clubs).all()

# Erstelle für jeden Verein eine Node
for row in result_all_clubs:
    net.add_node(dict(row).get('club_id'),
                 dict(row).get('full_name'),
                 labelHighlightBold=True,
                 group=dict(row).get('nationality_id'),
                 size=(int(dict(row).get('number_of_to_transfers')) + int(
                     dict(row).get('number_of_from_transfers'))) * 10
                 )

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

colors = Turbo
for row in result_all_transfers:
    x = float(dict(row).get('avg_fee_per_transfer'))
    if x <= 50000:
        color = colors[0]
    elif x <= 100000:
        color = colors[1]
    elif x <= 250000:
        color = colors[2]
    elif x <= 500000:
        color = colors[3]
    elif x <= 750000:
        color = colors[4]
    elif x <= 1000000:
        color = colors[5]
    elif x <= 2500000:
        color = colors[6]
    elif x <= 5000000:
        color = colors[7]
    elif x <= 7500000:
        color = colors[8]
    elif x <= 10000000:
        color = colors[9]
    elif x <= 50000000:
        color = colors[10]
    else:
        color = colors[11]

    net.add_edge(weight=.87,
                 source=dict(row).get('from_club_id'),
                 to=dict(row).get('to_club_id'),
                 title=str(dict(row).get('avg_fee_per_transfer')) + ' average €: from ' + str(
                     dict(row).get('from_club_id')) + ' to ' + str(dict(row).get('to_club_id')),
                 color=color)

net.set_options('var options = "nodes": {'
                + '"font": {'
                + '"size": 120'
                + '}}')

# populates the nodes and edges data structures
# net.show_buttons(filter_=['physics'])

net.show('club_transfer_network.html')
