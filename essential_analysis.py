import os
import csv

basePath = "C:\\Users\\Sophia Santos\\OneDrive - Universidade do Minho\\CEB\\PycharmProjects\\DD_DeCaf\\Tests\\examples\\Results"

def createDict (keys, values):
    return dict(zip(keys, values + [None] * (len(keys) - len(values))))

def countKV(x):
    values = []
    cleanX = []
    total = len(x)
    x_met = sum(x, [])
    #x_met = x.split()
    print(x_met)
    [cleanX.append(j) for j in x_met if j not in cleanX]
    for i in cleanX:
        xi = (x_met.count(i))/total
        values.append(xi)
    return values, cleanX

for file in os.listdir(basePath + "/sophia_models_results"):
    if file.endswith(".txt"):
        FILE = (os.path.join(basePath + "/sophia_models_results", file))
        csvFile = open(FILE, 'r')
        reader = csv.reader(csvFile, delimiter=';')

        model = []
        value = []
        essential = []
        dictEssential = {}

        for row in reader:
            if row[0].endswith(".xml"):
                model.append(row[0])
            if row[0].startswith("Critical"):
                value = countKV(row[0])
                essential.append(row[1])

        #if len(model)==len(essential):
        dictEssential = dict(zip(model,essential))
        #else:
            #print("Model and Essential do not have the same lenght!!")

        print("Models: ", model, "lenght: ", len(model))
        print("Essential: ", essential, "lenght: ", len(essential))
        print("Values: ", value)
        print(dictEssential)