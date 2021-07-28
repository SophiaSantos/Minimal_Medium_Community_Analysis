#=============== Medium Optimization for files in directory =====================#
from framed import load_cbmodel
from optimModels.simulation.simul_problems import StoicSimulationProblem
from optimModels.utils.configurations import StoicConfigurations
from optimModels.utils.utils import fix_exchange_reactions_model
import os
import csv

basePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DD_DeCaF/Tests/examples/models/sophia_models"

def medium_optim_all (isMultiProc=False, size=1, withCobraPy = False):
    nFiles = 0

    #model_id = []
    #carbon_source = []
    #biomass_rxn = []

    cSource = "R_EX_C00011__dra"
    bRXN = "R_e_Biomass__cytop"

    #for file in os.listdir(basePath):
    #   if file.endswith(".csv"):
    #        FILE = (os.path.join(basePath, file))
    #        csvFile = open(FILE, 'r')
    #        reader = csv.reader(csvFile, delimiter=';')
    #        next(reader, None)  # ignore header

    #        for row in reader:
    #            model_id.append(row[0])
    #            biomass_rxn.append(row[2])
    #            carbon_source.append(row[3])

    for file in os.listdir(basePath):
        if file.endswith("saz_v17.xml"):
            SBML_FILE =(os.path.join(basePath, file))

            model = load_cbmodel(SBML_FILE, exchange_detection_mode='R_EX_')
            newModel = fix_exchange_reactions_model(model)
            count = rxn_count = 0

            for r_id, rxn in newModel.reactions.items():
                rxn_count+=1
                if rxn.is_exchange:  # ou tambem podes fazer if rxn.is_exchange:
                    rxn.lb = -10
                    rxn.ub = 10
                    count += 1

            #for i in range(0,len(model_id)):
            #    for mID in model_id:
            #        if mID == newModel.id:
            #            j = model_id.index(mID)
            #            cSource = carbon_source[j]
            #            bRXN = biomass_rxn[j]

            constraints = []
            #for r_id, rxn in newModel.reactions.items():
            #   if r_id.startswith(cSource):
            #       constraints = {r_id: (-99999, 0)}

            #print("Number of drains; ", count)
            #print("Number of reactions; ", rxn_count)
            #print("Constraints; ", constraints)

            #simulProb = StoicSimulationProblem(newModel, objective = {"R_BM_tot_Synth":1}, withCobraPy = withCobraPy, method = "pFBA", constraints = constraints)
            simulProb = StoicSimulationProblem(newModel, objective={bRXN: 1}, withCobraPy=withCobraPy,
                                               method="pFBA", constraints=constraints)

            pfba = simulProb.simulate()
            #if pfba.solverStatus == 1:
                #print("Biomass; " + str(pfba.get_fluxes_distribution()["R_BM_tot_Synth"]))
                #print("Biomass; " + str(pfba.get_fluxes_distribution()["R_BIOMASS"]))
            #else:
                #print("Solver status"+ str(pfba.solverStatus))

            if (count/rxn_count) > 0.01:
                essential = simulProb.find_essential_drains()
                #print("Essential; ",essential)

                if simulProb.constraints:
                    simulProb.constraints.update(
                        {reac: (StoicConfigurations.DEFAULT_LB, 0) for reac in essential})  # put essential reactions as constraints
                else:
                    simulProb.constraints = {reac: (StoicConfigurations.DEFAULT_LB, 0) for reac in essential}

                cR = []
                for key in simulProb.constraints.keys():
                    cR.append(key)

                criticalReacs = cR

                print( file, "\t", criticalReacs)


            nFiles += 1

if __name__ == '__main__':
    import time
    size = 20

    t1 = time.time()

    medium_optim_all(False, size, False)

    t2 = time.time()
    print ("time of FRAMED: " + str(t2 - t1))


