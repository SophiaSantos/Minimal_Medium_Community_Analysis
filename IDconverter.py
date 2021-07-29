import os

import pandas as pd


basePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DD_DeCaF/Tests/examples/models/nitro"

list_models = []

for file in os.listdir(basePath):
    if file.endswith('.csv'):
        id_df = pd.read_csv(os.path.join(basePath, file), sep = ';')
    if file.endswith("v6.xml"):
        SBML_FILE = (os.path.join(basePath, file))
        list_models.append(SBML_FILE)

lst = id_df.values.tolist()
dct = dict((x,y) for x, y in lst)

for l in list_models:
    new = open(l + "_smetana.xml", 'w')
    with open(l, 'r') as m:
        data = m.read()
        m.close()
    for key, value in dct.items():
        data = data.replace(value, key)
    new.write(data)
    new.close()


