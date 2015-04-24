###
## Draws a cool frequency dot grid based on start point and end point frequency
##
## D.E. Budzitowski 150876
###

import Image,ImageDraw,csv,sys,collections

##Translates the path to a list of grid coordinates
def point2Coords_three(num):
    incR = 50
    incC = 50
    num = int(num)
    y = (num/3)*incR + 25
    x = (num%3)*incC + 25
    return (x,y)
    
##Translates the path to a list of grid coordinates
def point2Coords_four(num):
    incR = 39
    incC = 46
    num = int(num)
    y = (num/4)*incR + 18
    x = (num%4)*incC + 20
    return (x,y)

def getReader(size):
    if size is 3:
        file = open("./analysis/3x3/3x3_data.csv")
        return csv.DictReader(file)
    else:
        file = open("./analysis/4x4/4x4_data.csv")
        return csv.DictReader(file)

def drawgrid(size,count):
     ## Load blank image
    im = Image.open("blank.gif")
    draw = ImageDraw.Draw(im)

    ## Pick function based on size:
    for i in xrange(0,size**2):
        if size is 3:
            point = point2Coords_three(i)
        else:
            point = point2Coords_four(i)
        i = str(i)
        rad = count[i]/5
        start = (point[0]-rad,
                 point[1]-rad,
                 point[0]+rad,
                 point[1]+rad)
        print start
        draw.ellipse(start, fill=128)
    
    im.show()
    return im

def save(size,start,end):
    if size is 3:
        start.save("./analysis/3x3/start.bmp")
        end.save("./analysis/3x3/end.bmp")
    else:
        start.save("./analysis/4x4/start.bmp")
        end.save("./analysis/4x4/end.bmp")

def main(argv):

    ##Check args
    if len(argv) is not 1:
        exit("Not enough (or too many) args!")
    size = int(argv[0])
    if size is not 3 and size is not 4:
        exit("Size: " + str(size) + "not supported!")

    ## Set up csv reader
    reader = getReader(size)
    
    ## count start and end points
    startList = []
    endList = []
    for row in reader:
        if row['type'] is not 'r':
            startList.append(row['start'])
            endList.append(row['end'])

    startCount = collections.Counter(startList)
    endCount = collections.Counter(endList)
    #print startCount
    #print endCount
    
    ## Draw!
    start = drawgrid(size,startCount)
    end = drawgrid(size,endCount)

    ## Save!
    save(size,start,end)
    

if(__name__ == "__main__"):    
   main(sys.argv[1:])
