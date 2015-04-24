###
## Reads a pattern csv file and returns the most common grid passwords
##
## D.E. Budzitowski 150876
###

import sys,csv,collections,Image


def main(argv):
        
    ## Error Check
    if len(argv) is not 1 or (int(argv[0]) is not 3 and int(argv[0]) is not 4):
        exit("incorrect args")

    ## Path to file
    s = str(argv[0]) + 'x' + str(argv[0])
    rootPath = "./analysis/" + s + "/"
    path = rootPath + s + "_data.csv"

    ## Open csv
    file = open(path)
    reader = csv.DictReader(file)
    
    pattern_image = {}
    patternList = []
    for row in reader:
        if(row['pattern'] is not 'X' and row['type'] is not 'r'):
            patternList.append(row['pattern'])
            pattern_image[row['pattern']] = row['image']
            
    counter = collections.Counter(patternList)
    
    for patt in counter.most_common(5):
        print patt
        print pattern_image[patt[0]]
        im = Image.open(pattern_image[patt[0]])
        im.show()

if(__name__ == "__main__"):    
   main(sys.argv[1:])
