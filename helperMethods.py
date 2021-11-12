from pixelWeight import *
from pixelAverager import *
import math

RED_INDEX = 0
GREEN_INDEX = 1
BLUE_INDEX = 2
ALPHA_INDEX = 3

def checkSurrounding(pixelLocation, pixelMap, pixelArrayCount):
    """ 
    Returns true if all pixels surrounding the position is the
    same color and has equal counts as the rest
    """
    pixel = pixelMap[pixelLocation]
    pixelCount = pixelArrayCount[pixelLocation]
    for i in range(pixelLocation[0]-1, pixelLocation[0]+2):
        for j in range(pixelLocation[1]-1, pixelLocation[1]+2):
            newPixel = pixelMap[i,j]
            newPixelCount = pixelArrayCount[i,j]

            if not pixel == newPixel or not pixelCount == newPixelCount:
                return False

    return True


def averagePixels(pixel1, count, maxCount, pixel2):
    """ 
    Averages two pixels, where the first is the dominant one 
    When count == maxCount, the returned pixel will be the first pixel
    When count == 1, the returned pixel will be the two's averaged
    """
    pixel1 = tuple(pixel1)
    newPixel = [0,0,0,0]
    for index in [RED_INDEX, GREEN_INDEX, BLUE_INDEX, ALPHA_INDEX]:
        averageVal = (tuple(pixel1)[index]+tuple(pixel2)[index])/2

        # Note that wehn maxCount = count, the new pixel should be pixel 1
        # when count = 1, the new pixel should be the average of the two pixels

        delta = averageVal - tuple(pixel2)[index] 
        newPixel[index] = round(averageVal+delta*((count-1)/(maxCount-1))) 
    return tuple(newPixel)

# Fills blobs of the same color and assigns an alias number to find max
# color of a blob

#Let me try something new
def floodFill(x_loc, y_loc, color, im):
    """ Finds the highest pixelCount in a blob of the same color """

    seenPositions = set()

    toFill = set()
    toFill.add((x_loc,y_loc))
    while not len(toFill) == 0:
        (x,y) = toFill.pop()
        # OOB
        if x < 0 or y < 0 or x >= im.size[0] or y>= im.size[1]:
            continue
        # Not the same color
        pixel_color = im.getpixel((x,y))
        if not color == pixel_color:
            continue

        if (x,y) in seenPositions:
            continue
        # print("hello")
        seenPositions.add((x,y))

        toFill.add((x-1,y))
        toFill.add((x-1,y-1))
        toFill.add((x,y-1))
        toFill.add((x+1,y-1))
        toFill.add((x+1,y))
        toFill.add((x-1,y+1))
        toFill.add((x,y+1))
        toFill.add((x+1,y+1))
    return seenPositions

def isEdgePixel(pixelLocation, pixelMap):
    """ 
    Returns true if any surrounding pixel is not the current pixel color
    """
    pixel = pixelMap[pixelLocation]
    for i in range(pixelLocation[0]-1, pixelLocation[0]+2):
        for j in range(pixelLocation[1]-1, pixelLocation[1]+2):
            newPixel = pixelMap[(i,j)]
            if not pixel == newPixel:
                return True
    return False

def diminutiveFlood(x_loc, y_loc, color, im, pixelArrayMax, colormap):
    # def sigmoid(num, maxNum):
    #     factor = math.log(2*maxNum-1)/(maxNum-1)
    #     f = lambda x, c : 2*c/(1+math.e**(-10*factor*(x-c)))
    #     return f(num, maxNum)

    def sigmoid(num, maxNum):
        h = lambda x, c : (maxNum)**(x-c+maxNum/2)+x
        return h(num, float(maxNum))

    # PCNT = 0.5
    """ Finds the highest pixelCount in a blob of the same color """
    differentPixels = []
    for i in range(x_loc-1, x_loc + 2):
        for j in range(y_loc-1, y_loc+2):
            if not im.getpixel((i,j)) == color:
                differentPixels.append(im.getpixel((i,j))) 
    newPixel = findAveragePixel(differentPixels)

    maxPixelNum = pixelArrayMax[(x_loc,y_loc)] #* 2 # *(2**26)

    seenPositions = set()
    toFill = set()
    toFill.add(((x_loc,y_loc), maxPixelNum))

    while not len(toFill) == 0:
        data = toFill.pop()
        (x,y) = data[0]
        count = data[1]
        if count == 0:
            continue
        # OOB
        if x < 0 or y < 0 or x >= im.size[0] or y>= im.size[1]:
            continue
        # Not the same color
        pixel_color = im.getpixel((x,y))
        if not color == pixel_color:
            continue

        if (x,y) in seenPositions:
            continue

        seenPositions.add((x,y))
        sigTest = sigmoid(count, maxPixelNum)
        colormap[x][y].append(pixelWeight(tuple(newPixel), sigTest))


        toFill.add(((x-1,y),count-1))
        toFill.add(((x,y-1),count-1))
        toFill.add(((x+1,y),count-1))
        toFill.add(((x,y+1),count-1))
        toFill.add(((x-1,y-1),count-1))
        toFill.add(((x-1,y+1),count-1))
        toFill.add(((x+1,y-1),count-1))
        toFill.add(((x+1,y+1),count-1))
    return seenPositions

# def generateComplement()