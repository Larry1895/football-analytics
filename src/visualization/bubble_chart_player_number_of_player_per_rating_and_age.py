import plotly.graph_objects as go
import plotly.io as pio
from _plotly_utils.colors.carto import Temps
from sqlalchemy import text

from src.scrapper.base import Session

# https://stackoverflow.com/questions/50250010/plotly-chart-is-not-displayed-in-pycharm
pio.renderers.default = "browser"

session = Session()
sql = text(
    'SELECT rating, date_part(\'year\', AGE(date_of_birth)) as age, Count(ptd.player_id) as number_of_player '
    + 'FROM player_transfer_data ptd '
    + 'left join player p on p.player_id = ptd.player_id '
    + 'WHERE value != 0 '
    + 'GROUP BY rating, date_part(\'year\', AGE(date_of_birth)) '
    + 'ORDER BY rating asc')
result = session.execute(sql).all()

session.close()

x_values = []
y_values = []
size_values = []
hover_text = []

for row in result:
    x_values.append(int(dict(row).get('rating')))
    y_values.append(int(dict(row).get('age')))
    size_values.append(int(dict(row).get('number_of_player')))
    hover_text.append(('Rating: {rating}<br>' +
                       'Age: {age}<br>' +
                       '<b>Number of player: {number_of_player}<b><br>')
                      .format(rating=dict(row).get('rating'),
                              age=dict(row).get('age'),
                              number_of_player=dict(row).get('number_of_player')
                      ))

fig = go.Figure(
    data=[go.Scatter(
        text=hover_text,
        x=x_values,
        y=y_values,
        mode='markers',
        marker=dict(
            opacity=0.7,
            color=size_values,
            colorscale=Temps,
            size=size_values,
            showscale=True,
            sizemode='area',
            sizeref=8. * max(size_values) / (200. ** 2),
            sizemin=1,
            colorbar=dict(title=dict(text="<b>Spieleranzahl<b> <br>&nbsp;", side='top'))
        ),
    )])

fig.update_xaxes(title="<b>Gesamtbewertung<b>",
                 range=[min(x_values) - 0.9, max(x_values) + 0.9],
                 dtick=1)
fig.update_yaxes(title="<b>Alter<b>",
                 range=[min(y_values) - 0.9, max(y_values) + 0.9],
                 dtick=1)

fig.update_layout(title='<b>Anzahl der Spieler im Verhältnis zur Gesamtbewertung und dem Alter<b>')

# Only for the images within the Thesis
fig.update_layout(font=dict(size=28, family="Arial"))
fig.update_xaxes(title_standoff=40, tickvals=[47, 50, 55, 60, 65, 70, 75, 80, 85, 90, 93])
fig.update_yaxes(title_standoff=40, tickvals=[17, 20, 25, 30, 35, 40, 44])

fig.show()
