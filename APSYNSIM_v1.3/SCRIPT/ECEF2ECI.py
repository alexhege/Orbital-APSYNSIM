#Alex Hegedus porting from 
#https://www.mathworks.com/matlabcentral/fileexchange/28234-convert-ecef-to-eci-coordinates
#by Darin Koblick

from pylab import *

#mean siderial time in degrees
def JD2GMST(JD):
    
    #Find the Julian Date of the previous midnight, JD0
    JD0 = zeros(size(JD))
    JDmin = floor(JD)-.5
    JDmax = floor(JD)+.5
    JD0[where(JD > JDmin)[0]] = JDmin[where(JD > JDmin)[0]]
    JD0[where(JD > JDmax)[0]] = JDmax[where(JD > JDmax)[0]]
    H = (JD-JD0)*24       #Time in hours past previous midnight
    D = JD - 2451545.0     #Compute the number of days since J2000
    D0 = JD0 - 2451545.0   #Compute the number of days since J2000
    T = D/36525.          #Compute the number of centuries since J2000
    #Calculate GMST in hours (0h to 24h) ... then convert to degrees
    GMST = mod(6.697374558 + 0.06570982441908*D0  + 1.00273790935*H + \
        0.000026*(T**2),24.)*15.
        
    return GMST
    
    
    
#Convert a specified Julian Date Vector to Greenwhich Apparent Sidereal Time in degrees.
def JD2GAST(JD):
    
    THETAm = JD2GMST(JD)
    
    T = (JD - 2451545.0)/36525.
    
    #Mean obliquity of the ecliptic (EPSILONm)
    # see http://www.cdeagle.com/ccnum/pdf/demogast.pdf equation 3
    EPSILONm = 84381448-46.8150*T - .00059*(T**2) + .001813*(T**3)
    
    #Nutations in obliquity and longitude (degrees)
    # see http://www.cdeagle.com/ccnum/pdf/demogast.pdf equation 4
    L = 280.4665 + 36000.7698*T
    dL = 218.3165 + 481267.8813*T
    OMEGA = 125.04452 - 1934.136261*T
    
    #Calculate nutations using the following two equations:
    # see http://www.cdeagle.com/ccnum/pdf/demogast.pdf equation 5
    dPSI = -17.20*sin(OMEGA*pi/180.) - 1.32*sin(2.*L*pi/180.) - .23*sin(2.*dL*pi/180.) \
        + .21*sin(2.*OMEGA*pi/180.)
    dEPSILON = 9.20*cos(OMEGA*pi/180.) + .57*cos(2.*L*pi/180.) + .10*cos(2.*dL*pi/180.) - \
        .09*cos(2.*OMEGA*pi/180.)
        
        
    #Convert the units from arc-seconds to degrees
    dPSI = dPSI*(1/3600)
    dEPSILON = dEPSILON*(1/3600.)
    
    #(GAST) Greenwhich apparent sidereal time expression in degrees
    # see http://www.cdeagle.com/ccnum/pdf/demogast.pdf equation 1
    GAST = mod(THETAm + dPSI*cos((EPSILONm+dEPSILON)*pi/180.),360.)
    
    return GAST
    
#needs JD in a numpy array 1xN
#r_ECEF is in numpy array 3xN
def ECEF2ECI(JD, r_ECEF):
    
    #Calculate the Greenwich Apparent Sideral Time (THETA) equation 27
    THETA = JD2GAST(JD)
    
    
    #Average inertial rotation rate of the earth radians per second
    omega_e = 7.29211585275553e-005
    
    #Assemble the transformation matricies to go from ECEF to ECI
    #See http://www.cdeagle.com/omnum/pdf/csystems.pdf equation 26
    n = shape(r_ECEF)[1]
    r_ECI = zeros([3, n])
    
    for i in range(n):
        t = THETA[i]
        rotMatrix = matrix([[cos(t*pi/180.), -sin(t*pi/180.), 0], \
                           [sin(t*pi/180.), cos(t*pi/180.), 0], \
                           [0, 0, 1.]])
        r_ECI[:, i] = (rotMatrix*(matrix(r_ECEF[:, i]).T)).flatten() 
        
    return r_ECI
    
        
