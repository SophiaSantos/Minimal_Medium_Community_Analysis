import os
import itertools

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from framed import load_cbmodel
from optimModels.utils.utils import fix_exchange_reactions_model
from optimModels.simulation.simul_problems import StoicSimulationProblem

basePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DD_DeCaF/Tests/examples/models/sophia_models"

met_list = []
rxn_list = []
met_dict = {}
flux_dict = {}
met_list_name=[]
exchange_dict = {}
constraints = {}
exchange_list = []
header = ['Rxn', 'Flux', 'Condition']
Rxn = []
Rxn_lists = []
Flux_lists = []
Flux = []
dict_data = []
len_list=[]
conditions = []

KO = ['R_EX_C06251__dra', 'R_EX_C06026__dra', 'R_EX_C06024__dra', 'R_EX_C06025__dra', 'R_EX_C00288__dra']

SBML_FILE = (os.path.join(basePath, 'model_saz_v13a.xml'))
model = load_cbmodel(SBML_FILE, exchange_detection_mode='R_EX_')
newModel = fix_exchange_reactions_model(model)


print(newModel.id)


for r_id, rxn in newModel.reactions.items():
    if rxn.is_exchange:
        rxn.lb = -1000 if rxn.lb is None else rxn.lb
        rxn.ub = 1000 if rxn.ub is None else rxn.ub

for r_id, rxn in newModel.reactions.items():
    if r_id.startswith('R_ATPM'):
        rxn.lb = 8.39
        rxn.ub = 8.39
    if rxn.is_exchange:
        rxn.lb = 0
#        rxn.lb = -100
        exchange_list.append(r_id)
    if r_id.startswith('R_sink_'):
        rxn.lb = 0
        exchange_list.append(r_id)


bRXN = "R_e_Biomass__cytop"

co2 = 'R_EX_C00011__dra'

carbon_source = ['R_EX_C00011__dra']

essential = ['R_EX_C14818__dra']

minimal_medium = ['R_EX_C00014__dra', 'R_EX_C00087__dra', 'R_EX_C00001__dra', 'R_EX_C00009__dra']

cell = 'R_EX_C00760__dra'

oxygen = ['R_EX_C00007__dra']

starvation = ['R_EX_C00014__dra']

newModel.biomass_reaction = 'R_e_Biomass__cytop'


for i in minimal_medium:
    constraints.update({i: (-1000, 1000)})


for i in essential:
    constraints.update({i: (-1000, 1000)})

for i in oxygen:
    constraints.update({i: (-0.01, 1000)})

for i in starvation:
    constraints.update({i: (-0.257, 0)})

for i in carbon_source:
    constraints.update({i: (-12, -12)})

#for i in KO:
#    constraints.update({i: (0, 0)})

print(constraints)

#carbon_source_production = {'R_EX_C00993__dra': (0.0, 0.1518), 'R_EX_C00288__dra': (0.0, 14.85), 'R_EX_C00033__dra':(0.0, 0.3039), 'R_EX_C00760__dra': (0.0, 0.6188), 'R_EX_C00007__dra': (-5.0, -0.008659)}
carbon_source_production = {'R_EX_C00007__dra': (-1.0, -0.008659)}


for n, j in enumerate(carbon_source_production):
    s = float(carbon_source_production.get(j)[0])
    t = float(carbon_source_production.get(j)[1])

    if carbon_source_production.get(j)[0] < 0:
        p = 0.01
    else:
        s = float(carbon_source_production.get(j)[0])
        p = float(carbon_source_production.get(j)[1] - carbon_source_production.get(j)[0])/10

    print("===== " + str(s) + " ===== " + str(t)+ " ===== " + str(p))

    print(np.arange(s,t,p))

    for a, i in enumerate(np.arange(s,t,p)):
        constraints.update({j: (i, i)})
        print(constraints)

        simulProb_fva = StoicSimulationProblem(newModel, objective={bRXN: 1}, method="pFBA", constraints=constraints)
        optfva = simulProb_fva.simulate()

        if optfva.solverStatus == 1:

            print("===============================================================")
            print("FVA test: " + str(j) + ", step: " + str(i))
            print("===============================================================")

            print("Cellulose_fva: " + str(optfva.get_fluxes_distribution()[cell]))
            print("Biomass_fva: " + str(optfva.get_fluxes_distribution()[bRXN]))
            print("===============================================================")

            for r_id, rxn in newModel.reactions.items():
                # print(r_id + ": " + str(pfba.get_fluxes_distribution()[r_id]))
                if rxn.is_exchange or r_id.startswith('R_sink'):
                    met_list.append(rxn.get_substrates())
                    rxn_list.append(optfva.get_fluxes_distribution()[r_id])
                    # print(r_id + ": " + str(pfba.get_fluxes_distribution()[r_id]))

            met_list_merged = list(itertools.chain(*met_list))
            met_list_name = [1] * len(met_list_merged)

            for m_id, met in newModel.metabolites.items():
                for k in met_list_merged:
                    for l in range(0, len(met_list_merged)):
                        if met_list_merged[l] == m_id:
                            met_list_name[l] = str(met)

            for m in range(0, len(met_list_name)):
                exchange_dict.update({met_list_name[m]: rxn_list[m]})

            for key in exchange_dict:
                if exchange_dict[key] != 0:
                    Rxn.append(key)
                    Flux.append(exchange_dict[key])
                    print('Rxn: ' + str(key) + ', Flux: ' + str(exchange_dict[key]))
            dict_single = dict(zip(Rxn, Flux))
            print(dict_single)
            Rxn_lists.insert(a, Rxn)
            Flux_lists.insert(a, Flux)
            Rxn = []
            Flux = []
            dict_data.append(dict_single)

            conditions.append(str(j) + "_step_" + str(i))


        else:
            print("No simulation results for " + str(j) + ", step: " + str(i))

        constraints.update({j: (s, t)})


    df = pd.DataFrame(dict_data, index = conditions)

    print(constraints)
    print(df)
    df.to_csv(os.path.join(basePath, 'fva_data_o2.csv'), sep=';')


