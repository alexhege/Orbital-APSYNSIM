#Alex Hegedus
#This script changes the python and config files to automate generation of 


#!/bin/bash

#wl is in meters
for wl in 060 030 020 015 010  #120 300
do
  sed -i "s/self.wavelength = .[0-9]* ###/self.wavelength = .$wl ###/" relicAPSYNSIM.py


#inner older part
#this updates the how far into time the software should go 
  max=301
  step=3
  for i in `seq 1 $step $max`
  do
    sed -i "s/limit=[0-9]*/limit=$i/" relicinbase.py
    sed -i "s/nH = [0-9]*/nH = $i/" relicAPSYNSIM.config
    python relicAPSYNSIM.py
  done


#update this to correct path on dsts
  cd /media/sf_XubuntuShare/RadGal

  convert -delay 15 -loop 0 $(for ((a=1; a<= $max; a+= $step)); do printf -- "RadGal_%s.png " $a; done;) animation.gif

  mkdir wl_${wl}_m
  mv *.png *.gif wl_${wl}_m

  cd /home/hegedus/Downloads/APSYNSIM_v1.3/SCRIPT



done

#$(for ((a=1; a<=$h; a+= 500)); do printf -- "^Cme%s.png " $a; done;)
