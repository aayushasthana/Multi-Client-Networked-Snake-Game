import math
from math import *

def collide_block(b1, b2):
    if (b1[0]>=b2[0]+15) or (b1[0]+15<=b2[0]) or (b1[1]+15<=b2[1]) or (b1[1]>=b2[1]+15):
        return False
    else:
        return True

def check_and_add_fruits(f1, f2):
    pass

'''
print(collide_block([20, 50], [10, 40]))
print(collide_block([20, 50], [15, 40]))
print(collide_block([20, 50], [30, 40]))
print(collide_block([20, 50], [40, 70]))
print(collide_block([20, 50], [35, 65]))
'''
#head = [x,y], penalties = [[x,y],[x1, y2]...]
def nextMove1(head, penalties, rewards):
    Hx = head[0]
    Hy = head[1]
    
    xCompTotal = 0
    yCompTotal = 0

    for coord in penalties:
        xDist = coord[0]-Hx
        yDist = coord[1]-Hy

        dist = math.sqrt((xDist**2)+(yDist**2))
        magnitude = 1/(dist**2)
        angle = math.atan(yDist/xDist)

        if (xDist > 0 and yDist > 0):
            angle = angle
        elif (xDist < 0 and yDist > 0):
            angle += math.pi
        elif (xDist < 0 and yDist < 0):
            angle += math.pi
        elif (xDist > 0 and yDist < 0):
            angle += 2*math.pi
        
        xComp = math.cos(angle)
        yComp = math.sin(angle)

        print("xComp = " + str(xComp) + ", yComp = " + str(yComp))
        xCompTotal += xComp
        yCompTotal += yComp
        #print(magnitude)
        #print(angle*180/math.pi)
    
    print(xCompTotal)
    print(yCompTotal)

'''
def nextMove1(head, penalties, rewards):
    Hx = head[0]
    Hy = head[1]
    
    xCompTotal = 0
    yCompTotal = 0

    for coord in penalties:
        xDist = coord[0]-Hx
        yDist = coord[1]-Hy

        dist = math.sqrt((xDist**2)+(yDist**2))
        magnitude = 1/(dist**2)
        angle = math.atan(yDist/xDist)

        if (xDist > 0 and yDist > 0):
            angle = angle
        elif (xDist < 0 and yDist > 0):
            angle += math.pi
        elif (xDist < 0 and yDist < 0):
            angle += math.pi
        elif (xDist > 0 and yDist < 0):
            angle += 2*math.pi
        
        xComp = math.cos(angle)
        yComp = math.sin(angle)

        print("xComp = " + str(xComp) + ", yComp = " + str(yComp))
        xCompTotal += xComp
        yCompTotal += yComp
        #print(magnitude)
        #print(angle*180/math.pi)
    
    print(xCompTotal)
    print(yCompTotal)
'''

def nextMove2(self, head, penalties, rewards):
    Hx = head[0]
    Hy = head[1]
    
    xCompTotal = 0
    yCompTotal = 0

    for coord in penalties:
        xDist = coord[0]-Hx
        yDist = coord[1]-Hy

        dist = math.sqrt((xDist**2)+(yDist**2))
        magnitude = 1/(dist**2)
        angle = math.atan(yDist/xDist)

        if (xDist > 0 and yDist > 0):
            angle = angle
        elif (xDist < 0 and yDist > 0):
            angle += math.pi
        elif (xDist < 0 and yDist < 0):
            angle += math.pi
        elif (xDist > 0 and yDist < 0):
            angle += 2*math.pi
        
        xComp = magnitude * math.cos(angle)
        yComp = magnitude * math.sin(angle)

        #print("xComp = " + str(xComp) + ", yComp = " + str(yComp))
        xCompTotal -= xComp
        yCompTotal -= yComp
    
    for coord in rewards:
        xDist = coord[0]-Hx
        yDist = coord[1]-Hy

        dist = math.sqrt((xDist**2)+(yDist**2))
        magnitude = 20/(dist**2)
        angle = math.atan(yDist/xDist)

        if (xDist > 0 and yDist > 0):
            angle = angle
        elif (xDist < 0 and yDist > 0):
            angle += math.pi
        elif (xDist < 0 and yDist < 0):
            angle += math.pi
        elif (xDist > 0 and yDist < 0):
            angle += 2*math.pi
        
        xComp = magnitude * math.cos(angle)
        yComp = magnitude * math.sin(angle)

        #print("xComp = " + str(xComp) + ", yComp = " + str(yComp))
        xCompTotal += xComp
        yCompTotal += yComp
    
    print("xCompTotal = " + str(xCompTotal) + ", yCompTotal = " + str(yCompTotal))

    finalAngle = math.atan(yCompTotal/xCompTotal)

    if (xCompTotal > 0 and yCompTotal > 0):
        finalAngle = finalAngle
    elif (xCompTotal < 0 and yCompTotal > 0):
        finalAngle += math.pi
    elif (xCompTotal < 0 and yCompTotal < 0):
        finalAngle += math.pi
    elif (xCompTotal > 0 and yCompTotal < 0):
        finalAngle += 2*math.pi
    
    #print(finalAngle)
    print("direction X = " + str(math.cos(finalAngle)) + ", direction Y = " + str(math.sin(finalAngle)))
    self.direction = [math.cos(finalAngle), math.sin(finalAngle)]


nextMove2([0,0],[[3,3], [-3,3], [-3,-3], [3,-3]],[[1,2], [2,2], [-1,2]])
