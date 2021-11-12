from PIL import Image
import numpy as np
import copy
from numpy.lib.function_base import average
from numpy.lib.shape_base import split
from helperMethods import *
from pixelWeight import *
from pixelAverager import *
from tqdm import tqdm
from BasisPixel import BasisPixel

RED_INDEX = 0
GREEN_INDEX = 1
BLUE_INDEX = 2
ALPHA_INDEX = 3

HUE_INDEX = 0
SATURATION_INDEX = 1
VALUE_INDEX = 2

DEBUG_OUTPUT = True

UNITS_PER_PIXEL = 10000

# Load the image
im = Image.open("testfiles/minibox/mini3.png").convert('RGBA')
pixelMap = im.load()

pixelArrayCount = np.ones(im.size, dtype = int)
pixelArrayMax = np.ones(im.size, dtype = int)
colorMap = [[[] for i in range(im.size[1])] for i in range(im.size[0])]

basisPixels = []

change = True
maxNum = 0

# Determine the pixel counts
while change:
    maxNum += 1
    print("Iteration: "+str(maxNum))
    change = False
    oldArray = copy.deepcopy(pixelArrayCount)

    for i in range(1, im.size[0]-1):
        for j in range(1, im.size[1]-1):
            pixel = pixelMap[i, j]
            if not pixel[ALPHA_INDEX] == 0:
                if checkSurrounding((i,j), pixelMap, oldArray):
                    change = True
                    pixelArrayCount[(i,j)] += 1

print("Added Counts")

# Generate reigons:
splitColorReigons = []
for i in range(im.size[0]): 
    for j in range(im.size[1]):
        inReigon = False
        for reigon in splitColorReigons:
            if (i,j) in reigon:
                inReigon = True
        if not inReigon:
            splitColorReigons.append(floodFill(i,j, im.getpixel((i,j)), im))

print("Reigons Generated")

# Associate highest counts from each reigon
for reigon in splitColorReigons:
    highestCount = 0
    for point in reigon:
        if pixelArrayCount[point] > highestCount:
            highestCount = pixelArrayCount[point]
    for point in reigon:
        if pixelArrayCount[point] == highestCount:
            basisPixels.append(BasisPixel(point, pixelWeight(pixelMap[point], highestCount)))

print("Highest Count Pixels Determined")


basisPixelLocations = []
for maxPixel in basisPixels:
    basisPixelLocations.append(maxPixel.location)

for i in range(im.size[0]): 
    for j in range(im.size[1]):
        newPixels = []
        
        # Base pixels should not be altered
        if (i,j) not in basisPixelLocations:
            for maxPixel in basisPixels:
                loc = maxPixel.location
                pw = maxPixel.pixelWeight

                originalColor = pw.color
                originalWeight = pw.weight
                if i == 10 and j == 10:
                    print('d')
                
                newWeight = \
                    originalWeight/(maxPixel.getPixelSquareDistanceFrom((i,j)))

                newPixels.append(pixelWeight(originalColor, newWeight))
            pixelMap[i,j] = pixelWeight.averagePixels(newPixels, roundValues = True)

print("Colors finalized")


im.show()