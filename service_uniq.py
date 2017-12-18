#i! bin/python

import csv
import getpass
import pickle
import time
import os.path
from collections import Counter

inputFile = open("list.csv", 'r+')
outputFile = open("output.csv", 'wb')
inputReader = csv.reader(inputFile)
inputWriter = csv.writer(inputFile)
outputWriter = csv.writer(outputFile)
next(inputReader, None)
all_specialties = []
for row in inputReader:
    if row[5] == '':
        continue
    # raw_input(all_specialties)
    these_specialties = row[5].split(',')
    for word in these_specialties:
        all_specialties.append(word)

most_common = Counter(all_specialties).most_common()

for item in most_common:
    key = str(item[0])
    value = str(item[1])
    print(key.strip()+' : '+value.strip())

print("Number of non-unique: "+str(len(all_specialties)))
all_specialties = set(all_specialties)
print("Number of unique: "+str(len(all_specialties)))

