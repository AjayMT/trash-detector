


def boxCoordinates(width, height, boxSize):
    ratioX = boxSize/width
    ratioY = boxSize/height
    isCoveredX = False   
    isCoveredY = False
    numBoxesX = int((1/ratioX)*4 - 1)
    numBoxesY = int((1/ratioY)*4 - 1)
    boxCoord = []

    for i in range(numBoxesX):
        xCoord = int(boxSize/4 * i)
        for k in range(numBoxesY):
            yCoord = int(boxSize/4 * k)
            if (xCoord + boxSize == width): 
                isCoveredX = True
            if (yCoord + boxSize == height):
                isCoveredY = True
            boxCoord.append((xCoord,yCoord))

    if (isCoveredX == False and isCoveredY == False):
        boxCoord.append((width-boxSize,height-boxSize))

    return (boxCoord)








