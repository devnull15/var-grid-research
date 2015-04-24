###
## records the data stored in a list of Pattern objects to a csv file
###

import os, csv, sys
from pattern import Pattern

def record_CSV(fn, patterns):

    ## Open File
    rootPath = "./analysis/"
    rootPath += os.path.basename(os.path.dirname(fn)) + '/'
    rootPath += os.path.splitext(os.path.basename(fn))[0]
    csvfile = open(rootPath + '/analysis.csv', 'w+')

    ## Set up headers
    fieldnames = ['type','pattern','compromised','recall','symmetryH','symmetryV','length','start','end','stroke','direction','image']
    analysisWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    analysisWriter.writeheader()

    ## write the rows!
    for p in patterns:
        analysisWriter.writerow(p.writerow())

def main(argv):
    record_CSV('/foo/bar/Pattern-Proj-7APR.csv', [])


if(__name__ == "__main__"):    
   main(sys.argv[1:])
