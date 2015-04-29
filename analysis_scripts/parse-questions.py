###
## Counts responses to MC questions, might parse open-ended later.
##
## D.E.Budzitowski 150876
###

import csv, sys, glob
from collections import Counter

def main(argv):
    
    ## No args necessary!

    ## Counter Dict
    mc = { 'q1':Counter(),'q2':Counter(),'q3':Counter(),'q5':Counter(),'q6':Counter(),'q7':Counter(),'q8':Counter() }

    ## First 3x3...
    #path = "./csv/3x3/*"
    path = "./csv/3x3/Pattern-Proj-7APR.csv" # ignore 9APR--incomplete
    for f in glob.glob(path):
        print f
        with open(f) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for col in row:
                    if 'q' in col and 'exp' not in col:
                        sys.stdout.write(row[col] + ' ')
                        mc[col][row[col]] += 1
                print ''

    ## Then 4x4
    path = "./csv/4x4/*"
    for f in glob.glob(path):
        print f
        with open(f) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for col in row:
                    if 'q' in col and 'exp' not in col:
                        sys.stdout.write(row[col] + ' ')
                        mc[col][row[col]] += 1
                print ''

    ## Print Results
    print mc

    
if(__name__ == "__main__"):
   main(sys.argv[1:])
