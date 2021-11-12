from pixelAverager import findAveragePixel
from PIL import Image
from pixelWeight import pixelWeight

CIRCLE_RADIUS = True

# Load the image
im = Image.open("testfiles/minibox/mini.png").convert('RGBA')
pixelMap = im.load()

colorMap = [[[] for i in range(im.size[1])] for i in range(im.size[0])]

for i in range(im.size[0]): 
    for j in range(im.size[1]):
        for l in range(im.size[0]): 
            for m in range(im.size[1]):

                # Compliment generator 
                if tuple(pixelMap[l,m]) != tuple(pixelMap[i,j]):
                    if CIRCLE_RADIUS:
                        radius = round(((l-i)**2+(m-j)**2)**0.5)
                    else:
                        radius = max(abs(l-i), abs(m-j))
                    colorMap[i][j].append(pixelWeight(tuple(pixelMap[l,m]), radius))

for i in range(im.size[0]): 
    for j in range(im.size[1]):
        currentGroup = colorMap[i][j]

        # Understandably so this is rather an ineffecient way of doing so,
        # but the purpose of this is to make the most central pixels
        # the highest values, and the farthest the lowest, where
        # the minimum value is 1.
        weightList = []
        for item in currentGroup:
            weightList.append(item.weight)
        maxWeight = max(weightList)+1
        for item in currentGroup:
            item.weight = maxWeight - item.weight

        r = 0
        g = 0
        b = 0
        a = 0

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

        pixelMap[i,j] = (int(r), int(g), int(b), 255)
        # pixelMap[i,j] = findAveragePixel([(int(r), int(g), int(b), 255), pixelMap[i,j]])
                
im.show()