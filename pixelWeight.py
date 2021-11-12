RED_INDEX = 0
GREEN_INDEX = 1
BLUE_INDEX = 2
ALPHA_INDEX = 3

from pixelAverager import *

class pixelWeight():
    def __init__(self, inputColor, inputWeight):
        self.color = tuple(inputColor)
        self.weight = inputWeight
    
    @staticmethod
    def averagePixels(pixelList, roundValues = False):
        """ Averages the pixels within a list """

        newPixel = [0,0,0,0]
        weightTotal = 0
        for pixelW in pixelList:
            pixel = tuple(pixelW.color)
            weight = pixelW.weight
            # print(weight)
            weightTotal += weight
            for index in [RED_INDEX, GREEN_INDEX, BLUE_INDEX, ALPHA_INDEX]:
                newPixel[index] += pixel[index]*weight
        if weightTotal == 0:
            return findAveragePixel([pixelList[i].color for i in range(len(pixelList))])

        # print("successful return")

        if roundValues:
            return tuple(round(val/weightTotal) for val in newPixel)
        return tuple(val/weightTotal for val in newPixel)  
    
    @staticmethod
    def groupPixels(pixelList):
        newList = []
        newPixels = {}
        for pixelW in pixelList:
            color = tuple(pixelW.color)
            weight = pixelW.weight
            if not color in newPixels.keys():
                newPixels[color] = weight
            else:
                newPixels[color] += weight
        for key in newPixels.keys():
            newList.append(pixelWeight(key, newPixels[key]))
        return newList
