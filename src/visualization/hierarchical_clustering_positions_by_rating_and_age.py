import pandas as pd
import plotly.express as px
import plotly.io as pio
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sqlalchemy import text
from yellowbrick.cluster import KElbowVisualizer

from src.scrapper.base import Session

position_names = []
data = []
column_names = [
    'avg_rating',
    # 'avg_value',
    'avg_age'
]

session = Session()
positions_sql = text('SELECT p.position_id, p.short_name, '
                     + 'avg(rating) as avg_rating, '
                     + 'avg(value) as avg_value, '
                     + 'avg(date_part(\'year\', AGE(date_of_birth))) as avg_age '
                     + 'from player '
                     + 'left join player_transfer_data ptd on player.player_id = ptd.player_id '
                     + 'left join player_position pp on player.player_id = pp.player_id '
                     + 'left join position p on pp.position_id = p.position_id '
                     + 'where pp.is_main_position = true '
                     + 'group by p.position_id, p.full_name '
                     + 'order by p.full_name')

positions_result = session.execute(positions_sql).all()

# Iteriere durch alle Positionen
for row in positions_result:
    position_data = []
    position_id = dict(row).get('position_id')
    position_names.append(str(dict(row).get('short_name')))

    position_data.append(dict(row).get('avg_rating'))
    # position_data.append(dict(row).get('avg_value'))
    position_data.append(dict(row).get('avg_age'))
    data.append(position_data)

data_df = pd.DataFrame(data, columns=column_names)
sc_X = StandardScaler()
normalized_df = sc_X.fit_transform(data_df)
data_scaled_df = pd.DataFrame(normalized_df, columns=column_names)

data_raw = data_df
data_df = data_scaled_df

# elbow
model = KMeans()
visualizer = KElbowVisualizer(model, k=(1, 12), timings=False).fit(data_df)
visualizer.show()

# k-means custer
kmeans = KMeans(n_clusters=5, init='k-means++', random_state=0).fit(data_df)
data_df["cluster"] = kmeans.labels_
data_df.cluster = data_df.cluster.astype(str)
data_df["names"] = position_names

# Für das Chart werden die Daten im nicht Normalisiertem Format angezeigt.
# Vor dem Clustering wurden diese allerdings normalisiert.
data_raw["cluster"] = kmeans.labels_
data_raw.cluster = data_df.cluster.astype(str)
data_raw["names"] = position_names

df = px.data.iris()
pio.renderers.default = "browser"
fig = px.scatter(data_raw,
                 x=column_names[1],  # age
                 y=column_names[0],  # rating
                 color='cluster',
                 text="names")
fig.update_traces(textposition='middle right', marker_size=20)
fig.update_layout(
    height=720,
    width=1080,
    title_text='k=5',
    font=dict(
        size=30,
    )
)
fig.update_yaxes(
    title="Ø Gesamtbewertung<br>", showgrid=True, showline=True
)

fig.update_xaxes(
    title="<br>Ø Alter", showgrid=True
)
fig.update(layout_showlegend=False)
fig.show()
