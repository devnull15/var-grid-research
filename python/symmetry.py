###
## Computes the horiztonal and vertical symmetry of a pattern of a specified size
##
## D.E. Budzitowski 150876
###

import math


###!!NOTE!! Functions are redundant--could encapsulate everything past the pair determination into a helper function###

def vert_symmetry(size,key_pattern):

    ## Check for invalid pattern
    if key_pattern[1].pattern is 'X':
        return 0

    ##NOTE: Number of axises = size + size - 3

    ##Variables##
    partNum = key_pattern[0].split("-")[0] #participant number
    pattNum = key_pattern[0].split("-")[1] #pattern number
    patternList = key_pattern[1].pattern.split('.')
    maxSym = 0
    length = len(patternList)
    #probably a way to figure this out programmatically...
    threepairs = {0:{0:1,3:4,6:7},1:{0:2,3:5,6:8},2:{1:2,4:5,7:8}}
    fourpairs = {0:{0:1,4:5,8:9,12:13},1:{0:2,4:6,8:10,12:14},2:{0:3,4:7,8:11,12:15,1:2,5:6,9:10,13:14},3:{1:3,5:7,9:11,13:15},4:{2:3,6:7,10:11,14:15}}

    #DEBUGGING
    #print "Testing Particpant " + partNum + "'s Pattern " + pattNum + " for symmetry:"


    ##Determine pair map to use based on size
    if size is 3:
        pairs = threepairs
    elif size is 4:
        pairs = fourpairs
    else:
        exit("symmetry.py: size not supported!")

    ##for each line of symmetry, check to see if any of the point-pairs are symmetric...
    for i in xrange(0,size*2-3):
        symCount = 0
        pairCount = 0

        #DEBUGGING
        #print "*line of symmetry " + str(i) + ": "

        ## For each point, see if the symmetric point is also in the pattern
        for point in patternList:
            if pairs[i].has_key(int(point)):
                #count the symmetric pairs...
                if str(pairs[i][int(point)]) in patternList:
                    #DEBUGGING
                    #print "**symmetry found! "
                    symCount = symCount + 1
                pairCount += 1
                   

        ## After looking at all points, see if
        # this LOS had the greatest symmetry
        try:
            symmetry = float(symCount)/float(pairCount)
        except:
            symmetry = 0

        if symmetry > maxSym:
            ## Symmetry = symmetric pairs / all possible pairs
            #  if no pairs then symmetry = 0
            maxSym = symmetry

    return maxSym


def horiz_symmetry(size,key_pattern):

    ## Check for invalid pattern
    if key_pattern[1].pattern is 'X':
        return 0

    ##NOTE: Number of axises = size + size - 3

    ##Variables##
    partNum = key_pattern[0].split("-")[0] #participant number
    pattNum = key_pattern[0].split("-")[1] #pattern number
    patternList = key_pattern[1].pattern.split('.')
    maxSym = 0
    length = len(patternList)
    #probably a way to figure this out programmatically...
    threepairs = {0:{0:3,1:4,2:5},1:{0:6,1:7,2:8},2:{3:6,4:7,5:8}}
    fourpairs = {0:{0:4,1:5,2:6,3:7},1:{0:8,1:9,2:10,3:11},2:{0:12,1:13,2:14,3:15,4:8,5:9,6:10,7:11},3:{4:12,5:13,6:14,7:15},4:{8:12,9:13,10:14,11:15}}

    #DEBUGGING
    #print "Testing Particpant " + partNum + "'s Pattern " + pattNum + " for symmetry:"


    ##Determine pair map to use based on size
    if size is 3:
        pairs = threepairs
    elif size is 4:
        pairs = fourpairs
    else:
        exit("symmetry.py: size not supported!")

    ##for each line of symmetry, check to see if any of the point-pairs are symmetric...
    for i in xrange(0,size*2-3):
        symCount = 0
        pairCount = 0

        #DEBUGGING
        #print "*line of symmetry " + str(i) + ": "


        ## For each point, see if the symmetric point is also in the pattern
        for point in patternList:
            if pairs[i].has_key(int(point)):
                #count the symmetric pairs...
                if str(pairs[i][int(point)]) in patternList:
                    #DEBUGGING
                    #print "**symmetry found! "
                    symCount = symCount + 1
                pairCount += 1
                   

        ## After looking at all points, see if
        # this LOS had the greatest symmetry
        try:
            symmetry = float(symCount)/float(pairCount)
        except:
            symmetry = 0

        if symmetry > maxSym:
            ## Symmetry = symmetric pairs / all possible pairs
            #  if no pairs then symmetry = 0
            maxSym = symmetry

    return maxSym
