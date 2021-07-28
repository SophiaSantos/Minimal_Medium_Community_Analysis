import csv
import os
import ast

basePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DeCaF/Tests/examples/Results"

def createDict (keys, values):
    return dict(zip(keys, values + [None] * (len(keys) - len(values))))

modelName_txt=[]
modelName_csv=[]
critical_rxns=[]
rxns=[]

essential = {}
newRxn = {}
Full_list = {}

for file in os.listdir(basePath + "/joana_models_results"):
    if file.endswith(".txt"):
        if file.startswith("essential"):
            FILE_e = (os.path.join(basePath + "/joana_models_results", file))
            txtFile_e = open(FILE_e, 'r')
            reader_e = txtFile_e.readlines()
            for line_e in reader_e:
                if line_e.startswith("i"):
                    name_e = line_e.replace(";", "")
                    modelName_txt.append(str(name_e.replace("\n", "")))
                if line_e.startswith("Critical"):
                    critical = ast.literal_eval(line_e[9:len(line_e)])
                    critical_rxns.append(critical)

            for i in range(0, len(modelName_txt)):
                essential.update({modelName_txt[i]: critical_rxns[i]})

    if file.endswith(".csv"):
        if file.startswith("medium_analysis"):
            FILE = (os.path.join(basePath + "/joana_models_results", file))
            csvFile = open(FILE, 'r')
            reader_csv = csv.reader(csvFile, delimiter=';')
            next(reader_csv, None)  # ignore header

            for row in reader_csv:
                modelName_csv.append(row[0])

        for j in range (0, len(modelName_csv)):
            name = modelName_csv[j]

            #newRxn.update({modelName_csv[j], rxns[j]})


#print("Essential: " + str(essential))
print("Models: " + str(modelName_csv))
print("Rxns: " + str(rxns))
