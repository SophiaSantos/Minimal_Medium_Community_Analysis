#=============== Evaluation of Minimnal Medium solutions from files in directory =====================#
from framed import load_cbmodel
from optimModels.simulation.simul_problems import StoicSimulationProblem
from optimModels.utils.utils import fix_exchange_reactions_model
import os
import csv
import ast

basePath_csv = "C:/Users/Sophia Santos/Desktop/mpa2019_data"
basePath_xml = "C:/Users/Sophia Santos/Desktop/mpa2019_data/models/"

#basePath_xml="C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DeCaF/Tests/examples/models/joana_models"
#basePath_csv = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DeCaF/Tests/examples/Results/joana_models_results"
#===Variables===

model_id_xml = []
model_id_csv = []
constraints = []
biomass_rxn = []
carbon_source = []
minimalM_exp = []
medium_exp = {}
cs = ''

#bRXN = "R_BIOMASS"
#cSource = "R_EX_glc_"

nCarbons = []
expMedium = []

for file in os.listdir(basePath_xml):
    if file.startswith("community_composition"):
        FILE = (os.path.join(basePath_xml, file))
        csvFile = open(FILE, 'r')
        reader = csv.reader(csvFile, delimiter=';')
        next(reader, None)  # ignore header

        for row in reader:
            model_id_xml.append("community_"+row[0]+".xml")
            biomass_rxn.append(row[2])
            carbon_source.append(row[3])
            nCarbons.append(row[4])
            expMedium.append(row[5])


for file in os.listdir(basePath_csv):
    if file.startswith("minimal_medium_optim"):
        FILE = (os.path.join(basePath_csv, file))
        csvFile = open(FILE, 'r')
        reader = csv.reader(csvFile, delimiter=';')
        next(reader, None)  # ignore header

        for row in reader:
            model_id_csv.append(row[0])
            constraints.append(row[1])

model_id_m = []
essential = []

for file_m in os.listdir(basePath_csv):
    if file_m.startswith("essential_output_c"):
        FILE_m = (os.path.join(basePath_csv, file_m))
        csvFile_m = open(FILE_m, 'r')
        reader_m = csv.reader(csvFile_m, delimiter=';')
        next(reader_m, None)  # ignore header

        for row in reader_m:
            print(row)
            model_id_m.append(row[0])
            #essential.append(row[1])
#print(model_id_m)
for file in os.listdir(basePath_xml):
    if file.endswith(".xml"):
        Id = file
        for mID in model_id_csv:
            if mID == file:
                j = model_id_csv.index(mID)
                constr_vector = constraints[j]
                constr_vector_ar = ast.literal_eval(constr_vector) # trasnformar str em array
                cSource = carbon_source[j]
                bRXN = biomass_rxn[j]

                medium = {}
                medium_opt = {}
                medium_exp = {}
                medium_official = []
                comparison = {}

                SBML_FILE = (os.path.join(basePath_xml, file))
                model = load_cbmodel(SBML_FILE, flavor="fbc2")
                #model = load_cbmodel(SBML_FILE, exchange_detection_mode="unbalanced")
                newModel = fix_exchange_reactions_model(model)
                for r_id, rxn in newModel.reactions.items():
                    if rxn.is_exchange:
                        rxn.lb = -10 if rxn.lb is None else rxn.lb
                        rxn.ub = 10 if rxn.ub is None else rxn.ub
                        if rxn.lb != 0:
                            medium.update({r_id:(rxn.lb, rxn.ub)})

                        for met in constr_vector_ar:
                            for m in medium.keys():
                                if m == met and m == r_id:
                                    medium_opt.update({r_id:(rxn.lb, rxn.ub)})
                            else:
                                if met == r_id:
                                    medium_opt.update({r_id:(-10, rxn.ub)})

                        for met in expMedium:
                            for m in medium.keys():
                                if m == met and m == r_id:
                                    medium_exp.update({r_id:(rxn.lb, rxn.ub)})
                            else:
                                if met == r_id:
                                    medium_exp.update({r_id:(-10, rxn.ub)})

                        if r_id.startswith(cSource):
                            cs = r_id
                            medium.update({r_id:(-0.01, -0.001)})
                            medium_opt.update({r_id:(-10, -0.1)})
                            medium_exp.update({r_id: (-10, -0.1)})


                for r_id, rxn in newModel.reactions.items():
                    if rxn.is_exchange:  # ou tambem podes fazer if rxn.is_exchange:
                        rxn.lb = 0

                simulProb = StoicSimulationProblem(newModel, objective={bRXN: 1}, method="pFBA", constraints=medium)
                pfba = simulProb.simulate()

                if pfba.solverStatus == 1:
                    for flux in pfba.get_fluxes_distribution():
                        if(flux.startswith("R_EX_")):
                            if (pfba.get_fluxes_distribution()[flux] < 0):
                                medium_official.append(flux)

                #print(file, medium_official)
                simulProb_opt = StoicSimulationProblem(newModel, objective={bRXN: 1}, method="pFBA", constraints=medium_opt)
                pfba_opt = simulProb_opt.simulate()

                simulProb_exp = StoicSimulationProblem(newModel, objective={bRXN: 1}, method="pFBA", constraints=medium_exp)
                pfba_exp = simulProb_exp.simulate()



#                if pfba.solverStatus == 1:
#                    if pfba_opt.solverStatus == 1:
#                        if pfba_exp.solverStatus == 1:
#                            if(pfba.get_fluxes_distribution()[cs] != 0 and pfba_opt.get_fluxes_distribution()[cs]!=0):
#                                print(file,"\t", pfba.get_fluxes_distribution()[bRXN]/(-10*int(nCarbons[j])), "\t", pfba_opt.get_fluxes_distribution()[bRXN]/(pfba_opt.get_fluxes_distribution()[cs]*int(nCarbons[j])), "\t", cs)

    # ==================== Medium Comparison =============

                #print("Medium ", medium)
                #print("Medium optimized ", medium_opt)

                for mo in medium_opt.keys():
                    comparison.update({mo: 1})
                    for m in medium_official:
                        if m == mo:
                            comparison.update({m : 2})
                for m in medium_official:
                    if m in comparison.keys():
                        comparison.update({m: comparison.get(m)})
                    else:
                        comparison.update({m:0})

                equal = []
                new = []
                original = []

                for k in comparison.keys():
                    if comparison.get(k) == 2:
                        equal.append(k)
                    if comparison.get(k) == 1:
                        new.append(k)
                    if comparison.get(k) == 0:
                        original.append(k)


                #print(file, "\t", comparison, "\t", len(medium_official), "\t", len(medium_opt), "\t", len(equal), "\t", len(new), "\t", len(original), "\t")
                #print(file, "\t", medium_opt.keys())
                #print(file, )
#=====================================================================