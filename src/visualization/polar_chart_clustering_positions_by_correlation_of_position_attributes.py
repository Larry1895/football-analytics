import numpy as np
import pandas as pd
import plotly.express as px
from sqlalchemy import text

from src.scrapper.base import Session

# Diese arrays beinhalten das Korrelationsverhältnis der einzelnen Attribute pro position
positions = []
attributes = []
values = []

session = Session()
positions_sql = text('SELECT position_id, short_name ' +
                     'from position ')
positions_result = session.execute(positions_sql).all()

# Iteriere durch alle Positionen
for row in positions_result:
    position_id = dict(row).get('position_id')
    position_name = str(dict(row).get('short_name'))

    print('Build correlation matrix from atrributes of all player for position ' + position_name)

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

    positions.append(position_name)
    attributes.append("crossing")
    values.append(np_corr_def[0][1])

    positions.append(position_name)
    attributes.append("finishing")
    values.append(np_corr_def[0][2])

    positions.append(position_name)
    attributes.append("heading_accuracy")
    values.append(np_corr_def[0][3])

    positions.append(position_name)
    attributes.append("short_passing")
    values.append(np_corr_def[0][4])

    positions.append(position_name)
    attributes.append("volleys")
    values.append(np_corr_def[0][5])

    positions.append(position_name)
    attributes.append("dribbling")
    values.append(np_corr_def[0][6])

    positions.append(position_name)
    attributes.append("curve")
    values.append(np_corr_def[0][7])

    positions.append(position_name)
    attributes.append("fk_accuracy")
    values.append(np_corr_def[0][8])

    positions.append(position_name)
    attributes.append("long_passing")
    values.append(np_corr_def[0][9])

    positions.append(position_name)
    attributes.append("ball_control")
    values.append(np_corr_def[0][10])

    positions.append(position_name)
    attributes.append("acceleration")
    values.append(np_corr_def[0][11])

    positions.append(position_name)
    attributes.append("sprint_speed")
    values.append(np_corr_def[0][12])

    positions.append(position_name)
    attributes.append("agility")
    values.append(np_corr_def[0][13])

    positions.append(position_name)
    attributes.append("reactions")
    values.append(np_corr_def[0][14])

    positions.append(position_name)
    attributes.append("balance")
    values.append(np_corr_def[0][15])

    positions.append(position_name)
    attributes.append("shot_power")
    values.append(np_corr_def[0][16])

    positions.append(position_name)
    attributes.append("jumping")
    values.append(np_corr_def[0][17])

    positions.append(position_name)
    attributes.append("stamina")
    values.append(np_corr_def[0][18])

    positions.append(position_name)
    attributes.append("strength")
    values.append(np_corr_def[0][19])

    positions.append(position_name)
    attributes.append("long_shots")
    values.append(np_corr_def[0][20])

    positions.append(position_name)
    attributes.append("aggression")
    values.append(np_corr_def[0][21])

    positions.append(position_name)
    attributes.append("interceptions")
    values.append(np_corr_def[0][22])

    positions.append(position_name)
    attributes.append("positioning")
    values.append(np_corr_def[0][23])

    positions.append(position_name)
    attributes.append("vision")
    values.append(np_corr_def[0][24])

    positions.append(position_name)
    attributes.append("penalties")
    values.append(np_corr_def[0][25])

    positions.append(position_name)
    attributes.append("composure")
    values.append(np_corr_def[0][26])

    positions.append(position_name)
    attributes.append("defensive_awareness")
    values.append(np_corr_def[0][27])

    positions.append(position_name)
    attributes.append("standing_tackle")
    values.append(np_corr_def[0][28])

    positions.append(position_name)
    attributes.append("sliding_tackle")
    values.append(np_corr_def[0][29])

    positions.append(position_name)
    attributes.append("gk_diving")
    values.append(np_corr_def[0][30])

    positions.append(position_name)
    attributes.append("gk_handling")
    values.append(np_corr_def[0][31])

    positions.append(position_name)
    attributes.append("gk_kicking")
    values.append(np_corr_def[0][32])


    positions.append(position_name)
    attributes.append("gk_positioning")
    values.append(np_corr_def[0][33])

    positions.append(position_name)
    attributes.append("gk_reflexes")
    values.append(np_corr_def[0][34])

correlated_df = pd.DataFrame({
    "attribute": attributes,
    "position": positions,
    "value": values,
})

# Polar
df = px.data.wind()

# print(correlated_df)

fig = px.line_polar(correlated_df,
                    r="value",
                    theta="attribute",
                    color="position",
                    line_close=True,
                    color_discrete_sequence=px.colors.qualitative.Plotly)
fig.show()
