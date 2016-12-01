#Alex Hegedus
#This script takes the paramfile and runs APSYNSIM in a black box manner 
#!/bin/bash



paramFile=$1

echoBlackBox=$(cat $paramFile | grep 'echoBlackBox[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
if [ $echoBlackBox == 'True' ]; then
  set -x
fi

APSYNSIMDir=$(cat $paramFile | grep 'APSYNSIMDir[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')

pyFile="${APSYNSIMDir}/SCRIPT/relicAPSYNSIM.py"



#grep floating point numbers with [-+]?[0-9]*\.?[0-9]+\.?

#Gain noise

gNoise=$(cat $paramFile | grep 'gNoise[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
sed -i "s/gainNoise = [a-zA-Z]*/gainNoise = $gNoise/" $pyFile

if [ $gNoise == 'True' ]; then
  gainNoiseRMS=$(cat $paramFile | grep 'gainNoiseRMS[[:space:]]*=' | awk -F = '{print $2}'| cut -d' ' -f 1-) 
  sed -i "s/gainNoiseRMS = (.*)/gainNoiseRMS = $gainNoiseRMS/" $pyFile
fi


#Phase Noise from pos uncertainty
posUncertain=$(cat $paramFile | grep 'posUncertain[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
sed -i "s/posUncertain = [a-zA-Z]*/posUncertain = $posUncertain/" $pyFile
if [ $posUncertain == 'True' ]; then
  posUncert=$(cat $paramFile | grep 'posUncert[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
  sed -i -r "s/posUncert = [-+]?[0-9]*\.?[e]?[+-]?[0-9]+\.?/posUncert = $posUncert/" $pyFile
  clockUncert=$(cat $paramFile | grep 'clockUncert[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
  sed -i -r "s/clockUncert = [-+]?[0-9]*\.?[e]?[+-]?[0-9]+\.?/clockUncert = $clockUncert/" $pyFile
fi



#Thermal Noise
tNoise=$(cat $paramFile | grep 'tNoise[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
sed -i "s/thermalNoise = [a-zA-Z]*/thermalNoise = $tNoise/" $pyFile

if [ $tNoise == 'True' ]; then
  thermalNoise=$(cat $paramFile | grep 'thermalNoise[[:space:]]=' | awk -F = '{print $2}'|awk '{print $1}')
  if [ $thermalNoise != 'galactic' ]; then
    sed -i "s/customNoise = [a-zA-Z]*/customNoise = True/" $pyFile
    sed -i -r "s/customRMS = [-+]?[0-9]*\.?[e]?[+-]?[0-9]+\.?/customRMS = $thermalNoise/" $pyFile   
  else 
    sed -i "s/customNoise = [a-zA-Z]*/customNoise = False/" $pyFile 
  fi
fi
  
step=$(cat $paramFile | grep 'step[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
sed -i -r "s/stepSize = [0-9]+ ###/stepSize = $step ###/" $pyFile

intTime=$(cat $paramFile | grep 'intTime[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
sed -i -r "s/intTime = [-+]?[0-9]*\.?[e]?[+-]?[0-9]+\.?/intTime = $intTime/" $pyFile

bandwidth=$(cat $paramFile | grep 'bandwidth[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
sed -i -r "s/bandwidth = [-+]?[0-9]*\.?[e]?[+-]?[0-9]+\.?/bandwidth = $bandwidth/" $pyFile


  
#longest bl
largestbl=$(cat $paramFile | grep 'largestbl[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
sed -i -r "s/self.largestbl = [-+]?[0-9]*\.?[0-9]+\.?/self.largestbl = $largestbl/" $pyFile
  
#autoquit
autoQuit=$(cat $paramFile | grep 'autoQuit[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
sed -i "s/autoQuit = [a-zA-Z]*/autoQuit = $autoQuit/" $pyFile

#savefig
saveFig=$(cat $paramFile | grep 'saveFig[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
sed -i "s/saveFig = [a-zA-Z]*/saveFig = $saveFig/" $pyFile
  
#figName
figName=$(cat $paramFile | grep 'figName[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
sed -i "s|baseFigName = '.*'|baseFigName = '$figName'|" $pyFile

#saveRMSE
saveRMSE=$(cat $paramFile | grep 'saveRMSE[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
sed -i "s/saveRMSE = [a-zA-Z]*/saveRMSE = $saveRMSE/" $pyFile

#RMSEFile
RMSEFile=$(cat $paramFile | grep 'RMSEFile[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
sed -i "s|RMSEFile = '.*'|RMSEFile = '$RMSEFile'|" $pyFile


#create model file
imSize=$(cat $paramFile | grep 'imSize[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
wavelength=$(cat $paramFile | grep 'wavelength[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
imageName=$(cat $paramFile | grep 'imageName[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
brightestPix=$(cat $paramFile | grep 'brightestPix[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')

modelFile="${APSYNSIMDir}/SOURCE_MODELS/BBParam.model"
echo "IMSIZE $imSize" > $modelFile
echo "WAVELENGTH $wavelength" >> $modelFile
echo "IMAGE $imageName $brightestPix" >> $modelFile

#Change .config values
configFile="${APSYNSIMDir}/SCRIPT/relicAPSYNSIM.config"
Npix=$(cat $paramFile | grep 'Npix[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
sed -i "s/Npix = [0-9]*/Npix = $Npix/" $configFile


#Change inbase stuff
inbaseFile="${APSYNSIMDir}/SCRIPT/relicinbase.py"
ranges=$(cat $paramFile | grep 'ranges[[:space:]]*=' | awk -F = '{print $2}'| grep '(*)')
sed -i "s/ranges =.*)/ranges = $ranges/" $inbaseFile


ra=$(cat $paramFile | grep 'ra[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
dec=$(cat $paramFile | grep 'dec[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
orbitFile=$(cat $paramFile | grep 'orbitFile[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
numsc=$(cat $paramFile | grep 'numsc[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
diameter=$(cat $paramFile | grep 'diameter[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
lowerLimit=$(cat $paramFile | grep 'lowerLimit[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')


sed -i "s/ra = '.*'/ra = $ra/" $inbaseFile
sed -i "s/dec = '.*'/dec = $dec/" $inbaseFile
sed -i "s/numsc = [0-9]*/numsc = $numsc/" $inbaseFile
sed -i "s|orbitFile = '.*'|orbitFile = '$orbitFile'|" $inbaseFile
sed -i -r "s/diameter = [-+]?[0-9]*\.?[0-9]+\.?/diameter = $diameter/" $inbaseFile
sed -i "s/lowerLimit = [0-9]*/lowerLimit = $lowerLimit/" $inbaseFile





#Gif stuff and running code
makegif=$(cat $paramFile | grep 'makegif[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')

if [ $makegif == 'False' ]; then
  sed -i "s/gifName = [a-zA-Z]*/gifName = False/" $pyFile
  sed -i "s/gifMode = [a-zA-Z]*/gifMode = False/" $pyFile
  python $pyFile
  
  
  
  
#Gif Mode!!! 
else
  #gets total number of samples from sum of subintervals
  tot=$(python pHelp.py "$ranges") 
  

  #Turn on autoquit and special naming, savefig, and savermse
  sed -i "s/saveFig = [a-zA-Z]*/saveFig = True/" $pyFile
  sed -i "s/autoQuit = [a-zA-Z]*/autoQuit = True/" $pyFile
  sed -i "s/gifName = [a-zA-Z]*/gifName = True/" $pyFile
  sed -i "s/saveRMSE = [a-zA-Z]*/saveRMSE = True/" $pyFile
  #step=$(cat $paramFile | grep 'step[[:space:]]*=' | awk -F = '{print $2}'|awk '{print $1}')
  
  sed -i "s/gifMode = [a-zA-Z]*/gifMode = True/" $pyFile
  python $pyFile
  
  #for i in `seq 1 $step $tot`
  #do
  #  sed -i -r "s/limit = [-+]?[0-9]*/limit = $i/" $inbaseFile
  #  python $pyFile
    #rootName=$(echo $figName | awk -F . '{print $1}')
    #gifName=$(printf "%s_%s.png " $rootName $i)
    
    #convert $gifName -crop 250x250+898+345 $gifName
  #done
  
  
  #sed -i -r "s/limit = [-+]?[0-9]*/limit = -1/" $inbaseFile


  rootName=$(echo $figName | awk -F . '{print $1}')

  convert -delay 15 -loop 0 $(for ((a=$step; a<= $tot; a+= $step)); do printf -- "%s_%s.png " $rootName $a; done;) ${rootName}.gif
fi
