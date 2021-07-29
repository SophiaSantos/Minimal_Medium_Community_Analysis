import os
import numpy as np
import csv

basePath = "C:/Users/Sophia Santos/Desktop/sophia_organisms"

count = 0
n = 0
full_list = {}

for file in os.listdir(basePath):
    if file.endswith(".txt"):
        org_list = []

        FILE = (os.path.join(basePath, file))
        print(file)
        org_list.append(file)
        csvFile = open(FILE, 'r')

        reader = csv.reader(csvFile, delimiter=';')

        for row in reader:
            org_list.append(row)
    full_list.update({file: org_list})

    print(full_list)


np.savetxt("file_name.csv", full_list, delimiter=";", fmt='%s')

