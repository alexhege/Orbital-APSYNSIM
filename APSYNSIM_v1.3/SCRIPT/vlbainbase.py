import numpy as np

import datetime
import ephem 
from ECEF2ECI import *


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


#       Using the numbers from the VLBA experiment VEX file, DSN numbers from itrf2008.XYZ
#       the VLBA numbers in itrf2008 agreed very well with their numbers in VEX file
ANT=dict()
#            ant  elev(m)  long(west, neg)     lat(north)            X(m)            Y(m)        Z(m)
ANT['14'] = ['14',1002.11,'243:06:37.67 '  ,'35:25:33.24518 ',-2353621.437 ,-4641341.473  , 3677052.268  ]
ANT['13'] = ['13',1071.18,'243:12:19.955'  ,'35:14:49.79342 ',-2351112.660 ,-4655530.657  , 3660912.693  ]
ANT['sc'] = ['sc',  -15.01,'064:35:01'     ,'17:45:23.7'    , 2607848.54310,-5488069.65740, 1932739.57020]
ANT['hn'] = ['hn', -295.56,'071:59:11'     ,'42:56:01.0'    , 1446375.06850,-4447939.65720, 4322306.12670]
ANT['nl'] = ['nl',  222.26,'091:34:26'     ,'41:46:17.1'    , -130872.29900,-4762317.11090, 4226851.02680]
ANT['fd'] = ['fd', 1606.42,'103:56:41'     ,'30:38:06.1'    ,-1324009.16220,-5332181.96000, 3231962.45080]
ANT['la'] = ['la', 1962.43,'106:14:44'     ,'35:46:30.4'    ,-1449752.39880,-4975298.58190, 3709123.90440]
ANT['pt'] = ['pt', 2364.67,'108:07:09'     ,'34:18:03.7'    ,-1640953.75070,-5014816.02080, 3575411.85810]
ANT['kp'] = ['kp', 1901.99,'111:36:44'     ,'31:57:22.7'    ,-1995678.66400,-5037317.70640, 3357328.10270]
ANT['ov'] = ['ov', 1196.31,'118:16:37'     ,'37:13:53.9'    ,-2409150.16290,-4478573.20450, 3838617.37970]
ANT['br'] = ['br',  250.49,'119:40:59'     ,'48:07:52.4'    ,-2112065.01550,-3705356.51070, 4726813.76690]
ANT['mk'] = ['mk', 3763.04,'155:27:19'     ,'19:48:05.0'    ,-5464075.00190,-2495248.92910, 2148296.94170]


scposECEF = np.array([[-2353621.437 ,-4641341.473  , 3677052.268  ], [-2351112.660 ,-4655530.657  , 3660912.693  ], [2607848.54310,-5488069.65740, 1932739.57020], \
	[1446375.06850,-4447939.65720, 4322306.12670], [1446375.06850,-4447939.65720, 4322306.12670], [-1324009.16220,-5332181.96000, 3231962.45080], \
	[-1449752.39880,-4975298.58190, 3709123.90440], [-1640953.75070,-5014816.02080, 3575411.85810], [-1995678.66400,-5037317.70640, 3357328.10270], \
	[-2409150.16290,-4478573.20450, 3838617.37970], [-2112065.01550,-3705356.51070, 4726813.76690], [-5464075.00190,-2495248.92910, 2148296.94170]])*.001

#turn to 3xN array
scposECEF =scposECEF.T


JDranges =  ((2457690.5, 2457690.51))
JDstep = .01

timesnips = []

if len(np.shape(JDranges)) == 1:
  JDstart, JDend = JDranges
  assert JDend > JDstart, "error, JDend = %f before JDstart = %f" % (JDend, JDstart)
  numJD = int((JDend - JDstart)/JDstep)+1
  if ((JDend - JDstart)/JDstep) == int((JDend - JDstart)/JDstep):
    numJD = numJD - 1 #to make it exclusive the later time if lines up exactly with step size  
    
  timesnips += np.linspace(JDstart, JDend, numJD).tolist()
else:
  for r in JDranges:
    JDstart, JDend = r
    assert JDend > JDstart, "error, JDend = %f before JDstart = %f" % (JDend, JDstart)
    numJD = int((JDend - JDstart)/JDstep)+1
    if ((JDend - JDstart)/JDstep) == int((JDend - JDstart)/JDstep):
      numJD = numJD - 1 #to make it exclusive the later time if lines up exactly with step size  
    timesnips += np.linspace(JDstart, JDend, numJD).tolist()
    
times = timesnips



scpos = []

for jd in times:
  eci_r = ECEF2ECI(jd*ones(12), scposECEF) #return 3xN
  scpos.append(eci_r.T.flatten().tolist()) #feed as x1y1z1x2y2z2 etc


nscpos = np.array(scpos)

numsc = np.shape(scpos)[1]/3

numbl = numsc*(numsc - 1)/2


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

diameter = 25.

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

























