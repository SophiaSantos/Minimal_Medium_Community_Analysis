import os

from reframed import load_cbmodel
from reframed import Community, Environment
from reframed import SteadyCom, SteadyComVA

basePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DD_DeCaF/Tests/examples/models/nitro"

constraints = {}
list_models = []

for file in os.listdir(basePath):
    if file.endswith("smetana_fbc2.xml"):
        SBML_FILE = (os.path.join(basePath, file))
        Id = file
        model = load_cbmodel(SBML_FILE, exchange_detection='R_EX_')
        #newModel = fix_exchange_reactions_model(model)
        model.biomass_reaction = "R_e_Biomass__cytop"

        for r_id, rxn in model.reactions.items():
            if r_id.startswith('R_EX_'):
                rxn.lb = 0

        list_models.append(model)

#print(list_models)

community = Community('Nitro', models = list_models)
merged = community.merge_models()
#Environment.complete(merged, inplace=True)


for i in community.merged_model.reactions:
    if i.startswith('R_EX_') or i.startswith('R_Sink_'):
        constraints.update({i:(0,1000)})

print(constraints)

minimal_medium = ['R_EX_M_so4_e', 'R_EX_M_o2_e', 'R_EX_M_pi_e', 'R_EX_M_co2_e', 'R_EX_M_fe2_e', 'R_EX_M_etoh_e', 'R_EX_M_nh4_e']

biomass_exchange = ['R_EX_M_e_Biomass_e']

no2_pool = ['R_EX_M_no2_e']


for i in minimal_medium:
    constraints.update ({i:(-5, 0)})

for i in no2_pool:
    constraints.update({i: (0, 0)})


print('===============================================')
print('=== SteadyComm ===')

steady_sol = SteadyCom(community, constraints=constraints)

print(steady_sol)