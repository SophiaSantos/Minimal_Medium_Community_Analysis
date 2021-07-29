import os

from framed import load_cbmodel, save_cbmodel

from optimModels.utils.utils import fix_exchange_reactions_model

basePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DD_DeCaF/Tests/examples/models/nitro"

for file in os.listdir(basePath):
    if file.endswith("_smetana.xml"):
        SBML_FILE = (os.path.join(basePath, file))
        Id = file
        print(Id)
        model = load_cbmodel(SBML_FILE, exchange_detection_mode='R_EX_')
        newModel = fix_exchange_reactions_model(model)
        newModel.biomass_reaction = "R_e_Biomass__cytop"
        newID = basePath + "/" + Id + "_fbc2.xml"
        print(newID)
        save_cbmodel(newModel, newID, flavor='fbc2')
