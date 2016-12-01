import sys 
import numpy as np


def main():

    ranges = eval(sys.argv[1])
    jdstep = eval(sys.argv[2])
    if len(np.shape(ranges)) == 1:
        print str(int((ranges[1] - ranges[0])/jdstep)+1)

    else:
      s = 0
      for r in ranges:
          s+= r[1] - r[0]

      print str(int(s/jdstep)+1)

    return


if __name__ == "__main__":
    main()



