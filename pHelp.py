import sys 
import numpy as np


def main():

    ranges = eval(sys.argv[1])
    if len(np.shape(ranges)) == 1:
        print str(ranges[1] - ranges[0])

    else:
      s = 0
      for r in ranges:
          s+= r[1] - r[0]

      print str(s)

    return


if __name__ == "__main__":
    main()



