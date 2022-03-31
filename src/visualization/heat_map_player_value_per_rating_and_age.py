import plotly.graph_objects as go
import plotly.io as pio
from _plotly_utils.colors.carto import Temps
from sqlalchemy import text

from src.scrapper.base import Session

# https://stackoverflow.com/questions/50250010/plotly-chart-is-not-displayed-in-pycharm
pio.renderers.default = "browser"

session = Session()

sql_min_max = text(
    'SELECT min(rating) as min_rating, '
    + 'max(rating) as max_rating, '
    + 'min(date_part(\'year\', AGE(date_of_birth))) as min_age, '
    + 'max(date_part(\'year\', AGE(date_of_birth))) as max_age '
    + 'FROM player_transfer_data ptd '
    + 'left join player p on p.player_id = ptd.player_id '
      'WHERE value != 0 ')
result_min_max = session.execute(sql_min_max).one()

min_rating = int(dict(result_min_max).get('min_rating'))
max_rating = int(dict(result_min_max).get('max_rating'))
min_age = int(dict(result_min_max).get('min_age'))
max_age = int(dict(result_min_max).get('max_age'))

x = []
y = []

for r in range(min_rating, max_rating):
    x.append(str(r))

for a in range(min_age, max_age):
    y.append(str(a))

z = [[None for col in range(max_rating + 1 - min_rating)] for row in range(max_age + 1 - min_age)]

sql = text(
    'SELECT rating, date_part(\'year\', AGE(date_of_birth)) as age, AVG(ptd.value) as avg_value, avg(ptd.wage) as avg_wage '
    + 'FROM player_transfer_data ptd '
    + 'left join player p on p.player_id = ptd.player_id '
    + 'WHERE value != 0 '
    + 'GROUP BY rating, date_part(\'year\', AGE(date_of_birth)) '
    + 'ORDER BY rating asc')
result = session.execute(sql).all()
session.close()

# print(z)

for row in result:
    row_rating = int(dict(row).get('rating'))
    row_age = int(dict(row).get('age'))
    row_avg_value = int(dict(row).get('avg_value'))
    # print(str(row_age) + ',' + str(row_rating) + '->' + 'z[' + str(row_age-min_age) + '][' + str(row_rating-min_rating) + ']')
    z[row_age - min_age][row_rating - min_rating] = row_avg_value

fig = go.Figure(data=go.Heatmap(
    z=z,
    x=x,
    y=y,
    hoverongaps=False,
    # zsmooth='best',
    # colorscale=Temps,
    colorscale=[
        [0, 'rgb(0, 147, 146)'],  # 0
        [1. / 1000, 'rgb(57, 177, 133)'],  # 10.000
        [1. / 200, 'rgb(156, 203, 134)'],  # 50.000
        [1. / 100, 'rgb(233, 226, 156)'],  # 100.000
        [1. / 20, 'rgb(238, 180, 121)'],  # 500.000
        [1. / 10, 'rgb(232, 132, 113)'],  # 1.000.000
        [1., 'rgb(207, 89, 126)'],  # 10.000.000
    ],
    showscale=False,
))

colorbar_trace = go.Scatter(
    x=[None],
    y=[None],
    mode='markers',
    marker=dict(
        colorscale=Temps,
        showscale=True,
        cmin=1,
        cmax=9,
        colorbar=dict(title=dict(text="<b>Durchschn. Spielerwert <br>in Euro (€)<b><br>&nbsp;<br>&nbsp;", side='top'),
                      thickness=40,
                      tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9],
                      ticktext=['10K €', '50K €', '100K €', '500K €', '1M €', '5M €', '10M €', '50M €', '> 100M €'],
                      outlinewidth=0,
                      # orientation='h'
                      )
    ),
    hoverinfo='none'
)
fig.add_trace(colorbar_trace)

fig.update_layout(title='<b>Durchschnittlicher Spielerwert in Euro (€) pro Gesamtbewertung und dem Alter<b>')

# Only for the images within the Thesis
fig.update_layout(font=dict(size=28, family="Arial"))
fig.update_xaxes(title_standoff=40, tickvals=[47, 50, 55, 60, 65, 70, 75, 80, 85, 90, 93], title="<b>Gesamtbewertung<b>",)
fig.update_yaxes(title_standoff=40, tickvals=[17, 20, 25, 30, 35, 40, 44], title="<b>Alter<b>",)



fig.show()
