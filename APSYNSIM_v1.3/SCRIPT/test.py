import numpy as np


pfile = open('iner_traj_042616_reconfig_5s.txt')
#63452 times
     

times = []
scpos = []
     
#get into arrays, preprocess strings a bit
for line in pfile.readlines():
  line = line.split(',')
  times.append(line[0])
  line[-1] = line[-1][:-2]
  scpos.append(line[1:])


limit=63452

scpos=scpos[:limit]


#move into np array
nscpos = np.zeros((len(scpos), 93))
for i in range(len(scpos)):
  nscpos[i] = np.array(map(float, scpos[i]))


#reshape array so first indexed by spacecraft
numsc = 31
numbl = numsc*(numsc - 1)/2
length = len(scpos) #number of positions for each s/c
allscpos = np.zeros((numsc, length, 3))
for i in range(numsc):
  allscpos[i] = nscpos[:, i*3:(i+1)*3]


#make new array so first indexed by baseline
baselines = np.zeros((numbl, length, 3))
c=0
for i in range(numsc):
  for j in range(i):
    baselines[c] =  allscpos[i] - allscpos[j]
    c+=1

#update array file
target = open('/home/hegedus/Downloads/APSYNSIM_v1.3/ARRAYS/RelicStart.array', 'w')
target.truncate()
target.write('LATITUDE  90.0 \n')
target.write('DECLINATION  90.0 \n')
target.write('HOUR_ANGLE  -0.0  0.1 \n')

for i in range(numsc):
  target.write('ANTENNA  ' + str(allscpos[i][limit - 1][0]) + '  ' + str(allscpos[i][limit - 1][1]) + '\n')

target.close()	

