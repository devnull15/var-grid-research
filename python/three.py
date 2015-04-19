import csv, Image, ImageDraw, os, sys, getopt, collections
from symmetry import horiz_symmetry

##GLOBAL VARS###
plist = {} #list of all patterns
glist = {} #list of all guesses
rlist = {} #list of all recalls
plistDraw = {} #list of pattern drawings
glistDraw = {} #list of guess drawings



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
    ##store patterns in appropriate lists (including invalid)
    parNum = row['Participant #']
    if "pattern" in col:
        patNum = col[7:]
        key = parNum + '-' + patNum
        plist[key] = row[col]
        plistDraw[key] = im
    elif "guess" in col:
        gNum = col[5:]
        key = parNum + '-' + gNum
        glist[key] = row[col]
        glistDraw[key] = im
    elif "recall" in col:
        gNum = col[6:]
        key = parNum + '-' + gNum
        rlist[key] = row[col]
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
            if rlist[rkey] == pattern:
                correct = True
                break;
        if correct:
            correctList[partNum] += 1
            ##save image to correct folder
            path = rootPath + "/correct/" + partNum + "pattern" + pattNum + ".bmp"
            print("Saving: " + path)
            plistDraw[key].save(path)
            #print("Correct!")
        else:
            path = rootPath + "/incorrect/" + partNum + "pattern" + pattNum + ".bmp"
            print("Saving: " + path)
            plistDraw[key].save(path)

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
                plistDraw[k1].save(path)
                print("Saving: " + path)

def symmetry():
    for key,p in plist.iteritems():
        print horiz_symmetry(3,p)

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

    ###Compute and record symmetry
    symmetry()

    ##Parse Questions Somehow...

###END MAIN###

if(__name__ == "__main__"):    
   main(sys.argv[1:])
