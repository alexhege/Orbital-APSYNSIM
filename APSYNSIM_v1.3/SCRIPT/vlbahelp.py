import sys 
import numpy as np


def main():

    ranges = eval(sys.argv[1])
    jdstep = eval(sys.argv[2])
    if len(np.shape(ranges)) == 1:
        JDstart, JDend = ranges
        if ((JDend - JDstart)/jdstep) == int((JDend - JDstart)/jdstep):
            print str(int((ranges[1] - ranges[0])/jdstep)) #to make it exclusive the later time if lines up exactly with step size  
        print str(int((ranges[1] - ranges[0])/jdstep)+1)

    else:
        s = 0
        for r in ranges:
            JDstart, JDend = r
            if ((JDend - JDstart)/jdstep) == int((JDend - JDstart)/jdstep):
                s += int((r[1] - r[0])/jdstep)
            else:
                s+= int((r[1] - r[0])/jdstep)+1

        print str(s)

    return


if __name__ == "__main__":
    main()



