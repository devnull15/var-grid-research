###
## Exploring why 4x4 grids have a spike of patterns with stroke length 11
## Will display all 4x4 grids of stroke length 11 in 4x4_data.csv
##
## D.E.Budzitowski 150876
###

import Image, csv

with open("./analysis/3x3/3x3_data.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    savepath = "./analysis/3x3_stroke8/"
    for row in reader:
        if(float(row['stroke']) > 7 and float(row['stroke']) < 9):
            imgpath = row['image']
            im = Image.open(imgpath)
            im.show()
            imgname = imgpath.split('/')[5]
            im.save(savepath+imgname)
