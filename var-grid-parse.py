import csv, Image, ImageDraw, os, sys

def reset(filename):
    file = open(filename)
    return csv.DictReader(file)

def drawGrid(path):
    im = Image.open("4x4dots.gif")
    draw = ImageDraw.Draw(im)
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
        im.show()
    del draw
    return im

def invalidDataCheck(row,col):
    for num in row[col].split('.'):
        if num != 'X' and (num == '' or int(num) > 15):
            return True
    return False

##Translates the path to a list of grid coordinates
def path2Coords(path):
    ret = []
    incR = 46
    incC = 39
    for num in path.split('.'):
        num = int(num)
        r = (num/4)*incR + 20
        c = (num%4)*incC + 18
        pair = (r,c)
        ret.append(pair)
    print ret
    return ret


##global vars
fn = 'Pattern-Proj-24MAR.csv'
reader = reset(fn)
plist = [] #list of all patterns
glist = [] #list of all guesses
plistDraw = [] #list of pattern drawings
glistDraw = [] #list of guess drawings

###Valid data check
print("Checking data for valid coordinates...")
for row in reader:
    for col in row:
        ##Only patterns for now
        if(col != "Participant #" and "q" not in col):

            ##Validate Data
            if invalidDataCheck(row,col):
                exit("Error! #" + row['Participant #'] + " at " + col)

            ##Draw the grid
            im = drawGrid(row[col])
            ##store patterns in appropriate lists
            if "pattern" in col:
                if row[col] != 'X': #throw out bad passwords
                    plist.append(row[col])
                plistDraw.append(im)
            if "guess" in col:
                if row[col] != 'X': #throw out bad passwords
                    glist.append(row[col])
            glistDraw.append(im)
            del im


###Compute Recall
reader = reset(fn)
print("\nChecking Recall...")
k = 0 #pattern counter
for row in reader:
    print("Participant #" + row['Participant #'])
    correct = 0
    for i in xrange(1,4):
        p = row['pattern' + str(i)]
        for j in xrange(1,4):
            r = row['recall' + str(j)]
            if p!='X' and r!='X': #throw out bad passwords
                if(p == r):
                    correct += 1
                    ##save image to correct folder
                    path = "./" + os.path.splitext(fn)[0] + "/correct/"
                    path += "pattern" + str(k) + ".jpg"
                    #print path
                    #plistDraw[k].save(path)
                    #print("Correct!")
                else:
                    x = 1
                    #print("Incorrect!")
        k += 1

    print(str(correct) + "/3")
                
                
###Check for Compromised Passwords
print("\nChecking for compromised passwords...")
for p in plist:
    for g in glist:
        if p == g:
            print("Pattern Compromised!")

##Parse Questions Somehow...
