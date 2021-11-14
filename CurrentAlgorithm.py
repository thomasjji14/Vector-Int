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

# Load the image
im = Image.open("testfiles/minibox/3x.png").convert('RGBA')
pixelMap = im.load()

pixelArrayCount = np.ones(im.size, dtype = int)
pixelArrayMax = np.ones(im.size, dtype = int)
colorMap = [[[] for i in range(im.size[1])] for i in range(im.size[0])]

basisPixels = []

# Generate reigons:
splitColorReigons = []
for i in range(im.size[0]): 
    for j in range(im.size[1]):
        inReigon = False
        for reigon in splitColorReigons:
            if (i,j) in reigon:
                inReigon = True
        if not inReigon and pixelMap[i,j][ALPHA_INDEX] != 0:
            splitColorReigons.append(floodFill(i,j, im.getpixel((i,j)), im))
        

print("Reigons Generated")

# Generate counts based off of the previously determined regions
for region in splitColorReigons:
    change = True
    localMax = 0
    while change:
        localMax += 1
        change = False
        oldArray = copy.deepcopy(pixelArrayCount)
        analysisArray = copy.deepcopy(pixelArrayCount)
        
        for pixel in region:
            if checkSurrounding(pixel, pixelMap, oldArray):
                change = True
                analysisArray[pixel] += 1
        
        if change:
            # Check 1: Make sure all local maxima == localMax
            # Check 2: Circular
            change = localIsAbsoluteAndCircular(region, localMax + 1, analysisArray)

            if change:
                pixelArrayCount = analysisArray

            
np.savetxt("data.csv",pixelArrayCount)

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
    print(str(i)+"/"+str(im.size[0]))
    for j in range(im.size[1]):
        # Ignore transparent pixels
        if pixelMap[i,j][ALPHA_INDEX] == 0:
            continue

        newPixels = []
        for maxPixel in basisPixels:
            loc = maxPixel.location
            pw = maxPixel.pixelWeight

            originalColor = pw.color
            originalWeight = pw.weight
            
            if not (i,j) == maxPixel.location:
                newWeight = \
                    originalWeight/(maxPixel.getPixelSquareDistanceFrom((i,j)))
                    
            newPixels.append(pixelWeight(originalColor, newWeight))
        
        finalAveragedPixel = pixelWeight.averagePixels(newPixels, roundValues = True)
        pixelMap[i,j] = finalAveragedPixel

print("Colors finalized")


im.show()