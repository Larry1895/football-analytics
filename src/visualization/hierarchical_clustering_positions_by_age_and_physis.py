import pandas as pd
import plotly.express as px
import plotly.io as pio
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sqlalchemy import text
from yellowbrick.cluster import KElbowVisualizer

from src.scrapper.base import Session

position_names = []
data = []
physis_data = []
column_names = [
    'avg_age',
    'principal component'
]

session = Session()
positions_sql = text('SELECT p.position_id, p.short_name, '
                     + 'avg(date_part(\'year\', AGE(date_of_birth))) as avg_age, '
                     + 'avg(height) as avg_height, '
                     + 'avg(weight) as avg_weight '
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
    physis_data_row = []
    position_id = dict(row).get('position_id')
    position_names.append(str(dict(row).get('short_name')))

    position_data.append(dict(row).get('avg_age'))
    physis_data_row.append(dict(row).get('avg_height'))
    physis_data_row.append(dict(row).get('avg_weight'))

    data.append(position_data)
    physis_data.append(physis_data_row)

data_physis_df = pd.DataFrame(physis_data, columns=['height', 'weight'])
pca = PCA(n_components=1)
principalComponents = pca.fit_transform(data_physis_df)
principalDf = pd.DataFrame(data=principalComponents, columns=['principal component'])

data_df = pd.DataFrame(data, columns=['avg_age'])
data_df = data_df.merge(principalDf, how='left', left_index=True, right_index=True)

sc_X = StandardScaler()
normalized_df = sc_X.fit_transform(data_df)
data_scaled_df = pd.DataFrame(normalized_df, columns=column_names)

data_raw = data_df
data_df = data_scaled_df

# elbow
model = KMeans()
visualizer = KElbowVisualizer(model, k=(1, 12), timings=False).fit(data_df)
# visualizer.ax.xaxis.label.set_size(22)
# visualizer.ax.yaxis.label.set_size(22)
visualizer.show()

# k-means custer
kmeans = KMeans(n_clusters=4, init='k-means++', random_state=0).fit(data_df)
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
                 x=column_names[1],  # physis
                 y=column_names[0],  # age
                 color='cluster',
                 text="names")
fig.update_traces(textposition='middle right', marker_size=20)
fig.update_layout(
    height=720,
    width=1080,
    title_text='k=4',
    font=dict(
        size=30,
    )
)
fig.update_yaxes(
    title="Ø Alter<br>", showgrid=True, showline=True
)

fig.update_xaxes(
    title="<br>Ø Physiswert (PCA)", showgrid=True
)
fig.update(layout_showlegend=False)
fig.show()
