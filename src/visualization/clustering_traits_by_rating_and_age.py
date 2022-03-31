import pandas as pd
import plotly.express as px
import plotly.io as pio
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
from sqlalchemy import text
from yellowbrick.cluster import KElbowVisualizer

from src.scrapper.base import Session

trait_names = []
data = []
column_names = [
    'avg_rating',
    # 'avg_value',
    'avg_age'
]
# One club player wird ausgenommen, da es nur zwei Spieler gibt (Weltklasse)
session = Session()
traits_sql = text('SELECT t.trait_id, t.name, '
                  + 'avg(rating) as avg_rating, '
                  + 'avg(value) as avg_value, '
                  + 'avg(date_part(\'year\', AGE(date_of_birth))) as avg_age '
                  + 'from player '
                  + 'left join player_transfer_data ptd on player.player_id = ptd.player_id '
                  + 'left join fifa_player_trait fpt on player.player_id = fpt.player_id '
                  + 'left join trait t on fpt.trait_id = t.trait_id '
                  + 'Where '
                  + 't.trait_id is not null AND '
                  + 't.trait_id != 5 '
                  + 'group by t.trait_id, t.name '
                  + 'order by t.trait_id')

traits_result = session.execute(traits_sql).all()

# Iteriere durch alle Positionen
for row in traits_result:
    trait_data = []
    trait_id = dict(row).get('trait_id')
    trait_names.append(str(dict(row).get('name')).replace("(AI)", ""))

    trait_data.append(dict(row).get('avg_rating'))
    # trait_data.append(dict(row).get('avg_value'))
    trait_data.append(dict(row).get('avg_age'))
    data.append(trait_data)

    data_df = pd.DataFrame(data, columns=column_names)
    transpose_normalized_df = normalize(data_df.transpose())
    data_scaled_df = pd.DataFrame(transpose_normalized_df.transpose(), columns=column_names)

# elbow
model = KMeans()
visualizer = KElbowVisualizer(model, k=(1, 12), timings=False).fit(data_df)
# visualizer.ax.xaxis.label.set_size(22)
# visualizer.ax.yaxis.label.set_size(22)
visualizer.show()

# k-means custer
kmeans = KMeans(n_clusters=5, init='k-means++', random_state=0).fit(data_df)
data_df["cluster"] = kmeans.labels_
data_df.cluster = data_df.cluster.astype(str)

data_df["names"] = trait_names

df = px.data.iris()
pio.renderers.default = "browser"
fig = px.scatter(data_df,
                 x=column_names[1],  # value
                 y=column_names[0],  # rating
                 color='cluster',
                 text="names")
fig.update_traces(textposition='top center', marker_size=20)
fig.update_layout(
    height=1080,
    width=1920,
    title_text='Trait clustering based on average value and average rating',
    font=dict(
        size=19,
    )
)
fig.show()
