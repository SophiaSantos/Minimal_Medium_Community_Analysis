import os
import csv
import ast

basePath = "C:/Users/Sophia Santos/OneDrive - Universidade do Minho/CEB/PycharmProjects/DD_DeCaF/Tests/examples/Results/anis_model_results"

def addToDict(fileName, dict1, dict2):
    for n in dict1.keys():
        if fileName == n:
            for e in dict1.get(n):
                dict2.update({e: 1.0})

def finalMets (fileName, dict, ar):
    for n in dict.keys():
        if fileName == n:
            for m in dict.get(n):
                ar.append(m)
    return ar

def longest(list1):
    longest_list = max(len(elem) for elem in list1)
    return longest_list

def score(reader):
    score_list = []
    met = []
    for row in reader:
        if row[0] == "242":
            met.append(row[3])
            score_list.append(row[1])
    mscore = max(score_list)
    return mscore, met, score_list

def createDict (keys, values):
    return dict(zip(keys, values + [None] * (len(keys) - len(values))))

def countKV(x):
    values = []
    cleanX = []
    total = len(x)
    x_met = sum(x, [])
    [cleanX.append(j) for j in x_met if j not in cleanX]
    for i in cleanX:
        xi = (x_met.count(i))/total
        values.append(xi)
    return values, cleanX

codes = ["medium_optim_c","_glc.csv"]

modelName_txt=[]
biomassValue=[]
biomassValueDict={}
critical_rxns=[]
essential={}
critical_rxns_ar= []
cRXN = []

count = 0

for file in os.listdir(basePath):
    if file.endswith(".csv"):
        if file.startswith("essential_output"):
            FILE_e = (os.path.join(basePath, file))
            csvFile = open(FILE_e, 'r')
            reader_e = csv.reader(csvFile, delimiter=';')
            next(reader_e, None)  # ignore header

            for row in reader_e:
                modelName_txt.append(row[0])
                #print(modelName_txt)
                crxn = ast.literal_eval(row[1])
                print(crxn)
                critical_rxns.append(crxn)

#print(len(modelName_txt), modelName_txt[31])
#print(len(critical_rxns), critical_rxns[31])


for i in range (0, len(modelName_txt)):
    essential.update({modelName_txt[i]: critical_rxns[i]})

for file in os.listdir(basePath):
    if file.startswith("medium_optim"):
        FILE = (os.path.join(basePath, file))
        file = file[13:len(file)-4] # be careful!!! for single organisms (_glc.csv) change the 4 to 8
        #print(file)
        count += 1
        csvFile = open(FILE, 'r')
        reader = csv.reader(csvFile, delimiter=';')

        score_num = score(reader)
        score_list = score_num[2]
        score_met = score_num[1]

        j = 0
        met = []
        meto2 = []
        meto2_1 = []
        dictList = {}
        dictList_w_o2 = {}
        dictList_wo_o2 = {}
        cleanMet = []

        for i in score_list:
            j += 1
            #if i == score_num[0]:
            if float(i)> 0.7:
                single = (score_num[1])[j - 1]
                single_a = eval(single)
                met.append(single_a)

                #print(countKV(met)[1] + " ; " + countKV(met)[0])

                dictList = createDict(countKV(met)[1], countKV(met)[0])

                addToDict(file, essential, dictList)

                o2 = ['R_EX_M_o2_e_pool', 'R_EX_O2xt_', 'R_EX_O2xt_', 'R_EX_cpd00007_e', 'R_EX_m_o2_']

                for i in o2:
                    if i in dictList.keys():
                        if dictList.get(i) != 1.0:
                            if i in single:
                                single_a = eval(single)
                                meto2.append(single_a)
                                dictList_w_o2 = createDict(countKV(meto2)[1], countKV(meto2)[0])
                                addToDict(file, essential, dictList_w_o2)
                            else:
                                single_a = eval(single)
                                meto2_1.append(single_a)
                                dictList_wo_o2 = createDict(countKV(meto2_1)[1], countKV(meto2_1)[0])
                                addToDict(file, essential, dictList_wo_o2)
        arrayM = met[0]
        fMets = finalMets(file, essential, arrayM)

        #print(file, "; ",fMets, " ; ", len(fMets))
        print(file, "\t ", dictList)
        #print(file, "\t ", dictList, "\t ", dictList_w_o2, "\t", dictList_wo_o2)
        #print("Longest list: " + str((score_num[1])))
        #print("List O2: ", dictListo2)
        #print("List O2: ", dictListo2)

#print(count)