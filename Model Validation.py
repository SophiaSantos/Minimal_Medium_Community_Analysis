import os
import itertools

from framed import load_cbmodel
from optimModels.utils.utils import fix_exchange_reactions_model
from optimModels.simulation.simul_problems import StoicSimulationProblem


basePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DD_DeCaF/Tests/examples/models/sophia_models"
basePath_r = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DD_DeCaF/Tests/examples/"

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

#KO = ['R_EX_C06251__dra', 'R_EX_C06026__dra', 'R_EX_C06024__dra', 'R_EX_C06025__dra', 'R_EX_C00344__dra', 'R_EX_C01102__dra', 'R_EX_C01165__dra', 'R_EX_C00680__dra', 'R_EX_C00249__dra', 'R_EX_C00078__dra', 'R_EX_C00013__dra', 'R_EX_C00155__dra', 'R_EX_C00217__dra', 'R_EX_C00263__dra', 'R_EX_C00077__dra', 'R_EX_C00033__dra', 'R_EX_C00441__dra', 'R_EX_C00666__dra']
#KO = ['R_EX_C06251__dra', 'R_EX_C06026__dra', 'R_EX_C06024__dra', 'R_EX_C06025__dra']
KO = []

SBML_FILE = (os.path.join(basePath, 'model_saz_v18.xml'))
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
#        rxn.lb = 0
        rxn.lb = -10
        exchange_list.append(r_id)
    if r_id.startswith('R_sink_'):
        rxn.lb = 0
        exchange_list.append(r_id)

bRXN = "R_e_Biomass__cytop"

co2 = 'R_EX_C00011__dra'

carbon_source_list = ['R_EX_C00025__dra', 'R_EX_C00037__dra', 'R_EX_C00041__dra', 'R_EX_C00047__dra', 'R_EX_C00049__dra', 'R_EX_C00062__dra', 'R_EX_C00064__dra', 'R_EX_C00065__dra','R_EX_C00073__dra', 'R_EX_C00079__dra', 'R_EX_C00082__dra', 'R_EX_C00097__dra', 'R_EX_C00123__dra', 'R_EX_C00135__dra', 'R_EX_C00148__dra', 'R_EX_C00152__dra', 'R_EX_C00183__dra', 'R_EX_C00188__dra', 'R_EX_C00407__dra']

carbon_source = ['R_EX_C00011__dra']

essential = ['R_EX_C14818__dra']

minimal_medium = ['R_EX_C00014__dra', 'R_EX_C00087__dra', 'R_EX_C00001__dra', 'R_EX_C00009__dra', 'R_EX_C00080__dra']

cell = 'R_EX_C00760__dra'

oxygen = ['R_EX_C00007__dra']

starvation = ['R_EX_C00014__dra']

newModel.biomass_reaction = 'R_e_Biomass__cytop'

#for i in optim_medium:
#    constraints.update({i: (-0.5, 1000)})

for i in minimal_medium:
    constraints.update({i: (-1000, 1000)})

for i in carbon_source_list:
    constraints.update({i: (0, 1000)})

for i in essential:
    constraints.update({i: (-1000, 1000)})

for i in oxygen:
    constraints.update({i: (-0.01, 0)})
for i in starvation:
    constraints.update({i: (-0.25, 0)})

for i in carbon_source:
    constraints.update({i: (-12, 0)})

for i in KO:
    constraints.update({i: (0, 0)})

print(constraints)

for j in carbon_source:

    constraints.update({j: (-12, -12)})
    print(constraints)

    simulProb = StoicSimulationProblem(newModel, objective={bRXN: 1}, method="pFBA", constraints=constraints)
    pfba = simulProb.simulate()

    if pfba.solverStatus == 1:

        print("===============================================================")

        print("Cellulose: " + str(pfba.get_fluxes_distribution()[cell]))
        print("Biomass: " + str(pfba.get_fluxes_distribution()[bRXN]))
        print("===============================================================")

        #fva = FVA(newModel, obj_percentage=0.1,reactions=['R_EX_C00760__dra', 'R_EX_C00014__dra', 'R_EX_C00087__dra', 'R_EX_C14818__dra','R_EX_C00080__dra', 'R_EX_C00007__dra', 'R_EX_C00009__dra', 'R_EX_C00288__dra','R_EX_C00993__dra', 'R_EX_C00033__dra'], constraints=constraints)

        constraints.update({bRXN:(pfba.get_fluxes_distribution()[bRXN]*0.7, 1000)})

        optProb = StoicSimulationProblem(newModel, objective = {cell:1}, method = "pFBA", constraints=constraints)

        optpfba = optProb.simulate()

        print("Cellulose_optm: " + str(optpfba.get_fluxes_distribution()[cell]))
        print("Biomass_optm_cellulose: " + str(optpfba.get_fluxes_distribution()[bRXN]))
        print("===============================================================")

        #essentialRxn = essential_reactions(newModel, min_growth=0.7, constraints=constraints)

        constraints.update({i: (0, 0)})

        for r_id, rxn in newModel.reactions.items():
            # print(r_id + ": " + str(pfba.get_fluxes_distribution()[r_id]))
            if rxn.is_exchange or r_id.startswith('R_sink'):
                met_list.append(rxn.get_substrates())
                rxn_list.append(pfba.get_fluxes_distribution()[r_id])
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

    print('=========== Flux distribuition ================')
    print(pfba.get_fluxes_distribution())
    print('============ Essential Reactions ===============')
    #print(essentialRxn)
    print('============ FVA results ===============')
    #print(fva)


#for r_id, rxn in newModel.reactions.items():
#    print(rxn)


