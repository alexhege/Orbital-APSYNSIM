import numpy as np
import csv


scpos = []

with open('SunRISE_RelPos_SGEO_20160330_4locs.csv', 'rb') as csvfile:
  screader = csv.reader(csvfile, delimiter=',', quotechar='|')
  i=0
  for row in screader:
    i+=1
    if i > 1 and row[0] != '':
      scpos.append(row)

nscpos = np.zeros((len(scpos), 19))
for i in range(len(scpos)):
  nscpos[i] = np.array(map(float, scpos[i]))

#Don't need center coord for baselines
scpos = nscpos[:,4:]

#Reduce to just 1st part
scpos = scpos[:41]

#apply projection here later?

#extract xyz of each individual sc
numsc = 5
numbl = numsc*(numsc - 1)/2
length = len(scpos)
allscpos = np.zeros((numsc, length, 3))
for i in range(numsc):
  allscpos[i] = scpos[:, i*3:(i+1)*3]


#sc1pos = scpos[:, :3]
#sc2pos = scpos[:, 3:6]
#sc3pos = scpos[:, 6:9]
#sc4pos = scpos[:, 9:12]
#sc5pos = scpos[:, 12:]


#baselines = np.zeros((0, 3))

#for i in range(numsc):
#  for j in range(i):
#    baselines = np.concatenate((baselines, allscpos[i] - allscpos[j]), axis = 0)



baselines = np.zeros((numbl, length, 3))
c=0
for i in range(numsc):
  for j in range(i):
    baselines[c] =  allscpos[i] - allscpos[j]
    c+=1





