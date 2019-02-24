




def boxCoordinates(width, height, boxSize):
    ratioX = boxSize/width
    ratioY = boxSize/height
    isCoveredX = False   
    isCoveredY = False
    numBoxesX = int((1/ratioX)*2 - 1)
    numBoxesY = int((1/ratioY)*2 - 1)
    boxCoord = []

    for i in range(numBoxesX):
        xCoord = int(boxSize/2 * i)
        for k in range(numBoxesY):
            yCoord = int(boxSize/2 * k)
            if (xCoord + boxSize == width): 
                isCoveredX = True
            if (yCoord + boxSize == height):
                isCoveredY = True
            boxCoord.append((xCoord,yCoord))

    if (isCoveredX == False and isCoveredY == False):
        print("hi")
        boxCoord.append((width-boxSize,height-boxSize))

    print (boxCoord)

boxCoordinates(10,20, 2.8)







