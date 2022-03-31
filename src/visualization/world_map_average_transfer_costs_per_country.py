import plotly.graph_objects as go
import plotly.io as pio
from sqlalchemy import text

from src.scrapper.base import Session

# https://stackoverflow.com/questions/50250010/plotly-chart-is-not-displayed-in-pycharm
pio.renderers.default = "browser"

# TODO
session = Session()
sql = text('SELECT c.nationality_id, n.full_name, n.abbreviation_2, '
           + 'AVG(ptd.wage) as avg_wage, '
           + 'AVG(ptd.rating) as avg_rating, '
           + 'AVG(ptd.value) as avg_value, '
           + 'COUNT(ptd.player_id) '
           + 'FROM player_club_transfer '
           + 'LEFT JOIN ( '
           + 'SELECT player_id, MAX(changed_at) as last_transfer_date '
           + 'FROM player_club_transfer '
           + 'GROUP BY player_id '
           + ') as last_transfer on last_transfer.player_id = player_club_transfer.player_id '
           + 'LEFT JOIN club c on player_club_transfer.to_club_id = c.club_id '
           + 'LEFT JOIN nation n on c.nationality_id = n.nation_id '
           + 'LEFT JOIN player_transfer_data ptd on player_club_transfer.player_id = ptd.player_id '
           + 'WHERE last_transfer.last_transfer_date = player_club_transfer.changed_at '
           + 'GROUP BY c.nationality_id, n.full_name, n.abbreviation_2 '
           + 'ORDER BY AVG(ptd.wage) ')
result = session.execute(sql).all()
session.close()

iso_codes = []
country_names = []
avg_wage = []

for row in result:
    iso_codes.append(dict(row).get('abbreviation_2'))
    country_names.append(dict(row).get('full_name')),
    avg_wage.append(float(dict(row).get('avg_wage'))),

fig = go.Figure(data=go.Choropleth(
    locations=iso_codes,
    z=avg_wage,
    text=country_names,
    colorscale='Viridis',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title='Average wage<br>in Euro (€)',
))

fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='natural earth'
    ),
    title={
        'text': '<b>Average player wage by country</b>',
        'y': 0.96,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
    },
    title_font_color='#525252',
    title_font_size=26,
    font=dict(
        family='Heebo',
        size=18,
        color='#525252'
    ),
)

fig.show()
