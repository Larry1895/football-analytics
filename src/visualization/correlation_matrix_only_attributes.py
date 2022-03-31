import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sqlalchemy import text

from src.scrapper.base import Session

session = Session()

sql = text('SELECT player.player_id, player.full_name, value, wage, player.weight, player.height, date_part(\'year\','
           'age(date_of_birth)) as age ' +
           'from player ' +
           'left join player_transfer_data ptd on player.player_id = ptd.player_id'
           # + ' Where player.player_id < 100'
           )
result = session.execute(sql).all()

name = []
value = []
wage = []
weight = []
height = []
age = []

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
    value.append(float(dict_row.get('value')))
    wage.append(float(dict_row.get('wage')))
    weight.append(dict_row.get('weight'))
    height.append(dict_row.get('height'))
    age.append(dict_row.get('age'))

    sql_attributes = text('select a.name, attribute_value from fifa_player_attribute ' +
                          'left join attribute a on a.attribute_id = fifa_player_attribute.attribute_id ' +
                          'WHERE player_id = ' + str(dict_row.get('player_id')))
    result_attributes = session.execute(sql_attributes).all()
    dict_result_attributes = dict(result_attributes)

    print(str(dict_row.get('player_id')))

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

employees_df = pd.DataFrame({
    'Name': name,
    # 'Value': value,
    # 'Wage': wage,
    # 'Age': age,
    # 'Weight': weight,
    # 'Height': height,
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

corr_df = employees_df.corr(method='pearson')

# Getting the Upper Triangle of the co-relation matrix
matrix = np.triu(corr_df)

plt.figure(figsize=(32, 24))
res = sns.heatmap(corr_df, annot=True, cmap='RdYlGn_r', mask=matrix, annot_kws={"fontsize":14}, linewidths=1)

# X and Y axis
res.set_xticklabels(res.get_xmajorticklabels(), fontsize=26, rotation=90)
res.set_yticklabels(res.get_ymajorticklabels(), fontsize=26, rotation=0)

# Colorbar
cbar = res.collections[0].colorbar
cbar.ax.tick_params(labelsize=28)

res.figure.tight_layout()
plt.rcParams["font.family"] = "Arial"
plt.show()
