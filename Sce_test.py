#=============== Medium Optimization for files in directory =====================#
from framed import load_cbmodel
from optimModels import build_evaluation_function
from optimModels.optimization.run import cbm_strain_optim
from optimModels.simulation.simul_problems import StoicSimulationProblem
from optimModels.utils.configurations import StoicConfigurations
from optimModels.utils.constantes import optimType
from optimModels.utils.utils import fix_exchange_reactions_model
import os

basePath = "C:/Users/Sophia Santos/OneDrive/Documentos/CEB/PycharmProjects/DD-DeCaF/Tests/examples"

def medium_optim_all (isMultiProc=False, size=1, withCobraPy = False):
    nFiles = 0
    for file in os.listdir(basePath + "/models/"):
        if file.startswith("iMM904"):
            SBML_FILE =(os.path.join(basePath + "/models/", file))
            print(file)
            model = load_cbmodel(SBML_FILE, flavor="cobra")
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
            constraints = []
            for r_id, rxn in newModel.reactions.items():
                if r_id.startswith('R_EX_glc_D'):
                    constraints = {r_id: (-10, 0)}
                if r_id.startswith('R_EX__glc_D'):
                    constraints = {r_id: (-10, 0)}
                if r_id.startswith('R_EX_GLC_D'):
                    constraints = {r_id: (-10, 0)}
                if r_id.startswith('R_EX_cpd00027_e'):
                    constraints = {r_id: (-10, 0)}


            print("Number of drains: ", count)
            print("Constraints: ", constraints)

            simulProb = StoicSimulationProblem(newModel, objective = {"R_biomass_SC5_notrace":1, "R_EX_succ_e":1}, withCobraPy = withCobraPy, method = "pFBA", constraints = constraints)

            pfba = simulProb.simulate()

            print("Biomass: " + str(pfba.get_fluxes_distribution()["R_biomass_SC5_notrace"]))
            print("Succinate: " + str(pfba.get_fluxes_distribution()["R_EX_succ_e"]))

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

            bFlux = pfba.get_fluxes_distribution()["R_biomass_SC5_notrace"]
            lFlux = pfba.get_fluxes_distribution()["R_EX_succ_e"]



    #============= SET PARAMETERS ====================

            fileRes = basePath + "/Results/medium_optim_succ_"+ Id +".csv"

            if lFlux > 10:
                minObjective = {"R_EX_succ_e":lFlux}
            else:
                minObjective = {"R_EX_succ_e":lFlux}

            evalFunc = build_evaluation_function("BPCY","R_biomass_SC5_notrace", "R_EX_succ_e", "R_EX_glc_D_e")

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
    size = 5

    t1 = time.time()

    medium_optim_all(False, size, False)

    t2 = time.time()
    print ("time of FRAMED: " + str(t2 - t1))


