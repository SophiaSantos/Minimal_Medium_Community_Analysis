from cobra.io import read_sbml_model
import os
from framed.io.sbml import load_cbmodel
from optimModels.optimization.evaluation_functions import build_evaluation_function
from optimModels.simulation.simul_problems import StoicSimulationProblem
from optimModels.optimization.run import cbm_strain_optim
from optimModels.utils.constantes import optimType
from optimModels.utils.configurations import StoicConfigurations
from optimModels.utils.utils import fix_exchange_reactions_model

basePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DD_DeCaF/Tests/examples/models/sophia_models"
savePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DD_DeCaF/Tests/examples/Results/sophia_models_results"

# Optimization:
# model: EC_SC_model (community model generated by sophia's tool)
# Obj Func: BPY (maximizes the production of succinate by the community model)
# type: reaction knockouts


def reac_ko_optim_CM(isMultiProc=False, size=1, withCobraPy=False):
    SBML_FILE = (os.path.join(basePath, 'model_saz_v7.xml'))
    model = load_cbmodel(SBML_FILE, exchange_detection_mode='R_EX_')
    newModel = fix_exchange_reactions_model(model)
    Id = model.id
    fileRes = savePath + "/optim_cell_"+ Id +".csv"

    constraints = {}
    constraints_c = {}

    for r_id, rxn in newModel.reactions.items():
        if r_id.startswith('R_EX_'):  # ou tambem podes fazer if rxn.is_exchange:
            rxn.lb = -1000 if rxn.lb is None else rxn.lb
            rxn.ub = 1000 if rxn.ub is None else rxn.ub

    bRXN = "R_e_Biomass__cytop"
    cSource = "R_EX_C00011__cytop"
    product = "R_EX_C00760__cytop"

    minimal_medium = ['R_EX_C00009__cytop', 'R_EX_C00014__cytop', 'R_EX_C00087__cytop', 'R_EX_C14818__cytop',
                      'R_EX_C00080__cytop', 'R_EX_C00007__cytop']

    complete_medium = ['R_EX_C00007__cytop', 'R_EX_C00025__cytop', 'R_EX_C00037__cytop', 'R_EX_C00041__cytop', 'R_EX_C00047__cytop', 'R_EX_C00049__cytop', 'R_EX_C00062__cytop', 'R_EX_C00064__cytop', 'R_EX_C00065__cytop','R_EX_C00073__cytop','R_EX_C00078__cytop', 'R_EX_C00079__cytop', 'R_EX_C00082__cytop', 'R_EX_C00097__cytop', 'R_EX_C00123__cytop', 'R_EX_C00135__cytop', 'R_EX_C00148__cytop', 'R_EX_C00152__cytop', 'R_EX_C00183__cytop', 'R_EX_C00188__cytop', 'R_EX_C00407__cytop']

    for i in minimal_medium:
        constraints.update({i: (-1000, 0)})
        constraints_c.update({i: (-1000, 0)})

    for i in complete_medium:
        constraints_c.update({i: (-1, 0)})


    for i in cSource:
        constraints.update({i: (-15, 0)})
        constraints_c.update({i: (-15, 0)})

    print(constraints_c)

    simulProb = StoicSimulationProblem(model, objective={bRXN: 1}, method='pFBA', constraints=constraints_c)
    evalFunc = build_evaluation_function("BPCY", bRXN, product, cSource)

    result = cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, isMultiProc=isMultiProc,
                              candidateSize=size, resultFile=fileRes)
    result.print()