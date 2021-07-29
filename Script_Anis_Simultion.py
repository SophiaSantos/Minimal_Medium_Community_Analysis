import os
import itertools
import pandas as pd
import csv

from framed import load_cbmodel
from reframed import pFBA, FBA, Environment
from optimModels.utils.utils import fix_exchange_reactions_model
from optimModels.simulation.simul_problems import StoicSimulationProblem

basePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DD_DeCaF/Tests/examples/models/anis_models"

met_list = []
rxn_list = []
met_dict = {}
flux_dict = {}
met_list_name=[]
exchange_dict = {}
constraints = {}
exchange_list = []

SBML_FILE = (os.path.join(basePath, 'iCHOv1.xml'))
model = load_cbmodel(SBML_FILE, flavor='fbc2')
newModel = fix_exchange_reactions_model(model)

medium_list_key = []
conditions = []
fluxes = []
info = []
d={}
cond_list = []
medium_list_values_early_akg0 = []

print(newModel.id)

for r_id, rxn in newModel.reactions.items():
    if rxn.is_exchange:
        rxn.lb = -1000 if rxn.lb is None else rxn.lb
        rxn.ub = 1000 if rxn.ub is None else rxn.ub

for file in os.listdir(basePath):
    if file.endswith("2.csv"):
        if file.startswith("anis"):
            FILE_e = (os.path.join(basePath, file))
            df = pd.read_csv(FILE_e, sep=';')

#print(list(df["Compound"]))

for i in df.columns:
    for col in df.columns:
        val = list(df[col])
        cond_list.append(val)

bRXN = "R_BIOMASS_cho"
bRXN_iGG = "R_BIOMASS_cho_producing"

simulProb_n = StoicSimulationProblem(newModel, objective = {bRXN_iGG:1}, method = "pFBA")

pfba_n = simulProb_n.simulate()

print("Biomass: " + str(pfba_n.get_fluxes_distribution()[bRXN_iGG]))

for r_id, rxn in newModel.reactions.items():
    if rxn.is_exchange:
        if pfba_n.get_fluxes_distribution()[r_id] < 0:
            constraints.update({r_id:(pfba_n.get_fluxes_distribution()[r_id], 0)})
            print('Rxn: ', r_id, ' Flux: ' + str(pfba_n.get_fluxes_distribution()[r_id]))
        #rxn.lb = 0

constraints.update({'R_EX_cys__L_e': (0.0, 1000), 'R_EX_Lcystin_e': (-0.0009599999999999999,1000)})


medium_list_key = cond_list[0]
medium_list_values_early_akg0_lb = cond_list[1]
medium_list_values_late_akg0_lb = cond_list[9]
medium_list_values_early_akg4_lb = cond_list[3]
medium_list_values_late_akg4_lb = cond_list[11]
medium_list_values_early_akg8_lb = cond_list[5]
medium_list_values_late_akg8_lb = cond_list[13]
medium_list_values_early_akg12_lb = cond_list[7]
medium_list_values_late_akg12_lb = cond_list[15]
medium_list_values_early_akg0_ub = cond_list[2]
medium_list_values_late_akg0_ub = cond_list[10]
medium_list_values_early_akg4_ub = cond_list[4]
medium_list_values_late_akg4_ub = cond_list[12]
medium_list_values_early_akg8_ub = cond_list[6]
medium_list_values_late_akg8_ub = cond_list[14]
medium_list_values_early_akg12_ub = cond_list[8]
medium_list_values_late_akg12_ub = cond_list[16]

medium_list_values = [medium_list_values_early_akg0_lb, medium_list_values_early_akg0_ub, medium_list_values_early_akg4_lb, medium_list_values_early_akg4_ub, medium_list_values_early_akg8_lb, medium_list_values_early_akg8_ub, medium_list_values_early_akg12_lb, medium_list_values_early_akg12_ub, medium_list_values_late_akg0_lb, medium_list_values_late_akg0_ub, medium_list_values_late_akg4_lb, medium_list_values_late_akg4_ub, medium_list_values_late_akg8_lb, medium_list_values_late_akg8_ub, medium_list_values_late_akg12_lb, medium_list_values_late_akg12_ub]

for n, i in enumerate(medium_list_values):
    if n % 2 == 0 and n >= 8:
        p = n + 1
        for m, j in enumerate(i):
            if j <= 0:
                ub = medium_list_values[p]
                i[m] = (j, ub[m])
            else:
                ub = medium_list_values[p]
                i[m] = (0, ub[m])
        new_n = medium_list_values[n]
        for h, k in enumerate(new_n):
            constraints.update({medium_list_key[h]: new_n[h]})
        print("Constraints: " + str(constraints))


        simulProb = StoicSimulationProblem(newModel, objective = {bRXN_iGG:1}, method = "pFBA", constraints=constraints)
        print('===================')
        print(simulProb.constraints)
        pfba = simulProb.simulate()
        print("Biomass: " + str(pfba.get_fluxes_distribution()[bRXN_iGG]))

        for r_id, rxn in newModel.reactions.items():
            if rxn.is_exchange:
                if pfba.get_fluxes_distribution()[r_id] != 0:
                    print('Rxn: ', r_id, ' Flux: ' + str(pfba.get_fluxes_distribution()[r_id]))

        print('===========================')
        print(pfba.get_fluxes_distribution())
