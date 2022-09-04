import pygame
from pygame.locals import *
from gameconfiguration import *
from snake import *
from game import *
import copy
import math


class GameWindow:
    def __init__(self, my_snake_id):
        
        self.snake_block_image_list = []

        pygame.init() # pygame initialization
                                                      
        self.canvas = pygame.display.set_mode((BLOCK_COLS* BLOCK_SIZE,
                                               BLOCK_ROWS* BLOCK_SIZE))    # height x width
        window_title = WINDOW_TITLE +str(my_snake_id)
        pygame.display.set_caption(window_title)                          # game window title

        # scale it for it to appear like a square, else the aspect ration makes it look like a rectangle
        temp = pygame.image.load(IMAGE_WALL).convert()  
        self.wall_block_image= pygame.transform.scale(temp, (BLOCK_SIZE,BLOCK_SIZE))

        temp = pygame.image.load(IMAGE_GRASS).convert_alpha()  
        self.grass_block_image = pygame.transform.scale(temp, (BLOCK_SIZE,BLOCK_SIZE))

        temp = pygame.image.load(IMAGE_FRUIT).convert_alpha()  
        self.fruit_block_image = pygame.transform.scale(temp, (BLOCK_SIZE,BLOCK_SIZE))

        # load all the snake block image list
        for i in range(0,5):
            temp = pygame.image.load(Image_list[i]).convert_alpha()
            self.snake_block_image_list.append(pygame.transform.scale(temp, (SNAKE_BLOCK_SIZE,SNAKE_BLOCK_SIZE)))

        self.my_snake_block_image = temp
        # painting background and the wall
        self.canvas.fill(BLACK)   
        self.blit_game_wall()
        pygame.display.flip()
        globals.debug_obj.info("Game Window created")
        # create my local game and add my local snake
        self.add_my_snake(my_snake_id)
        self.game = Game(my_snake_id)
        self.game.add_snake(my_snake_id)
        

        # top left corner - show the color of the local snake
        self.canvas.blit(self.my_snake_block_image,(0*BLOCK_SIZE, (BLOCK_COLS-2)*BLOCK_SIZE))
        self.canvas.blit(self.my_snake_block_image,(0*BLOCK_SIZE, (BLOCK_COLS-1)*BLOCK_SIZE))
        self.canvas.blit(self.my_snake_block_image,(1*BLOCK_SIZE, (BLOCK_COLS-2)*BLOCK_SIZE))
        self.canvas.blit(self.my_snake_block_image,(1*BLOCK_SIZE, (BLOCK_COLS-1)*BLOCK_SIZE))

        self.font = pygame.font.Font('freesansbold.ttf', 20)
    
    

    def add_my_snake(self,my_snake_id):
        try: 
            temp = pygame.image.load(Image_list[my_snake_id]).convert_alpha()  
            self.my_snake_block_image = pygame.transform.scale(temp, (BLOCK_SIZE,BLOCK_SIZE))
            self.my_snake_id = my_snake_id

        except Exception as e: 
            print(e)


    def add_snake(self,snake):
        
        try: 
            
            temp = pygame.image.load(Image_list[snake.snake_id]).convert_alpha()  
            self.snake_block_image = pygame.transform.scale(temp, (BLOCK_SIZE,BLOCK_SIZE))
            
        except Exception as e: 
            print(e)
        
        self.game.add_snake(snake)

    
    def tick(self, temp_game):
        # ignore the server update of your snake
        # just use the server updates of the other client snakes
       
        temp_my_snake_id = self.game.my_snake_id
        temp_my_snake = copy.deepcopy(self.game.get_snake(self.game.my_snake_id))
        self.game = copy.deepcopy(temp_game)
        self.game.remove_snake(self.my_snake_id)
        self.game.snake_list.append(temp_my_snake)
        self.game.my_snake_id = temp_my_snake_id
        
        self.game.tick()


    def refresh(self):
        
        
        self.canvas.fill(BLACK)   # painting background
        if (self.game.getMySnake().isAlive == False) :
            self.game.snake_list.remove(self.game.getMySnake())
            self.blit_game_over()
        else:
            self.blit_game_wall()
            self.blit_fruits()
            self.blit_all_snakes()
            self.blit_score()

    def blit_game_over(self):
        gameovertext = "GAME OVER!"
        text = self.font.render(gameovertext, True, RED, BLACK)
        self.canvas.blit(text,(28*BLOCK_SIZE, 22*BLOCK_SIZE))
        

    # blit the wall of the game
    def blit_game_wall(self):
        #i = y, j = x
        #G=grass, W=wall
        '''
        Score board
        for i = 0...5:
            for j = 0...45:
                paintblack();
        
        Arena
        for i = 5...51:
            for j = 0...45:
                if (i==5) || (i==50) || (j==0) || (j==44):
                    paintwall();
                else:
                    paintgrass();
        '''
        for i in range(5,51):
            for j in range(0,45):
                if (i==5) or (i==50) or (j==0) or (j==44):
                    self.canvas.blit(self.wall_block_image, (j*BLOCK_SIZE, i*BLOCK_SIZE))
                else:
                    self.canvas.blit(self.grass_block_image,(j*BLOCK_SIZE, i*BLOCK_SIZE))



        # top left corner - show the color of the local snake
        for k in range (int(BLOCK_ROWS/4), int(3*BLOCK_ROWS/4)):
            self.canvas.blit(self.my_snake_block_image,(k*BLOCK_SIZE, 0*BLOCK_SIZE))
        
    def blit_fruits(self):
       for fruit in self.game.fruit_list:
           self.canvas.blit(self.fruit_block_image,(fruit[0]*BLOCK_SIZE, fruit[1]*BLOCK_SIZE))

    
    def blit_score(self):
        scorestring = 'Scores:'
        text = self.font.render(scorestring, True, WHITE, BLACK)
        self.canvas.blit(text,(2*BLOCK_SIZE, 2*BLOCK_SIZE))
        i = 0
        for snake in self.game.snake_list:
            snake_score_text = " {} ".format(snake.score)
            text = self.font.render(snake_score_text, True, Score_color_list[snake.snake_id], BLACK)
            self.canvas.blit(text,(2*i*BLOCK_SIZE, 2*BLOCK_SIZE))
            i+=1
        
    # blit a snake
    def blit_snake(self, snake):
        #DEBUG(DEBUG_GAME_WINDOW,"start-snake_id: {} {}".format(snake.snake_id,snake.blocks))
        try:
            for block in snake.blocks:
                self.canvas.blit(self.snake_block_image_list[snake.snake_id], (block[0]*SNAKE_BLOCK_SIZE, block[1]*SNAKE_BLOCK_SIZE))
        except Exception as e: 
            print(e)
        #DEBUG(DEBUG_GAME_WINDOW," done")


    # blit all snakes
    def blit_all_snakes(self):
        #DEBUG(DEBUG_GAME_WINDOW," # of snakes {}- start".format(len(self.game.snake_list)))
        for snake in self.game.snake_list:
            if snake.isAlive == True :
                self.blit_snake(snake)

    
    def handle_key_press(self):

        retval = True
        retkey = K_ESCAPE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                retval = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:       # escape
                    retval = False
                if event.key == K_RIGHT:        # right
                    self.game.get_snake(self.game.my_snake_id).move_right()
                elif event.key == K_LEFT:       # left
                    self.game.get_snake(self.game.my_snake_id).move_left()
                elif event.key == K_UP:  
                    retkey = event.key       # up
                    pass
        return retval, retkey