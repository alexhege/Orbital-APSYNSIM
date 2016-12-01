#Alex Hegedus
#This script changes the python and config files to automate generation of 


#!/bin/bash
for imsize in 100 500 1000
do

  sed -i "s/IMSIZE [0-9]*/IMSIZE $imsize/" ../SOURCE_MODELS/DubRadioGauss.model

  #noise gain
  for ng in True False
  do
    
    #thermal noise
    for nt in True False
    do
    
      sed -i "s/NOISY = [a-zA-Z]*/NOISY = $nt/" relicAPSYNSIM.py
      sed -i "s/noisegains = [a-zA-Z]*/noisegains = $ng/" relicAPSYNSIM.py
      

      #wl is in meters
      for wl in 060 030 020 015 010  #120 300
      do
        touch /media/sf_XubuntuShare/RadGal/rmse.dat
        sed -i "s/self.wavelength = .[0-9]* ###/self.wavelength = .$wl ###/" relicAPSYNSIM.py


      #inner older part
      #this updates the how far into time the software should go 
        max=100
        step=3
        for i in `seq 1 $step $max`
        do
          sed -i "s/limit=[0-9]*/limit = $i/" relicinbase.py
          sed -i "s/nH = [0-9]*/nH = $i/" relicAPSYNSIM.config
          python relicAPSYNSIM.py
        done


      #update this to correct path on dsts
        cd /media/sf_XubuntuShare/RadGal

        convert -delay 15 -loop 0 $(for ((a=1; a<= $max; a+= $step)); do printf -- "RadGal_%s.png " $a; done;) animation.gif

        mkdir wl_${wl}_m
        mv *.png *.gif *dat wl_${wl}_m

        cd /home/hegedus/Downloads/APSYNSIM_v1.3/SCRIPT



      done
      
      cd /media/sf_XubuntuShare/RadGal
      mkdir ng_${ng}_nt_${nt}
      mv *_m ng_${ng}_nt_${nt}
      cd /home/hegedus/Downloads/APSYNSIM_v1.3/SCRIPT
      
    done
    
  done
  
  cd /media/sf_XubuntuShare/RadGal
  mkdir ${imsize}_arcsec
  mv ng* ${imsize}_arcsec
  cd /home/hegedus/Downloads/APSYNSIM_v1.3/SCRIPT
  
done  

#$(for ((a=1; a<=$h; a+= 500)); do printf -- "^Cme%s.png " $a; done;)
