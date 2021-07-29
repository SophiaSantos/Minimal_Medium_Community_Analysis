#=============== Strain Optimization for files in directory =====================#
from framed import load_cbmodel, FBA
from optimModels import build_evaluation_function
from optimModels.optimization.run import cbm_strain_optim
from optimModels.simulation.simul_problems import StoicSimulationProblem
from optimModels.utils.configurations import StoicConfigurations
from optimModels.utils.constantes import optimType
from optimModels.utils.utils import fix_exchange_reactions_model
import os

basePath = "C:/Users/Sophia Santos/PycharmProjects/DD-DeCaF/Tests/examples/"

#KO optimization
def reac_ko_optim_CM_2(isMultiProc=False, size=1, withCobraPy = False):
    SBML_two = "C:/Users/Sophia Santos/PycharmProjects/DD-DeCaF/Tests/examples/models/DD_DeCaF_report/Two_species_optlux.xml" #usar modelo com minimal medium definido!
    model_two_aux = load_cbmodel(SBML_two, exchange_detection_mode='unbalanced')
    model_two = fix_exchange_reactions_model(model_two_aux)
    name_two = model_two.id

    fileRes_two = basePath + "/Results/optim_" + name_two + "_MM_KO.csv"

    for r_id, rxn in model_two.reactions.items():
        if rxn.is_exchange:  # ou tambem podes fazer if rxn.is_exchange:
            rxn.lb = -10 if rxn.lb is None else rxn.lb
            rxn.ub = 10 if rxn.ub is None else rxn.ub

    for r_id, rxn in model_two.reactions.items():
        if rxn.is_exchange:
            rxn.lb = 0
            rxn.ub = 100000
            # print(r_id, rxn.lb)

    constraints_two = {'R_N_up_MM':(-10,100000), 'R_N_up':(-10,100000), 'R_Ac_Medium_in':(-10,100000), 'R_Form_Medium':(-10,100000)}

    simulProb_two = StoicSimulationProblem(model_two, objective={"R_BM_tot_Synth": 1}, withCobraPy=withCobraPy,
                                             constraints=constraints_two, method='pFBA')

    pfba_two=simulProb_two.simulate()


    print(pfba_two.get_fluxes_distribution()["R_BM_tot_Synth"])

    evalFunc_form = build_evaluation_function("BPCY", "R_BM_tot_Synth","R_Meth_Medium", "R_Form_Medium")
    evalFunc_ac = build_evaluation_function("BPCY", "R_BM_tot_Synth", "R_Meth_Medium", 'R_Ac_Medium_in')

    #result_form = cbm_strain_optim(simulProb_two, evaluationFunc=evalFunc_form, levels=None, isMultiProc=isMultiProc, candidateSize= size, resultFile=fileRes_two) #KO_Reaction by default
    result_ac = cbm_strain_optim(simulProb_two, evaluationFunc=evalFunc_ac, levels=None, isMultiProc=isMultiProc, candidateSize= size, resultFile=fileRes_two) #KO_Reaction by default


# KO optimization
def reac_ko_optim_CM_3(isMultiProc=False, size=1, withCobraPy=False):
    SBML_three = "C:/Users/Sophia Santos/PycharmProjects/DD-DeCaF/Tests/examples/models/DD_DeCaF_report/Three_species_optflux.xml"  # usar modelo com minimal medium definido!
    model_three_aux = load_cbmodel(SBML_three, exchange_detection_mode='unbalanced')
    model_three = fix_exchange_reactions_model(model_three_aux)
    name_three = model_three.id

    fileRes_three = basePath + "Results/optim_" + name_three + "_MM_KO.csv"

    for r_id, rxn in model_three.reactions.items():
        if rxn.is_exchange:  # ou tambem podes fazer if rxn.is_exchange:
            rxn.lb = -10 if rxn.lb is None else rxn.lb
            rxn.ub = 10 if rxn.ub is None else rxn.ub

    for r_id, rxn in model_three.reactions.items():
        if rxn.is_exchange:
            rxn.lb = 0
            rxn.ub = 100000
            # print(r_id, rxn.lb)

    constraints_three = {'R_N_up_DV':(-10,100000), 'R_N_up_MM':(-10,100000), 'R_N_up_MB':(-10,100000), 'R_Lac_Medium':(-10,100000)}

    simulProb_three = StoicSimulationProblem(model_three, objective={"R_BM_tot_Synth": 1}, withCobraPy=withCobraPy,
                                             constraints=constraints_three, method='pFBA')

    pfba_three = simulProb_three.simulate()

    print(pfba_three.get_fluxes_distribution()["R_BM_tot_Synth"])

    evalFunc_lac = build_evaluation_function("BPCY", "R_BM_tot_Synth", "R_Meth_Medium", "R_Lac_Medium")

    result_three = cbm_strain_optim(simulProb_three, evaluationFunc=evalFunc_lac, levels=None,
                                    isMultiProc=isMultiProc, candidateSize=size,
                                    resultFile=fileRes_three)  # KO_Reaction by default


# KO optimization
def reac_ko_optim_CM_EC_SC(isMultiProc=False, size=1, withCobraPy=False):
    SBML = "C:/Users/Sophia Santos/PycharmProjects/DD-DeCaF/Tests/examples/models/DD_DeCaF_report/EC_SC.xml"  # usar modelo com minimal medium definido!
    modelaux = load_cbmodel(SBML, exchange_detection_mode='R_EX_')
    model = fix_exchange_reactions_model(modelaux)
    name = model.id

    fileRes = basePath + "Results/optim_" + name + "_MM_KO.csv"

    for r_id, rxn in model.reactions.items():
        if r_id.startswith('R_EX_'):
            rxn.lb = 0
            rxn.ub = 100000
            # print(r_id, rxn.lb)

    constraints = {'R_EX_glc_D_medium_': (-10, 100000), 'R_EX_mobd_e__mod1': (-100000, 100000), 'R_EX_mn2_e__mod1': (-100000, 100000), 'R_EX_ca2_e__mod1': (-100000, 100000), 'R_EX_k_medium_': (-100000, 100000), 'R_EX_cobalt2_e__mod1': (-100000, 100000), 'R_EX_zn2_e__mod1': (-100000, 100000), 'R_EX_mg2_e__mod1': (-100000, 100000), 'R_EX_cl_e__mod1': (-100000, 100000), 'R_EX_so4_medium_': (-100000, 100000), 'R_EX_o2s_e__mod1': (-100000, 100000), 'R_EX_amp_e__mod1': (-10, 100000), 'R_EX_cu2_e__mod1': (-100000, 100000), 'R_EX_fe3hox_e__mod1': (-100000, 100000)}

    simulProb = StoicSimulationProblem(model, objective={"R_BM_comm": 1}, withCobraPy=withCobraPy,
                                             constraints=constraints, method='pFBA')

    pfba = simulProb.simulate()

    print(pfba.get_fluxes_distribution()["R_BM_comm"])

    evalFunc = build_evaluation_function("BPCY", "R_BM_comm", "R_EX_succ_medium_", "R_EX_glc_D_medium_")

    result_three = cbm_strain_optim(simulProb, evaluationFunc=evalFunc, levels=None,
                                    isMultiProc=isMultiProc, candidateSize=size,
                                    resultFile=fileRes)  # KO_Reaction by default

# Simulation of the best results:
def cbm_simualtion():
    sbml_file = "C:/Users/Sophia Santos/PycharmProjects/DD-DeCaF/Tests/examples/models/DD_DeCaF_report/Three_species_optflux.xml"

    model = load_cbmodel(sbml_file, exchange_detection_mode="unbalanced")
    newModel = fix_exchange_reactions_model(model)
    for r_id, rxn in newModel.reactions.items():
        if rxn.is_exchange:  # ou tambem podes fazer if rxn.is_exchange:
            rxn.lb = 0
            rxn.ub = 100000

    constraints = {'R_N_up_DV':(-10,100000), 'R_N_up_MM':(-10,100000), 'R_N_up_MB':(-10,100000), 'R_Lac_Medium':(-10,100000), 'R_NADP_Hydrogenase_MM':(0,0), 'R_AcCoA_DV__Adh_DV':(0,0), 'R_Form_MM__CO2_MM':(0,0), 'R_CO2_DV__CO2_EX':(0,0), 'R_H2_EX__H2_MB':(0,0), 'R_PGlac_MB__PGluc_MB':(0,0)}

    simulProb_three = StoicSimulationProblem(newModel, objective={"R_BM_tot_Synth": 1},
                                             constraints=constraints, method='pFBA')

    pfba= simulProb_three.simulate()

    print(pfba.get_fluxes_distribution()["R_BM_tot_Synth"])
    print(pfba.get_fluxes_distribution()["R_Meth_Medium"])



if __name__ == '__main__':
    import time
    size = 10

    t1 = time.time()

    #eac_ko_optim_CM_EC_SC(False, size, False)
    #reac_ko_optim_CM_3(False, size, False)
    #reac_ko_optim_CM_2(False, size, False)
    cbm_simualtion()


    t2 = time.time()
    print ("time of FRAMED: " + str(t2 - t1))

    t1 = time.time()

    t2 = time.time()
    print ("time of COBRAPY: " + str(t2 - t1))
