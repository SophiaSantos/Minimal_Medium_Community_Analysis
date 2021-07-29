import os

from cobra import Model, Reaction, Metabolite
from cobra.io import read_sbml_model

basePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DD_DeCaF/Tests/examples/models/nitro"

SBML_FILE = (os.path.join(basePath, '1607_2.xml'))
model = read_sbml_model(SBML_FILE)

#constraints = ['EX_C00001__dra', 'EX_C00009__dra', 'EX_C00059__dra', 'EX_C00088__dra', 'EX_C14818__dra', 'EX_C00007__dra']

etoh = ['EX_C00469__dra']

KO = ['EX_C00014__dra']

#for i in constraints:
#    model.reactions.get_by_id(i).lower_bound = -10
#    model.reactions.get_by_id(i).upper_bound = 0

#for i in etoh:
#    model.reactions.get_by_id(i).lower_bound = -0.1
#    model.reactions.get_by_id(i).upper_bound = 0

#for i in KO:
#    model.reactions.get_by_id(i).lower_bound = 0
#    model.reactions.get_by_id(i).upper_bound = 0

minimal = ['EX_C00864__dra', 'EX_C00009__dra', 'EX_C00504__dra', 'EX_C00378__dra', 'EX_C00255__dra', 'EX_C00059__dra', 'EX_C14818__dra', 'EX_C00014__dra', 'EX_C00568__dra', 'EX_C00253__dra', 'EX_C00250__dra', 'EX_C00137__dra', 'EX_C00120__dra', 'EX_C06232__dra', 'EX_C05437__dra', 'EX_C08362__dra', 'EX_C00712__dra']
glucose = ['EX_C00267__dra']
amino = ['EX_C00135__dra', 'EX_C00078__dra', 'EX_C00073__dra']

ATPM = ['R00086__cyto']

for i in model.reactions:
    if '__dra' in i.id:
        i.bounds = (0, 1000)

for i in minimal:
    model.reactions.get_by_id(i).lower_bound = -1000
    model.reactions.get_by_id(i).upper_bound = 1000

for i in glucose:
    model.reactions.get_by_id(i).lower_bound = -1.5
    model.reactions.get_by_id(i).upper_bound = 1000

for i in amino:
    model.reactions.get_by_id(i).lower_bound = -0.2
    model.reactions.get_by_id(i).upper_bound = 1000

for i in ATPM:
    model.reactions.get_by_id(i).lower_bound = 0.45
    model.reactions.get_by_id(i).upper_bound = 0.45


solution = model.optimize()

print(model.summary())

print(model.metabolites.C00007__cyto.summary())