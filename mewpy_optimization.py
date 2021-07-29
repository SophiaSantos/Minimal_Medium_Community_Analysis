import os

from reframed.io.sbml import load_cbmodel
from cobra.io import read_sbml_model

from mewpy.simulation import get_simulator

from mewpy.optimization import EA
from mewpy.optimization.evaluation import BPCY
from mewpy.optimization.evaluation import WYIELD
from mewpy.problems import RKOProblem

basePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DD_DeCaF/Tests/examples/models/sophia_models"

SBML_FILE = (os.path.join(basePath, 'model_saz_v17.xml'))
model = load_cbmodel(SBML_FILE, exchange_detection='R_EX_')
#model = read_sbml_model(SBML_FILE)

constraints = {}
print(model.id)

simul = get_simulator(model)

for r_id in simul.reactions:
    if r_id.startswith('R_ATPM'):
        constraints.update({r_id: (8.39, 8.39)})
    if r_id.startswith('R_EX_'):
        constraints.update({r_id: (0, 1000)})
    if r_id.startswith('R_sink_'):
        constraints.update({r_id: (0, 1000)})

bRXN = 'R_e_Biomass__cytop'
cell = 'R_EX_C00760__dra'

carbon_source = ['R_EX_C00011__dra']
essential = ['R_EX_C14818__dra', 'R_EX_C00009__dra', 'R_EX_C00001__dra']
minimal_medium = ['R_EX_C00014__dra', 'R_EX_C00087__dra', 'R_EX_C00282__dra']
oxygen = ['R_EX_C00007__dra']


for r_id, rxn in model.reactions.items():
    for i in minimal_medium:
        if r_id==i:
            rxn.lb = -1000
    for j in essential:
        if r_id==j:
            rxn.lb = -1000
    for k in oxygen:
        if r_id==k:
            rxn.lb = -5
    for c in carbon_source:
        if r_id==c:
            rxn.lb = -15

for r_id, rxn in model.reactions.items():
    if r_id.startswith('R_EX_'):
        print(str(r_id) +": " + str(rxn.lb) + " " + str(rxn.ub))

model.biomass_reaction = bRXN

simul.objective = bRXN
result = simul.simulate(method = 'pFBA', constraints=constraints)
print(result.fluxes)

#simul.essential_reactions

#simul.essential_genes

#evaluator_1 = WYIELD (bRXN,cell)

#evaluator_2 = BPCY(bRXN,cell, method ='lMOMA')

#problem = RKOProblem(model,
#              fevaluation=[evaluator_1, evaluator_2],
#              envcond=envcond)

#ea = EA(problem, max_generations=100,algorithm='NSGAIII')
#ea.run()