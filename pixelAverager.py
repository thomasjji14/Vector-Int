RED_INDEX = 0
GREEN_INDEX = 1
BLUE_INDEX = 2
ALPHA_INDEX = 3
def findAveragePixel(pixelList):
    """ Averages the pixels within a list """
    newPixel = [0,0,0,0]
    for genpixel in pixelList:
        pixel = tuple(genpixel)
        for index in [RED_INDEX, GREEN_INDEX, BLUE_INDEX, ALPHA_INDEX]:
            newPixel[index] += pixel[index]
    return tuple(round(val/len(pixelList)) for val in newPixel)