import csv
import os

from framed import load_cbmodel, save_cbmodel, Environment, pFBA
from framed.community.model import Community
from optimModels.utils.utils import fix_exchange_reactions_model

community_name = []
organism_list = []
o = []

basePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DeCaF/Tests/examples/models/nitro"
savePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DeCaF/Tests/examples/models/mpa2019/community_models"

list_models = []

for file in os.listdir(basePath):
    if file.endswith(".xml"):
        SBML_FILE = (os.path.join(basePath, file))
        Id = file
        model = load_cbmodel(SBML_FILE, exchange_detection_mode='unbalanced')
        newModel = fix_exchange_reactions_model(model)
        newModel.biomass_reaction = "R_BIOMASS"
        list_models.append(newModel)

for file in os.listdir(savePath):
    if file.endswith(".csv"):
        FILE = (os.path.join(savePath, file))
        csvFile = open(FILE, 'r')
        reader = csv.reader(csvFile, delimiter=';')
        next(reader, None) #ignore header

        for row in reader:
            community_name.append(row[0])
            organism_list.append(row[1])

for i in range(0,len(community_name)):
    org = organism_list[i]
    x_mod = org.split()
    models = []

    for m in list_models:
        for o in x_mod:
            if(str(m.id) == str(o.replace(',', ''))):
                models.append(m)

    #print(community_name[i])
    #for t in range(0, len(models)):
        #print(str(models[t].id))

    community = Community(community_name[i], models = models, extracellular_compartment_id = 'e', interacting = True)
    merged = community.merged
    Environment.complete(merged, inplace=True)

    print(merged.id)
    newCommModel = fix_exchange_reactions_model(merged)


    save_cbmodel(newCommModel, savePath + '/community_' + community_name[i] + ".xml", flavor='fbc2')

    #sol = pFBA(newCommModel)
    #org_fluxes = community.split_fluxes(sol.values)

    print("Community name: " + community_name[i] + " Community id: " + newCommModel.id)

    # for x in list_models:
    # name = x.id
    # if name in community.organisms:
    # print("Solution of organism " + name + " : " + sol.show_values(pattern="_e_" + name, sort=True))

