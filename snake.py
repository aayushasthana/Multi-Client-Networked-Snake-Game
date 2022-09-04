from cmath import pi
from http import client
from gameconfiguration import *
import random
import math


import globals
STEP_ANGLE_RADIANS = math.radians(5)

class Snake:
    def __init__(self,snake_id):
        # default start of snake will be 4 blocks ( this shoule be part of configuration)
        # list of 4 coordinates(in block size) of the snake body
        # first time snake is create - 4 block snake
        # first block is the head 
        # last block is the tail
        # direction is where the head block moves next if not arrows are pressed
        # for example : if the head_postion is [20,20], then snake_body will be at
        # [20,20], [19,20], [19,21], [19,22] - like an 'flat inverted L"
        
      
        self.snake_id = snake_id
        self.score = 0
        
        start_location = random.randint(START_LOCATIONS[snake_id][0], START_LOCATIONS[snake_id][1])
        
        self.blocks = [[start_location, start_location]]
        for i in range(1, SNAKE_SIZE+1):
            self.blocks.append([start_location-1, start_location+i])
        
        #self.blocks =[[50,50], [49,50], [49,51], [49,52]]
        self.head = self.blocks[0]#[:]  # first block
        self.grow_block = self.head[:] # last block
        self.direction_index = 0
        self.direction = [1,0]
        self.isAlive = True
        globals.debug_obj.info("Snake created {}".format(snake_id))

    def move_front(self):
        # move to the next block in the same direction
        # update the body coordinates based on the direction 
        try:
            self.grow_block = self.blocks[-1][:]     # save it to grow later
            self.head[0] += SPEED * self.direction[0]
            self.head[1] += SPEED * self.direction[1]
            self.blocks.insert (0,self.blocks.pop())  # remove the last block from the list,
            self.blocks[0] = self.head[:]             # make the first block as the head
            

        except Exception as e: print(e)

    # move in a random direction
    def move_random(self,head, penalties, rewards):
        
        # avoid penalty
        self.direction = DIRECTIONS[self.direction_index]

    # move to the closest reward
    def move_shortest_distance(self,head, penalties, rewards):
        
        shortest_reward = rewards[0]
        shortest_distance = math.hypot(shortest_reward[0]-head[0],shortest_reward[1]-head[1])
        
        
        # first look for the closest reward
        # set the direction to move towards it
        # if there are penalties in the direction, 
        #   Keep changing the direction slightly till there are no penalties
        # ideally, there would be one direction where there is no penalties
        # open question :
        #  - Should we look for a different reward if there is a penalty in the path?

        
       # first get the closest reward based on eculidian distance from the head
        for r in rewards:
            dist = math.hypot(r[0]-head[0],r[1]-head[1])
            
            if dist < shortest_distance:
                shortest_distance = dist
                shortest_reward = r
        # check and change the direction
        radians = math.atan2(shortest_reward[1] - head[1], shortest_reward[0]- head[0])
        self.direction = [math.cos(radians), math.sin(radians)]
        globals.debug_obj.info("f:{} h:{} sd:{} r{}".format(shortest_reward,head, shortest_distance,radians))
    
    def nextMove_f2(self, head, penalties, rewards, snakelist, mysnakeid):
        Hx = head[0]
        Hy = head[1]
        
        xCompTotal = 0
        yCompTotal = 0

        for coord in penalties:
            xDist = coord[0]-Hx
            yDist = coord[1]-Hy

            dist = math.sqrt((xDist**2)+(yDist**2))
            magnitude = WALL_CHARGE/(dist**2)
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
            magnitude = FRUIT_CHARGE/(dist**2)
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
        
        
        for snake in snakelist:
            if (snake.snake_id == mysnakeid):
                continue
            else:
                
                maxmagnitude = 0
                
                for coord in snake.blocks:
                    xDist = coord[0]-Hx
                    yDist = coord[1]-Hy

                    dist = math.sqrt((xDist**2)+(yDist**2))
                    magnitude = BODY_BLOCK_CHARGE/(dist**2)
                    if (magnitude > maxmagnitude):
                        maxmagnitude = magnitude
                        
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

        
        #Finding Current Angle
        currAngle = math.atan(self.direction[1]/self.direction[0])

        if (self.direction[0] > 0 and self.direction[1] > 0):
            currAngle = currAngle
        elif (self.direction[0] < 0 and self.direction[1] > 0):
            currAngle += math.pi
        elif (self.direction[0] < 0 and self.direction[1] < 0):
            currAngle += math.pi
        elif (self.direction[0] > 0 and self.direction[1] < 0):
            currAngle += 2*math.pi
        
        print("Final Angle: " + str(finalAngle) + ", Current Angle: " + str(currAngle))

        if ((finalAngle - currAngle) % (2*math.pi) < math.pi):
            finalAngle = currAngle + (STEP_ANGLE * math.pi/180)
            #self.direction = [self.direction[0] + math.cos(STEP_ANGLE*math.pi/180), self.direction[1] + math.sin(STEP_ANGLE*math.pi/180)]
            #self.move_left()
        else:
            finalAngle = currAngle - (STEP_ANGLE * math.pi/180)
            #self.move_right()
            #self.direction = [self.direction[0] - math.cos(STEP_ANGLE*math.pi/180), self.direction[1] - math.sin(STEP_ANGLE*math.pi/180)]
        
        
        print(finalAngle)
        print("direction X = " + str(math.cos(finalAngle)) + ", direction Y = " + str(math.sin(finalAngle)))
        self.direction = [math.cos(finalAngle), math.sin(finalAngle)]


    def nextMove_f1(self, head, penalties, rewards):
        Hx = head[0]
        Hy = head[1]
        
        xCompTotal = 0
        yCompTotal = 0

        for coord in penalties:
            xDist = coord[0]-Hx
            yDist = coord[1]-Hy

            dist = math.sqrt((xDist**2)+(yDist**2))
            magnitude = WALL_CHARGE/(dist**2)
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
            magnitude = FRUIT_CHARGE/(dist**2)
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

        print(finalAngle)
        print("direction X = " + str(math.cos(finalAngle)) + ", direction Y = " + str(math.sin(finalAngle)))
        self.direction = [math.cos(finalAngle), math.sin(finalAngle)]
        
    def move_left(self):
        if (self.direction_index == (len(DIRECTIONS) - 1)):
            self.direction_index = 0
        else:
            self.direction_index += 1
        
        self.direction = DIRECTIONS[self.direction_index]

    def move_right(self):
        if (self.direction_index == 0):
            self.direction_index = len(DIRECTIONS)-1
        else:
            self.direction_index -= 1
        
        self.direction = DIRECTIONS[self.direction_index]
    

    def grow(self):
        for i in range(0, GROW_BY):
            self.blocks.append(self.grow_block)

