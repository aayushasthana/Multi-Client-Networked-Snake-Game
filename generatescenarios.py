from cgitb import scanvars
import random
from turtle import screensize
from gameconfiguration import *

fruitCount = 5
positionCount = 20
scenario = [[[0,0] for i in range(positionCount)] for j in range(fruitCount+1)]
#print(scenario)

for i in range(0, fruitCount+1):
    if (i==0):
        for j in range (0, positionCount):
            scenario[i][j][0] = -1
            scenario[i][j][1] = -1
    else:
        for j in range (0, positionCount):
            scenario[i][j][0] = random.randint(LEFTWALL_X+1,RIGHTWALL_X-1)
            scenario[i][j][1] = random.randint(TOPWALL_Y+1,BOTTOMWALL_Y-1)

#print(scenario)

for i in range(0, fruitCount+1):
    print("Fruit #" + str(i) + " positions: " + str(scenario[i]))