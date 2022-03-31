import pandas as pd
import plotly.express as px
import plotly.io as pio
from sqlalchemy import text

from src.scrapper.base import Session


def get_traits_for_pos(positions):
    where_statement = ''
    for pos in positions:
        if pos == positions[0]:
            where_statement = where_statement + 'p.short_name = \'' + pos + '\''
        else:
            where_statement = where_statement + 'OR p.short_name = \'' + pos + '\''

    sql = text('SELECT t.trait_id, t.name, '
               + 'COUNT(fpt.player_id) as number_of_traits_per_position '
               + 'from player '
               + 'left join player_transfer_data ptd on player.player_id = ptd.player_id '
               + 'left join fifa_player_trait fpt on player.player_id = fpt.player_id '
               + 'left join trait t on fpt.trait_id = t.trait_id '
               + 'left join player_position pp on player.player_id = pp.player_id '
               + 'left join position p on pp.position_id = p.position_id '
               + 'Where t.trait_id is not null '
               + 'AND (' + where_statement + ') '
               + 'group by t.trait_id, t.name '
               + 'order by t.trait_id')
    return session.execute(sql).all()


def set_values(trait_for_pos, label):
    for trait in traits:
        trait_value = 0
        for row in trait_for_pos:
            dict_row = dict(row)
            if dict_row.get('name') == trait:
                trait_value = int(dict_row.get('number_of_traits_per_position'))

        values.append(trait_value)
        trait_values.append(trait)
        position_cluster.append(label)


# https://stackoverflow.com/questions/50250010/plotly-chart-is-not-displayed-in-pycharm
pio.renderers.default = "browser"

traits = []

session = Session()
traits_sql = text('SELECT trait_id, name ' +
                  'from trait ')
traits_result = session.execute(traits_sql).all()

for row in traits_result:
    dict_row = dict(row)
    traits.append(dict_row.get('name'))

trait_values = []
position_cluster = []
values = []

trait_number_gk = get_traits_for_pos(['GK'])
set_values(trait_number_gk, 'Torwart')

trait_number_gk = get_traits_for_pos(['CB'])
set_values(trait_number_gk, 'Zentrale Verteidigung')

trait_number_gk = get_traits_for_pos(['RB', 'LB', 'RWB', 'LWB'])
set_values(trait_number_gk, 'Außenverteidigung')

trait_number_gk = get_traits_for_pos(['CM', 'CDM'])
set_values(trait_number_gk, 'Zentrales Mittelfeld')

trait_number_gk = get_traits_for_pos(['LM', 'RM', 'LW', 'RW'])
set_values(trait_number_gk, 'Flügelspieler')

trait_number_gk = get_traits_for_pos(['CAM', 'CF', 'ST'])
set_values(trait_number_gk, 'Sturm')

session.close()

correlated_df = pd.DataFrame({
    "traits": trait_values,
    "position_cluster": position_cluster,
    "value": values,
})

# Polar
fig = px.bar(correlated_df,
             x="traits",
             y="value",
             color="position_cluster",
             title="Long-Form Input",
             labels={'traits':'population of Canada', 'value': ''})
fig.show()
