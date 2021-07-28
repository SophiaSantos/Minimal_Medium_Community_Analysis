#=============== Medium Optimization for files in directory =====================#
from framed import load_cbmodel
from optimModels import build_evaluation_function
from optimModels.optimization.run import cbm_strain_optim
from optimModels.simulation.simul_problems import StoicSimulationProblem
from optimModels.utils.configurations import StoicConfigurations
from optimModels.utils.constantes import optimType
from optimModels.utils.utils import fix_exchange_reactions_model
import os
import csv

basePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DD_DeCaF/Tests/examples/models/sophia_models"
savePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DD_DeCaF/Tests/examples/Results/sophia_models_results"

model_id =[]
carbon_source = []
biomass_rxn = []

#for file in os.listdir(basePath):
#    if file.endswith(".csv"):
#        FILE = (os.path.join(basePath, file))
#        csvFile = open(FILE, 'r')
#        reader = csv.reader(csvFile, delimiter=';')
#        next(reader, None)  # ignore header
#
#        for row in reader:
#            model_id.append(row[0])
#            biomass_rxn.append(row[2])
#            carbon_source.append(row[3])

def medium_optim_all (isMultiProc=False, size=(1,1), withCobraPy = False):
    nFiles = 0
    for file in os.listdir(basePath):
        if file.endswith("_v8.xml"):
            SBML_FILE =(os.path.join(basePath, file))
            print(file)
            model = load_cbmodel(SBML_FILE, exchange_detection_mode ="R_EX_")
            Id = file

            for r_id, rxn in model.reactions.items():
                if rxn.is_exchange:  # ou tambem podes fazer if rxn.is_exchange:
                    rxn.lb = -1000 if rxn.lb is None else rxn.lb
                    rxn.ub = 1000 if rxn.ub is None else rxn.ub
            newModel = fix_exchange_reactions_model(model)
            count = rxn_count = 0
            for r_id, rxn in newModel.reactions.items():
                rxn_count += 1
                if rxn.is_exchange:
                    rxn.lb = -10
                    rxn.ub = 10
                    #print(rxn)
                    count+=1
                if r_id.startswith('R_sink_'):
                    rxn.lb = 0


#            for i in range(0,len(model_id)):
#                for mID in model_id:
#                    if mID == newModel.id:
#                        j = model_id.index(mID)
#                        cSource = carbon_source[j]
#                        bRXN = biomass_rxn[j]

            bRXN = "R_e_Biomass__cytop"
            cSource = "R_EX_C00041__cytop"
            product = "R_EX_C00760__cytop"

            constraints = []
            constraints_c = {}
            for r_id, rxn in newModel.reactions.items():
                if r_id.startswith('R_ATPm'):
                    rxn.lb = 8.39
                    rxn.ub = 8.39
                #if rxn.is_exchange:
                #    rxn.lb = 0
                #if r_id.startswith(cSource):
                #    constraints = {r_id: (-15, 0)}

            #minimal_medium = ['R_EX_C00009__cytop', 'R_EX_C00014__cytop', 'R_EX_C00087__cytop', 'R_EX_C14818__cytop',
            #                  'R_EX_C00080__cytop', 'R_EX_C00007__cytop']

            #complete_medium = ['R_EX_C00007__cytop', 'R_EX_C00025__cytop', 'R_EX_C00037__cytop', 'R_EX_C00041__cytop',
            #                   'R_EX_C00047__cytop', 'R_EX_C00049__cytop', 'R_EX_C00062__cytop', 'R_EX_C00064__cytop',
            #                   'R_EX_C00065__cytop', 'R_EX_C00073__cytop', 'R_EX_C00078__cytop', 'R_EX_C00079__cytop',
            #                   'R_EX_C00082__cytop', 'R_EX_C00097__cytop', 'R_EX_C00123__cytop', 'R_EX_C00135__cytop',
            #                   'R_EX_C00148__cytop', 'R_EX_C00152__cytop', 'R_EX_C00183__cytop', 'R_EX_C00188__cytop',
            #                   'R_EX_C00407__cytop']
            carbon_source=["R_EX_C00041__cytop"]

            #for i in minimal_medium:
            #    constraints.update({i: (-1000, 0)})
            #    constraints_c.update({i: (-1000, 0)})

            #for i in complete_medium:
            #    constraints_c.update({i: (-1, 0)})

            #for i in carbon_source:
            #    constraints.update({i: (-15, 0)})
            #    constraints_c.update({i: (-15, 0)})

            #print(constraints_c)

            print("Number of drains: ", count)
            #print("Constraints: ", constraints)

            simulProb = StoicSimulationProblem(newModel, objective = {bRXN:1}, method = "pFBA", constraints=constraints)

            pfba = simulProb.simulate()

            print("Biomass: " + str(pfba.get_fluxes_distribution()[bRXN]))

            #score = count / rxn_count

            #if score < 0.03 and score > 0.01:
            essential = simulProb.find_essential_drains()
            print("Essential: ", essential)

            if simulProb.constraints:
                 simulProb.constraints.update(
                    {reac: (StoicConfigurations.DEFAULT_LB, 0) for reac in essential})  # put essential reactions as constraints
            else:
                simulProb.constraints = {reac: (StoicConfigurations.DEFAULT_LB, 0) for reac in essential}

            cR = []
            for key in simulProb.constraints.keys():
                cR.append(key)

            criticalReacs = cR

            print("Critical: ", criticalReacs)

            bFlux = pfba.get_fluxes_distribution()[bRXN]

            print(pfba.get_fluxes_distribution())


    #============= SET PARAMETERS ====================

            #fileRes = savePath + "/medium_optim_cell"+ Id +".csv"
            fileRes = savePath + "/optim_KO_medium_cell_" + Id + ".csv"

            if bFlux > 10:
                minObjective = {bRXN: 0.01}
            else:
                minObjective = {bRXN: bFlux * 0.1}

            #evalFunc = build_evaluation_function("MinNumberReac",size, minObjective)
            #evalFunc = build_evaluation_function("BPCY", bRXN, product, cSource)
            evalFunc = build_evaluation_function("BP_MinModifications", bRXN, product)
            if count > 50:
                #size = int(count / 2) + 1
                #size=100
                size = (20,20)

                #cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, type=optimType.MEDIUM,
                #                     criticalReacs=criticalReacs, isMultiProc=isMultiProc, candidateSize=size,
                #                     resultFile=fileRes)
                cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, type=optimType.MEDIUM_REACTION_KO,
                                     criticalReacs=criticalReacs, isMultiProc=isMultiProc, candidateSize=size,
                                     resultFile=fileRes)  # KO_Reaction by default

            else:
                #cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, type = optimType.MEDIUM, criticalReacs = criticalReacs, isMultiProc=isMultiProc, candidateSize= size, resultFile=fileRes) #KO_Reaction by default
                cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, type=optimType.MEDIUM_REACTION_KO,
                                 criticalReacs=criticalReacs, isMultiProc=isMultiProc, candidateSize=size,
                                 resultFile=fileRes)  # KO_Reaction by default
        nFiles += 1

if __name__ == '__main__':
    import time
    size = (20, 20)

    t1 = time.time()

    medium_optim_all(False, size, False)

    t2 = time.time()
    print ("time of FRAMED: " + str(t2 - t1))