import os

from framed import load_cbmodel, save_cbmodel, Environment

from optimModels.utils.utils import fix_exchange_reactions_model
from optimModels.simulation.simul_problems import StoicSimulationProblem

basePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DD_DeCaF/Tests/examples/models/nitro"

constraints = {}

SBML_FILE = (os.path.join(basePath, 'model_nvu_v6.xml'))
model = load_cbmodel(SBML_FILE, exchange_detection_mode='R_EX_')
newModel = fix_exchange_reactions_model(model)

print(newModel.id)

bRXN = "R_e_Biomass_C4__cytop"

simulProb = StoicSimulationProblem(newModel, objective={bRXN: 1}, method="pFBA")

essential = simulProb.find_essential_drains()
print("Essential; ", essential)


for r_id, rxn in newModel.reactions.items():
    if rxn.is_exchange:
        rxn.lb = -1000 if rxn.lb is None else rxn.lb
        rxn.ub = 1000 if rxn.ub is None else rxn.ub

for r_id, rxn in newModel.reactions.items():
    if rxn.is_exchange:
        rxn.lb = 0

minimal_medium = ['R_EX_C00059__dra', 'R_EX_C00009__dra', 'R_EX_C00001__dra', 'R_EX_C14818__dra']

carbon_source = ['R_EX_C00011__dra']

ethanol = ['R_EX_C00469__dra']

oxygen = ['R_EX_C00007__dra']

nitrate = ['R_EX_C00088__dra']

#compounds = ['C00001', 'C00011', 'C00009', 'C00007', 'C00088', 'C00059', 'C00469', 'C14818']


for i in minimal_medium:
    constraints.update({i: (-1000, 1000)})

for i in carbon_source:
    constraints.update({i: (-10, 0)})

for i in ethanol:
    constraints.update({i: (-0.1, 0)})

for i in oxygen:
    constraints.update({i: (-1000, 1000)})

for i in nitrate:
    constraints.update({i: (-5, 1000)})

sol = StoicSimulationProblem(newModel, objective={bRXN: 1}, method="pFBA", constraints=constraints)

pfba = sol.simulate()

for r_id, rxn in newModel.reactions.items():
    if rxn.is_exchange:
        if pfba.get_fluxes_distribution()[r_id] != 0:
            print('Rxn: ' + str(r_id) + " Flux: " + str(pfba.get_fluxes_distribution()[r_id]))




#env = Environment.from_compounds(compounds, exchange_format="'R_EX_{}__dra'", max_uptake=5.0)

#Environment.apply(env, newModel, inplace=True)

#save_cbmodel(newModel, basePath + '/' + model.id + "_fbc2_v1.xml", flavor='fbc2')