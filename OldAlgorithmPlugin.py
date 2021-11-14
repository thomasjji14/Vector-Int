from PIL import Image
import numpy as np
import copy
from numpy.lib.function_base import average
from numpy.lib.shape_base import split
from helperMethods import *
from pixelWeight import *
from pixelAverager import *
from tqdm import tqdm

RED_INDEX = 0
GREEN_INDEX = 1
BLUE_INDEX = 2
ALPHA_INDEX = 3

HUE_INDEX = 0
SATURATION_INDEX = 1
VALUE_INDEX = 2

SIGMOID_LINEAR_COEFFICIENT = 18
EXPONENTIAL_LINEAR_COEFFICIENT = 8

DEBUG_OUTPUT = True
# DEBUG_OUTPUT = False

# Load the image
im = Image.open("testfiles/minibox/mini.png").convert('RGBA')
pixelMap = im.load()

pixelArrayCount = np.ones(im.size, dtype = int)
pixelArrayMax = np.ones(im.size, dtype = int)
colorMap = [[[] for i in range(im.size[1])] for i in range(im.size[0])]

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

print("Added the counts")

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

# Associate highest counts from each reigon
for reigon in splitColorReigons:
    highestCount = 0
    for point in reigon:
        if pixelArrayCount[point] > highestCount:
            highestCount = pixelArrayCount[point]
    for point in reigon:
        pixelArrayMax[point] = highestCount

print("Determined high counts")

for reigon in splitColorReigons:
    for point in list(reigon):
        for l in range(0, im.size[0]): 
            for m in range(0, im.size[1]):
                if not (l,m) in reigon:
                    # print('yeeeho')
                    radius = round(((l-i)**2+(m-j)**2)**0.5)
                    colorMap[point[0]][point[1]].append(pixelWeight(tuple(pixelMap[l,m]), radius))

print("Flooded")

if DEBUG_OUTPUT:
    # NOTE: ENABLE THIS TO EXPORT ENVIORNMENTAL OUTPUT
    for i in range(0, im.size[0]):
        for j in range(0, im.size[1]):
            if len(colorMap[i][j]) != 0:
                currentGroup = colorMap[i][j]
                weightList = []
                for item in currentGroup:
                    weightList.append(item.weight)
                maxWeight = max(weightList)+1
                for item in currentGroup:
                    item.weight = maxWeight - item.weight

                testGroup = pixelWeight.groupPixels(currentGroup)

                r = 0
                g = 0
                b = 0

                totalWeights = 0
                for pixel in testGroup:
                    weightModifier = pixel.weight**8
                    r += pixel.color[0] * weightModifier
                    b += pixel.color[1] * weightModifier
                    g += pixel.color[2] * weightModifier
                    totalWeights += weightModifier

                r /= totalWeights
                g /= totalWeights
                b /= totalWeights

                complementPixel = (round(r),round(g),round(b), 255)
                pixelMap[i,j] = complementPixel
            else:
                pixelMap[i,j] = (0,0,0,0)
else:
    # Find the average pixel color to take, and assigns them
    for i in range(0, im.size[0]):
        for j in range(0, im.size[1]):
            pixel = tuple(pixelMap[i,j])
            if len(colorMap[i][j]) != 0:

                currentGroup = colorMap[i][j]
                # weightList = []
                # for item in currentGroup:
                #     weightList.append(item.weight)
                # maxWeight = max(weightList)+1
                # for item in currentGroup:
                #     item.weight = maxWeight - item.weight

                r = 0
                g = 0
                b = 0

                totalWeights = 0
                for pixel in currentGroup:
                    weightModifier = pixel.weight**1
                    r += pixel.color[0] * weightModifier
                    b += pixel.color[1] * weightModifier
                    g += pixel.color[2] * weightModifier
                    totalWeights += weightModifier

                r /= totalWeights
                g /= totalWeights
                b /= totalWeights

                complementPixel = (int(r),int(g),int(b), 255)

    
                pixelMap[i,j] = averagePixels(
                    pixelMap[i,j], pixelArrayCount[i,j],
                    pixelArrayMax[i,j],
                    complementPixel
                    )
            else:
                pixelMap[i,j] = pixel

print("Colors finalized")


im.show()