import os

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing

basePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DD_DeCaF/Tests/examples/models/sophia_models"
CSV_FILE = (os.path.join(basePath, 'fva_data_v1.csv'))

fva_data = pd.read_csv(CSV_FILE, sep = ';', index_col='Condition')
indx = fva_data.index
cols = fva_data.columns
fva_data_corr = fva_data.corr()

min_max_scaler = preprocessing.MinMaxScaler()
np_scaled = min_max_scaler.fit_transform(fva_data)
df_normalized = pd.DataFrame(np_scaled, columns = cols, index = indx)

print(df_normalized)

df_normalized.to_csv(os.path.join(basePath, 'fva_data_norm.csv'), sep=';')

#ax = sns.heatmap(df_normalized, linewidth=1, linecolor='w', cmap='Blues')
#ax.set_xticklabels(ax.get_xticklabels(), rotation=40)
#plt.show()

ax2 = sns.clustermap(df_normalized, cmap="coolwarm")
plt.show()