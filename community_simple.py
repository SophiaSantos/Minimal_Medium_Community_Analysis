import csv
import os

from framed import load_cbmodel, save_cbmodel, Environment, pFBA
from framed.community.model import Community
from optimModels.utils.utils import fix_exchange_reactions_model
from optimModels.simulation.simul_problems import StoicSimulationProblem
from reframed import SteadyCom

community_name = []
organism_list = []
o = []

basePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DD_DeCaF/Tests/examples/models/nitro"
list_models = []
constraints = {}

for file in os.listdir(basePath):
    if file.endswith("smetana_fbc2.xml"):
        SBML_FILE = (os.path.join(basePath, file))
        Id = file
        model = load_cbmodel(SBML_FILE, exchange_detection_mode='R_EX_')
        newModel = fix_exchange_reactions_model(model)
        newModel.biomass_reaction = "R_e_Biomass__cytop"
        list_models.append(newModel)

community = Community('Nitro', models = list_models, extracellular_compartment_id = 'C_e', interacting = True)
merged = community.merged
Environment.empty(merged, inplace=True)

print(merged.id)
newCommModel = fix_exchange_reactions_model(merged)

save_cbmodel(newCommModel, basePath + "/commModel_nitro.xml", flavor='fbc2')

minimal_medium = ['R_EX_M_so4_e_pool', 'R_EX_M_o2_e_pool', 'R_EX_M_pi_e_pool', 'R_EX_M_fe2_e_pool', 'R_EX_M_nh4_e_pool']

carbon_source = ['R_EX_M_co2_e_pool', 'R_EX_etoh_e_model_nvulgaris']

so4 = ['R_EX_M_so4_e_pool']

KO_pool = ['R_EX_M_no2_e_pool', 'R_EX_nh4_e_model_nvulgaris', 'R_EX_hco3_e_model_nvulgaris', 'R_EX_hdca_e_model_nvulgaris']


for r_id, rxn in newCommModel.reactions.items():
    if rxn.is_exchange:
        rxn.lb = -1000 if rxn.lb is None else rxn.lb
        rxn.ub = 1000 if rxn.ub is None else rxn.ub

print(newCommModel.biomass_reaction)

simulProb = StoicSimulationProblem(newCommModel, objective={'R_Community_Growth': 1}, method="pFBA")

pfba = simulProb.simulate()

essential = simulProb.find_essential_drains()
print("Essential; ", essential)

for i in minimal_medium:
    constraints.update ({i:(-1000, 0)})

for i in KO_pool:
    constraints.update({i: (0, 0)})

for i in carbon_source:
    constraints.update({i: (-1, 0)})

for i in so4:
    constraints.update({i: (-1, 0)})


print(constraints)


sol = StoicSimulationProblem(newCommModel, objective={'R_Community_Growth': 1}, method="pFBA", constraints= constraints)

commpfba = sol.simulate()


print("Biomass: " + str(commpfba.get_fluxes_distribution()['R_Community_Growth']))


for r_id, rxn in newCommModel.reactions.items():
    if rxn.is_exchange:
        if commpfba.get_fluxes_distribution()[r_id] != 0:
            print('Rxn: ' + str(r_id) + " Flux: " + str(commpfba.get_fluxes_distribution()[r_id]))

print('================================================================')

comm_sol = pFBA(newCommModel)
org_fluxes = community.split_fluxes(comm_sol.values)

for x in list_models:
    name = x.id
    if name in community.organisms:
        for r_id, rxn in newCommModel.reactions.items():
            if r_id.endswith('_e_'+ name):
                if commpfba.get_fluxes_distribution()[r_id] != 0:
                    print('Rxn: ' + str(r_id) + " Flux: " + str(commpfba.get_fluxes_distribution()[r_id]))
