from pixelAverager import findAveragePixel
from PIL import Image
from pixelWeight import pixelWeight

CIRCLE_RADIUS = True

# Load the image
im = Image.open("testfiles/lines/halflines.png").convert('RGBA')
pixelMap = im.load()

colorMap = [[[] for i in range(im.size[1])] for i in range(im.size[0])]

totalPixels = im.size[0]*im.size[1]

for i in range(im.size[0]):
    for j in range(im.size[1]):
        print("Progress: "+str(i*im.size[0]+j)+"/"+str(totalPixels))
        pixelGroup = []
        for l in range(im.size[0]): 
            for m in range(im.size[1]):
                if (i,j) != (l,m):
                    radius_squared = ((l-i)**2+(m-j)**2) # **0.5
                    pixelGroup.append(pixelWeight(tuple(pixelMap[l,m]), 1/(radius_squared)))
        colorMap[i][j] = pixelWeight.averagePixels(pixelGroup, roundValues = True)
        

for i in range(im.size[0]):
    for j in range(im.size[1]):
        pixelMap[i,j] = colorMap[i][j]
                
im.show()