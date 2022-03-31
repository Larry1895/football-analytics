import pandas as pd
import scipy.cluster.hierarchy as shc
from pyvis.network import Network
from scipy.cluster import hierarchy as clust
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
from sqlalchemy import text
from yellowbrick.cluster import KElbowVisualizer

from src.scrapper.base import Session

# Die overall Bewertung fliegt raus da diese über die einzelnen Attribute abgedeckt wird
# Die Attribute zwischen den Spielern werden vorher korreliert, da Sie in der Summe (Anzahl) zu stark überwiegen würden
# Die Overall-Wertung gibt keine Aussage über die Ähnlichkeit der Attribute

session = Session()

sql = text('SELECT player.player_id, player.full_name, rating, potential, value, wage, international_reputation, ' +
           'date_part(\'year\', age(date_of_birth)) as age ' +
           'from player ' +
           'left join player_transfer_data ptd on player.player_id = ptd.player_id '
           + 'Where rating > 70 '
           + 'Order by player.player_id')
result = session.execute(sql).all()

all_player = []
names = []

for row in result:
    one_player = []
    dict_row = dict(row)
    # print(str(dict_row.get('player_id')))

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

linkage = shc.linkage(data_scaled_df, method='ward')

# Dendorgram

# def llf(id):
#     return names[id]
#
#
# plt.figure(figsize=(100, 24))
# plt.title("Dendrogram with hierarchical cluster of positions")
# dend = shc.dendrogram(shc.linkage(data_scaled_df, method='ward'), leaf_label_func=llf, color_threshold=0.1)
# plt.axhline(y=0.6, color='r', linestyle='--')
# plt.show()

clusters = clust.fcluster(shc.linkage(data_scaled_df, method='ward'), 0.1, criterion='distance')
print(clusters)

# Another Dendorgram

# https://stackoverflow.com/questions/50250010/plotly-chart-is-not-displayed-in-pycharm
# pio.renderers.default = "browser"
# fig = ff.create_dendrogram(
#     data_scaled_df, color_threshold=0.1, orientation='bottom', labels=names,
#     linkagefun=lambda x: shc.linkage(data_scaled_df, 'ward', metric='euclidean')
# )
# fig.update_layout(width=1920, height=1080)
# fig.show()

#
# seed_random = 1
#
# fitted_kmeans = {}
# labels_kmeans = {}
# df_scores = []
# k_values_to_try = np.arange(5, 100)
# for n_clusters in k_values_to_try:
#     # Perform clustering.
#     kmeans = KMeans(n_clusters=n_clusters,
#                     random_state=seed_random,
#                     )
#     labels_clusters = kmeans.fit_predict(data_scaled_df)
#
#     # Insert fitted model and calculated cluster labels in dictionaries,
#     # for further reference.
#     fitted_kmeans[n_clusters] = kmeans
#     labels_kmeans[n_clusters] = labels_clusters
#
#     # Calculate various scores, and save them for further reference.
#     silhouette = silhouette_score(data_scaled_df, labels_clusters)
#     ch = calinski_harabasz_score(data_scaled_df, labels_clusters)
#     db = davies_bouldin_score(data_scaled_df, labels_clusters)
#     tmp_scores = {"n_clusters": n_clusters,
#                   "silhouette_score": silhouette,
#                   "calinski_harabasz_score": ch,
#                   "davies_bouldin_score": db,
#                   }
#     df_scores.append(tmp_scores)
#
# # Create a DataFrame of clustering scores, using `n_clusters` as index, for easier plotting.
# df_scores = pd.DataFrame(df_scores)
# df_scores.set_index("n_clusters", inplace=True)


# Within-Cluster-Sum of Squared Errors
model = KMeans()
visualizer = KElbowVisualizer(model, k=(5, 30), timings=False)
visualizer.fit(data_scaled_df)
visualizer.show()

model = KMeans()
visualizer = KElbowVisualizer(model, k=(5, 30), metric='silhouette', timings=False)
visualizer.fit(data_scaled_df)
visualizer.show()

model = KMeans()
visualizer = KElbowVisualizer(model, k=(5, 30), metric='calinski_harabasz', timings=False)
visualizer.fit(data_scaled_df)
visualizer.show()


# K means
number_of_cluster = 42
kmeans = KMeans(n_clusters=number_of_cluster)
fit = kmeans.fit(data_scaled_df)
clusters = kmeans.predict(data_scaled_df)
data_scaled_df["Cluster"] = clusters

cluster_center = fit.cluster_centers_

# Network chart with groups

net = Network(height='1080px', width='100%', directed=True)
net.repulsion()

for cluster_id in range(number_of_cluster):
    net.add_node('cluster_' + str(cluster_id),
                 'cluster_' + str(cluster_id),
                 labelHighlightBold=True,
                 group=cluster_id)

for index, player_values in data_scaled_df.iterrows():
    net.add_node(index + 1,
                 names[index],
                 labelHighlightBold=True,
                 group=player_values['Cluster'])

    net.add_edge(source=index + 1,
                 to='cluster_' + str(int(player_values['Cluster'])))

net.show_buttons(filter_=['physics'])
net.show('club_transfer_network.html')


# https://www.kaggle.com/minc33/visualizing-high-dimensional-clusters
# PCA

# pca = PCA(n_components=2)
# principalComponents = pca.fit_transform(data_scaled_df)
#
# principalDf = pd.DataFrame(data=principalComponents
#                            , columns=['principal component 1', 'principal component 2'])
#
# principalDf.tail()
# plt.figure()
# plt.figure(figsize=(24, 18))
# plt.xticks(fontsize=24)
# plt.yticks(fontsize=24)
# plt.xlabel('Principal Component - 1', fontsize=32)
# plt.ylabel('Principal Component - 2', fontsize=32)
# plt.title("Principal Component Analysis of Breast Cancer Dataset", fontsize=20)
# targets = [0, 1, 2, 3, 4, 5]
# colors = ['r', 'g', 'b', 'm', 'c', 'k']
# for target, color in zip(targets, colors):
#     indicesToKeep = data_scaled_df["Cluster"] == target
#     plt.scatter(principalDf.loc[indicesToKeep, 'principal component 1']
#                 , principalDf.loc[indicesToKeep, 'principal component 2'], c=color, s=50)
#
# plt.legend(targets, prop={'size': 15})
# plt.show()

# tsne

#
# tsne_2d = TSNE(n_components=2)
#
# principalComponents_tsne = tsne_2d.fit_transform(data_scaled_df)
#
# principal_tsne_Df = pd.DataFrame(data=principalComponents_tsne,
#                                  columns=['principal component 1', 'principal component 2'])
#
# principal_tsne_Df.tail()
# plt.figure()
# plt.figure(figsize=(24, 18))
# plt.xticks(fontsize=24)
# plt.yticks(fontsize=24)
# plt.xlabel('Principal Component - 1', fontsize=32)
# plt.ylabel('Principal Component - 2', fontsize=32)
# plt.title("Principal Component Analysis of Breast Cancer Dataset", fontsize=20)
# targets = [0, 1, 2, 3, 4, 5]
# colors = ['r', 'g', 'b', 'm', 'c', 'k']
# for target, color in zip(targets, colors):
#     indicesToKeep = data_scaled_df["Cluster"] == target
#     plt.scatter(principal_tsne_Df.loc[indicesToKeep, 'principal component 1']
#                 , principal_tsne_Df.loc[indicesToKeep, 'principal component 2'], c=color, s=50)
#
# plt.legend(targets, prop={'size': 15})
# plt.show()
