import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as shc
from sklearn.cluster import KMeans
from sqlalchemy import text
from yellowbrick.cluster import KElbowVisualizer

from src.scrapper.base import Session

# Diese arrays beinhalten das Korrelationsverhältnis der einzelnen Attribute pro position
position_names = []
correlation_value_crossing = []
correlation_value_finishing = []
correlation_value_heading_accuracy = []
correlation_value_short_passing = []
correlation_value_volleys = []
correlation_value_dribbling = []
correlation_value_curve = []
correlation_value_fk_accuracy = []
correlation_value_long_passing = []
correlation_value_ball_control = []
correlation_value_acceleration = []
correlation_value_sprint_speed = []
correlation_value_agility = []
correlation_value_reactions = []
correlation_value_balance = []
correlation_value_shot_power = []
correlation_value_jumping = []
correlation_value_stamina = []
correlation_value_strength = []
correlation_value_long_shots = []
correlation_value_aggression = []
correlation_value_interceptions = []
correlation_value_positioning = []
correlation_value_vision = []
correlation_value_penalties = []
correlation_value_composure = []
correlation_value_defensive_awareness = []
correlation_value_standing_tackle = []
correlation_value_sliding_tackle = []
correlation_value_gk_diving = []
correlation_value_gk_handling = []
correlation_value_gk_kicking = []
correlation_value_gk_positioning = []
correlation_value_gk_reflexes = []

session = Session()
positions_sql = text('SELECT position_id, short_name ' +
                     'from position')
positions_result = session.execute(positions_sql).all()

# Iteriere durch alle Positionen
for row in positions_result:
    position_id = dict(row).get('position_id')

    print('Build correlation matrix from atrributes of all player for position ' + str(dict(row).get('short_name')))
    position_names.append(str(dict(row).get('short_name')))

    sql = text('SELECT player.player_id, player.full_name, rating ' +
               'from player ' +
               'left join player_transfer_data ptd on player.player_id = ptd.player_id '
               'left join player_position pp on player.player_id = pp.player_id '
               'where position_id = ' + str(position_id))
    result = session.execute(sql).all()

    # Hier werden für jeden Spieler die Attributwerte reingeschrieben
    name = []
    overall = []
    crossing = []
    finishing = []
    heading_accuracy = []
    short_passing = []
    volleys = []
    dribbling = []
    curve = []
    fk_accuracy = []
    long_passing = []
    ball_control = []
    acceleration = []
    sprint_speed = []
    agility = []
    reactions = []
    balance = []
    shot_power = []
    jumping = []
    stamina = []
    strength = []
    long_shots = []
    aggression = []
    interceptions = []
    positioning = []
    vision = []
    penalties = []
    composure = []
    defensive_awareness = []
    standing_tackle = []
    sliding_tackle = []
    gk_diving = []
    gk_handling = []
    gk_kicking = []
    gk_positioning = []
    gk_reflexes = []

    for row in result:
        dict_row = dict(row)
        name.append(dict_row.get('full_name'))
        overall.append(dict_row.get('rating'))

        sql_attributes = text('select a.name, attribute_value from fifa_player_attribute ' +
                              'left join attribute a on a.attribute_id = fifa_player_attribute.attribute_id ' +
                              'WHERE player_id = ' + str(dict_row.get('player_id')))
        result_attributes = session.execute(sql_attributes).all()
        dict_result_attributes = dict(result_attributes)

        crossing.append(dict_result_attributes.get('crossing'))
        finishing.append(dict_result_attributes.get('finishing'))
        heading_accuracy.append(dict_result_attributes.get('heading_accuracy'))
        short_passing.append(dict_result_attributes.get('short_passing'))
        volleys.append(dict_result_attributes.get('volleys'))
        dribbling.append(dict_result_attributes.get('dribbling'))
        curve.append(dict_result_attributes.get('curve'))
        fk_accuracy.append(dict_result_attributes.get('fk_accuracy'))
        long_passing.append(dict_result_attributes.get('long_passing'))
        ball_control.append(dict_result_attributes.get('ball_control'))
        acceleration.append(dict_result_attributes.get('acceleration'))
        sprint_speed.append(dict_result_attributes.get('sprint_speed'))
        agility.append(dict_result_attributes.get('agility'))
        reactions.append(dict_result_attributes.get('reactions'))
        balance.append(dict_result_attributes.get('balance'))
        shot_power.append(dict_result_attributes.get('shot_power'))
        jumping.append(dict_result_attributes.get('jumping'))
        stamina.append(dict_result_attributes.get('stamina'))
        strength.append(dict_result_attributes.get('strength'))
        long_shots.append(dict_result_attributes.get('long_shots'))
        aggression.append(dict_result_attributes.get('aggression'))
        interceptions.append(dict_result_attributes.get('interceptions'))
        positioning.append(dict_result_attributes.get('positioning'))
        vision.append(dict_result_attributes.get('vision'))
        penalties.append(dict_result_attributes.get('penalties'))
        composure.append(dict_result_attributes.get('composure'))
        defensive_awareness.append(dict_result_attributes.get('defensive_awareness'))
        standing_tackle.append(dict_result_attributes.get('standing_tackle'))
        sliding_tackle.append(dict_result_attributes.get('sliding_tackle'))
        gk_diving.append(dict_result_attributes.get('gk_diving'))
        gk_handling.append(dict_result_attributes.get('gk_handling'))
        gk_kicking.append(dict_result_attributes.get('gk_kicking'))
        gk_positioning.append(dict_result_attributes.get('gk_positioning'))
        gk_reflexes.append(dict_result_attributes.get('gk_reflexes'))

    session.close()

    attributes_df = pd.DataFrame({
        'Name': name,
        "overall": overall,
        'crossing': crossing,
        'finishing': finishing,
        'heading_accuracy': heading_accuracy,
        'short_passing': short_passing,
        'volleys': volleys,
        'dribbling': dribbling,
        'curve': curve,
        'fk_accuracy': fk_accuracy,
        'long_passing': long_passing,
        'ball_control': ball_control,
        'acceleration': acceleration,
        'sprint_speed': sprint_speed,
        'agility': agility,
        'reactions': reactions,
        'balance': balance,
        'shot_power': shot_power,
        'jumping': jumping,
        'stamina': stamina,
        'strength': strength,
        'long_shots': long_shots,
        'aggression': aggression,
        'interceptions': interceptions,
        'positioning': positioning,
        'vision': vision,
        'penalties': penalties,
        'composure': composure,
        'defensive_awareness': defensive_awareness,
        'standing_tackle': standing_tackle,
        'sliding_tackle': sliding_tackle,
        'gk_diving': gk_diving,
        'gk_handling': gk_handling,
        'gk_kicking': gk_kicking,
        'gk_positioning': gk_positioning,
        'gk_reflexes': gk_reflexes
    })

    corr_df = attributes_df.corr(method='pearson')
    # Hier drin steckt das Verhältnis von den einzelnen Attributen zuz Gesamtbewertung für eine Position
    np_corr_def = (np.array(corr_df))
    # print(np_corr_def[0])

    correlation_value_crossing.append(np_corr_def[0][1])
    correlation_value_finishing.append(np_corr_def[0][2])
    correlation_value_heading_accuracy.append(np_corr_def[0][3])
    correlation_value_short_passing.append(np_corr_def[0][4])
    correlation_value_volleys.append(np_corr_def[0][5])
    correlation_value_dribbling.append(np_corr_def[0][6])
    correlation_value_curve.append(np_corr_def[0][7])
    correlation_value_fk_accuracy.append(np_corr_def[0][8])
    correlation_value_long_passing.append(np_corr_def[0][9])
    correlation_value_ball_control.append(np_corr_def[0][10])
    correlation_value_acceleration.append(np_corr_def[0][11])
    correlation_value_sprint_speed.append(np_corr_def[0][12])
    correlation_value_agility.append(np_corr_def[0][13])
    correlation_value_reactions.append(np_corr_def[0][14])
    correlation_value_balance.append(np_corr_def[0][15])
    correlation_value_shot_power.append(np_corr_def[0][16])
    correlation_value_jumping.append(np_corr_def[0][17])
    correlation_value_stamina.append(np_corr_def[0][18])
    correlation_value_strength.append(np_corr_def[0][19])
    correlation_value_long_shots.append(np_corr_def[0][20])
    correlation_value_aggression.append(np_corr_def[0][21])
    correlation_value_interceptions.append(np_corr_def[0][22])
    correlation_value_positioning.append(np_corr_def[0][23])
    correlation_value_vision.append(np_corr_def[0][24])
    correlation_value_penalties.append(np_corr_def[0][25])
    correlation_value_composure.append(np_corr_def[0][26])
    correlation_value_defensive_awareness.append(np_corr_def[0][27])
    correlation_value_standing_tackle.append(np_corr_def[0][28])
    correlation_value_sliding_tackle.append(np_corr_def[0][29])
    correlation_value_gk_diving.append(np_corr_def[0][30])
    correlation_value_gk_handling.append(np_corr_def[0][31])
    correlation_value_gk_kicking.append(np_corr_def[0][32])
    correlation_value_gk_positioning.append(np_corr_def[0][33])
    correlation_value_gk_reflexes.append(np_corr_def[0][34])

correlated_df = pd.DataFrame({
    "correlation_value_crossing": correlation_value_crossing,
    "correlation_value_finishing": correlation_value_finishing,
    "correlation_value_heading_accuracy": correlation_value_heading_accuracy,
    "correlation_value_short_passing": correlation_value_short_passing,
    "correlation_value_volleys": correlation_value_volleys,
    "correlation_value_dribbling": correlation_value_dribbling,
    "correlation_value_curve": correlation_value_curve,
    "correlation_value_fk_accuracy": correlation_value_fk_accuracy,
    "correlation_value_long_passing": correlation_value_long_passing,
    "correlation_value_ball_control": correlation_value_ball_control,
    "correlation_value_acceleration": correlation_value_acceleration,
    "correlation_value_sprint_speed": correlation_value_sprint_speed,
    "correlation_value_agility": correlation_value_agility,
    "correlation_value_reactions": correlation_value_reactions,
    "correlation_value_balance": correlation_value_balance,
    "correlation_value_shot_power": correlation_value_shot_power,
    "correlation_value_jumping": correlation_value_jumping,
    "correlation_value_stamina": correlation_value_stamina,
    "correlation_value_strength": correlation_value_strength,
    "correlation_value_long_shots": correlation_value_long_shots,
    "correlation_value_aggression": correlation_value_aggression,
    "correlation_value_interceptions": correlation_value_interceptions,
    "correlation_value_positioning": correlation_value_positioning,
    "correlation_value_vision": correlation_value_vision,
    "correlation_value_penalties": correlation_value_penalties,
    "correlation_value_composure": correlation_value_composure,
    "correlation_value_defensive_awareness": correlation_value_defensive_awareness,
    "correlation_value_standing_tackle": correlation_value_standing_tackle,
    "correlation_value_sliding_tackle": correlation_value_sliding_tackle,
    "correlation_value_gk_diving": correlation_value_gk_diving,
    "correlation_value_gk_handling": correlation_value_gk_handling,
    "correlation_value_gk_kicking": correlation_value_gk_kicking,
    "correlation_value_gk_positioning": correlation_value_gk_positioning,
    "correlation_value_gk_reflexes": correlation_value_gk_reflexes
})

# Within-Cluster-Sum of Squared Errors
model = KMeans()
visualizer = KElbowVisualizer(model, k=(2, 10), timings=False)
visualizer.fit(correlated_df)
visualizer.show()

model = KMeans()
visualizer = KElbowVisualizer(model, k=(2, 10), metric='silhouette', timings=False)
visualizer.fit(correlated_df)
visualizer.show()

model = KMeans()
visualizer = KElbowVisualizer(model, k=(2, 10), metric='calinski_harabasz', timings=False)
visualizer.fit(correlated_df)
visualizer.show()


# Dendrogram with automated number of clusters by elbow method
# Clusters: GK, Offensive, Defensive

def llf(id):
    return position_names[id]


plt.figure(figsize=(10, 7))
plt.title("Dendrogram with hierarchical cluster of positions")
dend = shc.dendrogram(shc.linkage(correlated_df, method='ward'),
                      leaf_label_func=llf)
plt.axhline(y=1.3, color='r', linestyle='--')
plt.show()


# Dendrogram with custom number of clusters by eye
# Clusters: GK, Offensive Außenspieler, Defensive Außenspieler,
# Zentrales Mittelfeld, Zentrale Stürmer, Zentrale Defensive

plt.figure(figsize=(10, 7))
plt.title("Dendrogram with hierarchical cluster of positions")
dend = shc.dendrogram(shc.linkage(correlated_df, method='ward'),
                      leaf_label_func=llf,
                      color_threshold=0.6)
plt.axhline(y=0.6, color='r', linestyle='--')
plt.show()

# K means
# number_of_cluster = 42
# kmeans = KMeans(n_clusters=number_of_cluster)
# fit = kmeans.fit(correlated_df)
# clusters = kmeans.predict(correlated_df)
# correlated_df["Cluster"] = clusters
#
# cluster_center = fit.cluster_centers_
