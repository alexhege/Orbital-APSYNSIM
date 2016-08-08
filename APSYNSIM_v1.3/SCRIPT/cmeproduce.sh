#Alex Hegedus
#This script changes the python and config files to automate generation of 


#!/bin/bash

#wl is in meters
for wl in 005 #120 300
do
  #sed -i "s/self.wavelength = .[0-9]* ###/self.wavelength = .$wl ###/" sunAPSYNSIM.py


#inner older part
#this updates the how far into time the software should go 
  max=41
  for i in `seq 1 10 $max`
  do
    sed -i "s/limit=[0-9]*/limit=$i/" suninbase.py
    sed -i "s/nH = [0-9]*/nH = $i/" sunAPSYNSIM.config
    python sunAPSYNSIM.py
  done


#update this to correct path on dsts
  cd /media/sf_XubuntuShare/cmeTEST

  convert -delay 15 -loop 0 $(for ((a=1; a<= $max; a+= 10)); do printf -- "CME_%s.png " $a; done;) animation.gif

  #mkdir wl_${wl}_m
  #mv *.png *.gif wl_${wl}_m

  cd /home/hegedus/Downloads/APSYNSIM_v1.3/SCRIPT



done

#$(for ((a=1; a<=$h; a+= 500)); do printf -- "^Cme%s.png " $a; done;)
