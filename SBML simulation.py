from framed import load_cbmodel, pFBA
import os

basePath = "C:/Users/Sophia Santos/Downloads"

for file in os.listdir(basePath):
    if file.startswith("model_"):
        SBML_FILE = (os.path.join(basePath, file))

        print(file)

        model = load_cbmodel(SBML_FILE, flavor="bigg")

        #model.reactions.R_EX_glc__D_e.lb = -10.0
        #model.reactions.R_EX_o2_e.lb = -5.0

        sol = pFBA(model, objective={"R_e_Biomass_C4":1})
        print(sol)