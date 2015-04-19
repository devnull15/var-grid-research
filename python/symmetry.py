###
## Computes the horiztonal and vertical symmetry of a pattern of a specified size
##
## D.E. Budzitowski 150876
###

import math

def horiz_symmetry(size,pattern):
    ##NOTE: Number of axises = size + size - 3

    maxSym = 0

    ##first go until the middle axis
    middle = int(math.ceil(float(size)/2.0))
    for i in xrange(0,middle):
        ##for each line of symmetry, we must check size*row nodes
        # until we hit the middle axis
        print i
