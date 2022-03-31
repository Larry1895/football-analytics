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

for row in result:
    dict_row = dict(row)
    name.append(dict_row.get('full_name'))
    value.append(float(dict_row.get('value')))
    wage.append(float(dict_row.get('wage')))
    weight.append(dict_row.get('weight'))
    height.append(dict_row.get('height'))
    age.append(dict_row.get('age'))
    print(str(dict_row.get('player_id')))

session.close()

employees_df = pd.DataFrame({
    'Name': name,
    'Value': value,
    'Wage': wage,
    'Age': age,
    'Weight': weight,
    'Height': height
})

corr_df = employees_df.corr(method='pearson')

# Getting the Upper Triangle of the co-relation matrix
matrix = np.triu(corr_df)

plt.figure(figsize=(12, 8))
res = sns.heatmap(corr_df, annot=True, cmap='RdYlGn_r', mask=matrix, annot_kws={"fontsize":20}, linewidths=1, vmin=-1, vmax=1)

# X and Y axis
res.set_xticklabels(res.get_xmajorticklabels(), fontsize=26, rotation=90)
res.set_yticklabels(res.get_ymajorticklabels(), fontsize=26, rotation=0)

# Colorbar
cbar = res.collections[0].colorbar
cbar.ax.tick_params(labelsize=28)

res.figure.tight_layout()
plt.rcParams["font.family"] = "Arial"
plt.show()
