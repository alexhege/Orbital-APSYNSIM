import numpy as np

import datetime
import ephem 


ov = ephem.Observer()
#ov.date = ephem.now()
#ov.date = datetime.datetime.utcnow() + datetime.timedelta(hours=9) #for future
ov.date =  datetime.datetime(2016, 5, 12, 14, 0, 0)

#For Cyg A
ra = '19:59:28.3566'
dec = '40:44:02.096'

h, m, s = map(float, ra.split(':'))
raf = 15*h + m / 60. + s / 3600.
ra = raf*np.pi/180.0

h, m, s = map(float, dec.split(':'))
if h < 0. or dec.split(':')[0][:2] == '-0':
  m = -m
  s = -s


decf = h + m / 60. + s / 3600.
dec = decf*np.pi/180.0

#unit direction pointing in direction of source
x = np.cos(dec) * np.cos(ra)
y = np.cos(dec) * np.sin(ra)
z = np.sin(dec)
s = [x, y, z]


#get x and y axes perp to s
x = np.cross(s, [0, 1, 0])
y = np.cross(s, x)

#normalize since cross product isn't already 1 for some reason
x = x/np.linalg.norm(x)
y = y/np.linalg.norm(y)

###

#pfile = open('iner_traj_042616_reconfig_5s.txt')
#63452 times, 5 seconds each

orbitFile = '/home/hegedus/Downloads/APSYNSIM_v1.3/SCRIPT/inert_traj_061216_reconfig.txt'

pfile = open(orbitFile)
#77200 times, 1 min each
     

times = []
scpos = []
     
#get into arrays, preprocess strings a bit
for line in pfile.readlines():
  line = line.split(',')
  times.append(line[0])
  line[-1] = line[-1][:-2]
  scpos.append(line[1:])


numsc = np.shape(scpos)[1]/3

#what the sed script looks to change to modify integration time, and time intervals used
ranges =  ((0, 1))
snips = []
timesnips = []

if len(np.shape(ranges)) == 1:
  snips += scpos[ranges[0]:ranges[1]]
  timesnips += times[ranges[0]:ranges[1]] 
else:
  for r in ranges:
    snips += scpos[r[0]:r[1]]
    timesnips += times[r[0]:r[1]]
    
scpos = snips
times = timesnips



#move into np array, convert from strings to float with map
numbl = numsc*(numsc - 1)/2
nscpos = np.zeros((len(scpos), numsc*3))
for i in range(len(scpos)):
  nscpos[i] = np.array(map(float, scpos[i]))


#reshape array so first indexed by spacecraft

length = len(scpos) #number of positions for each s/c
allscpos = np.zeros((numsc, length, 3))
for i in range(numsc):
  allscpos[i] = nscpos[:, i*3:(i+1)*3]


#Change projection
#allscpos[:, :, 1] = allscpos[:, :, 2]




#make new array so first indexed by baseline
#baselines = np.zeros((numbl, length, 2))
#c=0
#for i in range(numsc):
#  for j in range(i):
#    baselines[c] =  projpos[i] - projpos[j]
#    c+=1


#make new array so first indexed by baseline
baselines = np.zeros((numbl, length, 3))
c=0
for i in range(numsc):
  for j in range(i):
    baselines[c] =  allscpos[i] - allscpos[j]
    c+=1


#project baselines only, not positions 
projpos = np.zeros((numbl, length, 2))

for i in range(numbl):
  for j in range(length):
    projpos[i][j][0] = np.dot(baselines[i][j][:], x) 
    projpos[i][j][1] = np.dot(baselines[i][j][:], y)

baselines = projpos.copy()

#Now compute proj pos for antenna stuff 
projpos = np.zeros((numsc, length, 2))

for i in range(numsc):
  for j in range(length):
    projpos[i][j][0] = np.dot(allscpos[i][j][:], x) 
    projpos[i][j][1] = np.dot(allscpos[i][j][:], y)


largestbl = np.amax(abs(baselines))


#update array file

diameter = 0.5

import os
d1 = os.path.dirname(os.path.realpath(__file__))
arraydir  = os.path.join(d1,'..','ARRAYS')
antenna_file = os.path.join(arraydir,'RelicStart.array')

target = open(antenna_file, 'w')
target.truncate()
target.write('LATITUDE  90.0 \n')
target.write('DECLINATION  90.0 \n')
target.write('HOUR_ANGLE  -0.0  0.1 \n')
target.write('DIAMETER  ' + str(diameter) + ' \n')

for i in range(numsc):
  target.write('ANTENNA  ' + str(projpos[i][-1][0]) + '  ' + str(projpos[i][-1][1]) + '\n')


target.close()	



minutesRev = 530. #minutes to do revolution within orbit

angFreq = 2*np.pi/minutesRev/60. #radians per second 1.976e-4


timeAvgLossScale = 10./600000./angFreq *.1 # 8.43 ms to avoid smearing at highest freq 30MHz


trackingRate = 32000*600000/(3e8)*angFreq # .01264 s 

























