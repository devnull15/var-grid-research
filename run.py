###
## Will run three.py and four.py based on args provided
## D.E. Budzitowski 150876
###
import sys, os, python.three, python.four

def main(argv):
    fn = "./csv"
    size = int(argv[0])
    ##Read args--get filename
    if(len(argv) != 2 or size < 3 or size > 4):
        exit("var-grid-parse.py [3|4] <date>");

    if(size is 3):
        fn +="/3x3/Pattern-Proj-" + argv[1] + ".csv"
        if(os.path.isfile(fn)):
            python.three.main(fn)
        else:
            exit("File not found: " + fn)

    elif(size is 4):
        fn +="/4x4/Pattern-Proj-" + argv[1] + ".csv"
        if(os.path.isfile(fn)):
            python.four.main(fn)
        else:
            exit("File not found: " + fn)

    else:
        exit("var-grid-parse.py [3|4] <date>");

if(__name__ == "__main__"):
   main(sys.argv[1:])
