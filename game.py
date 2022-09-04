
from re import X
from tkinter import TOP
from gameconfiguration import *
from snake import *
import copy 
import time
import globals

class Game: 

    def __init__(self,client_id):
        
        
        self.snake_list = []
        self.fruit_list = []
        self.wall_list = []
        self.delete_fruit = [-1,-1]

        
        
        self.my_snake_id = client_id  # this only for the clients
        self.create_game_wall()
        self.check_and_add_fruits()
        #self.dump_map()
        globals.debug_obj.info("Game Created..")
        
    # map functions

    '''
        Map creation
        map[i][j] represent type of cell at coordinates (j,i)
        i = row, j = column
        This is the initial creation of the map with no snakes or fruits
    ''' 
    def create_game_wall(self):
        
        for i in range(5,51):
            for j in range(0,45):
                if (i==5) or (i==50) or (j==0) or (j==44):
                    #self.canvas.blit(self.wall_block_image, (j*BLOCK_SIZE, i*BLOCK_SIZE))
                    self.wall_list.append([j,i])
                #else:
                    #self.canvas.blit(self.grass_block_image,(j*BLOCK_SIZE, i*BLOCK_SIZE))
        
    '''
    def update_game_map_with_snake(self,snake):
        self.map[int(snake.head[0])][int(snake.head[1])] = SNAKE_HEAD_BLOCK
        
        for block in snake.blocks :
            self.map[int(block[0])][int(block[1])] = SNAKE_BODY_BLOCK
            
        
    
    def update_game_map_with_fruit(self,fruit_x, fruit_y):
        self.map[fruit_x][fruit_y] = FRUIT_BLOCK
    '''
    def dump_map(self):
        globals.debug_obj.info("DUMP-MAP-START")
        #globals.debug_obj.info(self.map)
        globals.debug_obj.info("DUMP-MAP-END")
    

    def add_snake(self, snake_id):
        
        globals.debug_obj.info("Server add snake")
        s = Snake(snake_id)
        
        self.snake_list.append(s)
        globals.debug_obj.info("Map updated with snake body {}".format(s.blocks))
        
        #self.update_game_map_with_snake(s)

        #self.dump_map()
        
        

    
    def remove_snake(self,snake_id):
        
        for snake in self.snake_list:
            if (snake_id == snake.snake_id):
                self.snake_list.remove(snake)
                break
        

    
    def get_snake(self, snake_id):

        for snake in self.snake_list:
            if (snake.snake_id == snake_id):
                return snake

    def dump_snake_list(self):
        for snake in self.snake_list:
            print("Server snake {} {}".format(snake.snake_id,snake.blocks))

        
    def server_update_snake(self, s):
        
        for snake in self.snake_list:
            
            if (snake.snake_id == s.snake_id):
                self.snake_list.remove(snake)
                if (snake.isAlive):
                    self.snake_list.append(s)
                break

    
    # check for collision with wall
    # increase score when a snake 'eats' a cherry
    def update_snakes(self):
        #globals.debug_obj.info("Check for wall collision")
        # check for collision with wall
        for wb in self.wall_list:
            if self.collide_block(self.getMySnake().head, wb):
                print("Wall collided head:{} wall:{}".format(self.getMySnake().head, wb))
                self.getMySnake().isAlive = False

        #globals.debug_obj.info("Check for fruit collision")
        for fruit in self.fruit_list:
            if self.collide_block(self.getMySnake().head, fruit):
                print("Fruit collided head:{} fruit:{}".format(self.getMySnake().head, fruit))
                self.getMySnake().score += 1
                self.getMySnake().grow()
                print("Grow {} {} ".format(len(self.getMySnake().blocks), self.getMySnake().blocks))
                self.delete_fruit = fruit
                self.fruit_list.remove(fruit)
                break

        #globals.debug_obj.info("Check for snake collision")
        for snake in self.snake_list:
            if (snake.snake_id == self.my_snake_id):
                continue
            else:
                for block in snake.blocks:
                    if self.collide_block(self.getMySnake().head, block):
                        print("Snake collision: {} snake:{}".format(self.getMySnake().head, block))
                        self.getMySnake().isAlive = False
        #globals.debug_obj.info("Check for  collision Done")


    def collide_block(self, b1, b2):
        if (b1[0]>=b2[0]+1) or (b1[0]+1<=b2[0]) or (b1[1]+1<=b2[1]) or (b1[1]>=b2[1]+1):
            return False
        else:
            return True


        
    def remove_and_add_fruit(self, fruit):
        for f in self.fruit_list:
            if fruit[0] == f[0] and fruit[1] == f[1] :
                self.fruit_list.remove(f)
                x = random.randint(LEFTWALL_X+1,RIGHTWALL_X-1)
                y = random.randint(TOPWALL_Y+1,BOTTOMWALL_Y-1)
                self.fruit_list.append((x,y))

                break
    
    def check_and_add_fruits(self):
        if (len(self.fruit_list) < MAX_FRUITS):
            for i in range(0,MAX_FRUITS-len(self.fruit_list)):
                # add fruits at random location
                x = random.randint(LEFTWALL_X+1,RIGHTWALL_X-1)
                y = random.randint(TOPWALL_Y+1,BOTTOMWALL_Y-1)
                self.fruit_list.append((x,y))
                #self.update_game_map_with_fruit(x,y)
        self.delete_fruit = [-1,-1]
        

    def check_for_wall_collision(self, snake):
        retval = False  # False if no collision, 0 = x, 1 = y


        if (snake.head[0] == RIGHTWALL_X-1 and snake.direction == RIGHT):
            retval = True
        elif (snake.head[0] == LEFTWALL_X+1 and snake.direction == LEFT):
            retval = True
        elif (snake.head[1] == TOPWALL_Y+1 and snake.direction == UP):
            retval = True
        elif (snake.head[1] == BOTTOMWALL_Y-1 and snake.direction == DOWN):
            retval = True
        
        if (retval):
            snake.move_right()
        
        return retval
    
                

    def tick(self) :
        
        self.update_snakes()
        if (self.getMySnake().isAlive):
            
            self.get_snake(self.my_snake_id).move_front()
            #time.sleep(0.1)
            #self.get_snake(self.my_snake_id).nextMove_f1(self.getMySnake().head, self.wall_list, self.fruit_list)
            self.get_snake(self.my_snake_id).nextMove_f2(self.getMySnake().head, self.wall_list, self.fruit_list, self.snake_list, self.my_snake_id)
        
    def getMySnake(self):
        for snake in self.snake_list:
            if snake.snake_id == self.my_snake_id:
                return snake