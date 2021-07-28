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

basePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DeCaF/Tests/examples/models/mpa2019/community_models"
savePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DeCaF/Tests/examples/models/mpa2019/Results"

model_id =[]
carbon_source = []
biomass_rxn = []

for file in os.listdir(basePath):
    if file.endswith("_n.csv"):
        FILE = (os.path.join(basePath, file))
        csvFile = open(FILE, 'r')
        reader = csv.reader(csvFile, delimiter=';')
        next(reader, None)  # ignore header

        for row in reader:
            model_id.append(row[0])
            biomass_rxn.append(row[2])
            carbon_source.append(row[3])

def medium_optim_all (isMultiProc=False, size=1, withCobraPy = False):
    nFiles = 0
    for file in os.listdir(basePath):
        if file.endswith(".xml"):
            SBML_FILE =(os.path.join(basePath, file))
            print(file)
            model = load_cbmodel(SBML_FILE, flavor='fbc2')
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

            for i in range(0,len(model_id)):
                for mID in model_id:
                    if mID == newModel.id:
                        j = model_id.index(mID)
                        cSource = carbon_source[j]
                        bRXN = biomass_rxn[j]

            constraints = []
            for r_id, rxn in newModel.reactions.items():
                if r_id.startswith(cSource):
                    constraints = {r_id: (-99999, 0)}


            print("Number of drains: ", count)
            print("Constraints: ", constraints)

            simulProb = StoicSimulationProblem(newModel, objective = {bRXN:1}, withCobraPy = withCobraPy, method = "pFBA", constraints = constraints)

            pfba = simulProb.simulate()

            print("Biomass: " + str(pfba.get_fluxes_distribution()[bRXN]))

            #score = count / rxn_count

            #if score < 0.03 and score > 0.01:
            essential = simulProb.find_essential_drains()
            print("Essential: ",essential)

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



    #============= SET PARAMETERS ====================

            fileRes = savePath + "/medium_optim_"+ Id +".csv"

            if bFlux > 10:
                minObjective = {bRXN: 0.01}
            else:
                minObjective = {bRXN: bFlux * 0.1}

            evalFunc = build_evaluation_function("MinNumberReac",size, minObjective)

            if count > 50:
                size = int(count / 2) + 1
                cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, type=optimType.MEDIUM,
                                     criticalReacs=criticalReacs, isMultiProc=isMultiProc, candidateSize=size,
                                     resultFile=fileRes)  # KO_Reaction by default

            else:
                cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None, type = optimType.MEDIUM, criticalReacs = criticalReacs, isMultiProc=isMultiProc, candidateSize= size, resultFile=fileRes) #KO_Reaction by default
        nFiles += 1

if __name__ == '__main__':
    import time
    size = 20

    t1 = time.time()

    medium_optim_all(False, size, False)

    t2 = time.time()
    print ("time of FRAMED: " + str(t2 - t1))


