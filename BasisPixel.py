class BasisPixel():
    def __init__(self, location, pixelWeight):
        self.location = location
        self.pixelWeight = pixelWeight
    
    def getPixelSquareDistanceFrom(self, loc):
        return (self.location[0]-loc[0])**2 + (self.location[1]-loc[1])**2
    
    