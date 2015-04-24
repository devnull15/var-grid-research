import csv, Image, ImageDraw, os, sys, getopt, collections
from symmetry import horiz_symmetry, vert_symmetry
from pattern import Pattern
from record import record_CSV

##GLOBAL VARS###
plist = {} #list of all patterns
glist = {} #list of all guesses
rlist = {} #list of all recalls

###FUNCTIONS###
def reset(filename):
    file = open(filename)
    return csv.DictReader(file)


def drawGrid(path):
    ##Draw the patterns
    im = Image.open("3x3dots.gif")
    draw = ImageDraw.Draw(im)
    if(path == 'X'):
        draw.line((0, 0) + im.size, fill=128)
        draw.line((0, im.size[1], im.size[0], 0), fill=128)
    else:
        gridList = path2Coords(path)
        start = (gridList[0][0]-6,
                 gridList[0][1]-6,
                 gridList[0][0]+6,
                 gridList[0][1]+6)
        draw.ellipse(start, fill=128)
        for i in xrange(0,len(gridList)-1):
            draw.line(gridList[i] + gridList[i+1], fill=128)
        #im.show()
    del draw
    return im


def storeGrid(im,row,col):
    ##store patterns in appropriate lists (excluding invalid)
    parNum = row['Participant #']
    if "pattern" in col:
        patNum = col[7:]
        key = parNum + '-' + patNum
        plist[key] = Pattern('p', row[col], im)
    elif "guess" in col:
        gNum = col[5:]
        key = parNum + '-' + gNum
        glist[key] = Pattern('g', row[col], im)
    elif "recall" in col:
        rNum = col[6:]
        key = parNum + '-' + rNum
        rlist[key] = Pattern('r', row[col], im)
    return


def invalidDataCheck(reader):

    for row in reader:
        for col in row:
            ##Only patterns for now
            if(col != "Participant #" and "q" not in col):
                ##Validate Data
                for num in row[col].split('.'):
                    if num != 'X' and (num == '' or int(num) > 8):
                        print("Error! #" + row['Participant #'] + " at " + col)
                        return True
                    ##Check for duplicate nodes
                    if collections.Counter(row[col].split('.')).most_common(1)[0][1] > 1:
                        print("Error! #" + row['Participant #'] + " at " + col)
                        return True
                        
    return False

##Translates the path to a list of grid coordinates
def path2Coords(path):
    ret = []
    incR = 50
    incC = 50
    for num in path.split('.'):
        num = int(num)
        y = (num/3)*incR + 25
        x = (num%3)*incC + 25
        pair = (x,y)
        ret.append(pair)
    #$print ret
    return ret


def recall(fn):

    correctList = {} #counts the number of correct recalls per participant
    
    for key, pattern in plist.iteritems():
        pattern = pattern.pattern
        print pattern
        partNum = key.split("-")[0]
        pattNum = key.split("-")[1]

        #Initialize participant's recall count
        if not correctList.has_key(partNum):
            correctList[partNum] = 0

        #$print("Key: " + key + " Pattern: " + pattern);
        #$print("participant: " + part + " num: " + num);

        ##Check all 3 recall values for a user
        correct = False
        rootPath = "./analysis/3x3/" + os.path.splitext(os.path.basename(fn))[0]
        for i in xrange(1,4):
            ##Don't check invalid patterns
            if pattern == 'X':
                break
            rkey = partNum + '-' + str(i)
            if rlist[rkey].pattern == pattern:
                correct = True
                break;
        if correct:
            correctList[partNum] += 1
            ##save image to correct folder
            path = rootPath + "/correct/" + partNum + "pattern" + pattNum + ".bmp"
            print("Saving: " + path)
            plist[key].setImgPath(path) #save image path
            plist[key].setRecall(1) #mark pattern as recalled
            plist[key].img.save(path)
            #print("Correct!")
        else:
            path = rootPath + "/incorrect/" + partNum + "pattern" + pattNum + ".bmp"
            print("Saving: " + path)
            plist[key].setImgPath(path)
            plist[key].img.save(path)

    print("Scores:")
    for partNum,correctNum in correctList.iteritems():
        print("Participant #" + partNum + " " + str(correctNum) + "/3")


def compromised(fn):
    rootPath = "./analysis/3x3/" + os.path.splitext(os.path.basename(fn))[0] + "/compromised/"
    for k1,p in plist.iteritems():
        partNum = k1.split("-")[0] #participant number
        pattNum = k1.split("-")[1] #pattern number
        for k2,g in glist.iteritems():
            if p!='X' and p == g:
                print("Pattern Compromised!")
                print("pattern: " + k1 + " guess: " + k2)
                path = rootPath + partNum + "pattern" + pattNum + ".bmp"
                print("Saving: " + path)
                plist[k1].img.save(path)
                plist[k1].setCompromised(1) #mark pattern as compromised


def symmetry():
    for key_pattern in plist.iteritems():
        key = key_pattern[0]
        plist[key].setSymmetryH(horiz_symmetry(3,key_pattern))
        plist[key].setSymmetryV(vert_symmetry(3,key_pattern))
    for key_pattern in glist.iteritems():
        key = key_pattern[0]
        glist[key].setSymmetryH(horiz_symmetry(3,key_pattern))
        glist[key].setSymmetryV(vert_symmetry(3,key_pattern))
    for key_pattern in rlist.iteritems():
        key = key_pattern[0]
        rlist[key].setSymmetryH(horiz_symmetry(3,key_pattern))
        rlist[key].setSymmetryV(vert_symmetry(3,key_pattern))

def compute_metrics():
    print("*** Computing symmetry...")
    symmetry()
    print("*** Done.")
        
###END FUCTIONS###


###MAIN###
def main(fn):

    ###Valid data check
    reader = reset(fn)
    print("Checking data for valid coordinates...")
    if invalidDataCheck(reader):
        exit("Invalid Data, exiting...")
    else:
        print("All data valid!\n")


    ###Draw and store grids
    reader = reset(fn)
    print("Drawing and storing grids...")
    for row in reader:
        for col in row:
            if(col != "Participant #" and "q" not in col):
                ##Draw the grids
                im = drawGrid(row[col])
                ##then store it in approrpriate arrays
                storeGrid(im, row,col)
    print("Done.\n")

    #$print(plistDraw.keys())


    ###Compute Recall
    reader = reset(fn)
    print("Checking Recall...")
    recall(fn)
    print("Done.")
                
    ###Check for Compromised Passwords
    print("\nChecking for compromised passwords...")
    compromised(fn)
    print("Done.\n")

    ###Compute metrics for anaylsis...
    print("\nComputing metrics...")
    compute_metrics()
    print("Done.\n")

    ### Record data to CSV
    print("\nWriting data to csv...")
    record_CSV(fn,plist.values()+glist.values()+rlist.values())
    print("Done.\n")

    ##Parse Questions Somehow...

###END MAIN###

if(__name__ == "__main__"):    
   main(sys.argv[1:])
