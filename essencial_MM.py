#=============== Medium Optimization for files in directory =====================#
from framed import load_cbmodel
from optimModels.simulation.simul_problems import StoicSimulationProblem
from optimModels.utils.configurations import StoicConfigurations
from optimModels.utils.utils import fix_exchange_reactions_model
import os
import csv

basePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DeCaF/Tests/examples/mpa2018/"


list_models = []
model_name=[]
biomass_rxn=[]
carbon_source=[]

for file in os.listdir(basePath):
    if file.endswith(".xml"):
        SBML_FILE = (os.path.join(basePath, file))
        Id = file
        print(Id)
        model = load_cbmodel(SBML_FILE, exchange_detection_mode='unbalanced')
        newModel = fix_exchange_reactions_model(model)
        list_models.append(newModel)

print(list_models)

for file in os.listdir(basePath):
    if file.endswith(".csv"):
        FILE = (os.path.join(basePath, file))
        csvFile = open(FILE, 'r')
        reader = csv.reader(csvFile, delimiter=';')
        next(reader, None) #ignore header

        for row in reader:
            model_name.append(row[0])
            biomass_rxn.append(row[1])
            carbon_source.append(row[2])

print("Model name: " + str(model_name) + "; Biomass: " + str(biomass_rxn) + "; Carbon_source: " + str(carbon_source))
