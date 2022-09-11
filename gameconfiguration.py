# game configuration

# player arena constants


WINDOW_TITLE = "Snakes"
BLOCK_SIZE = 15
SNAKE_BLOCK_SIZE = 15
SNAKE_SIZE = 5
GROW_BY = 5
BLOCK_ROWS = 51 # x
BLOCK_COLS = 45 # y
SCORE_BOARD_WIDTH = 45
SCORE_BOARD_HEIGHT = 5

RIGHTWALL_X = 44
LEFTWALL_X = 0
TOPWALL_Y = 5
BOTTOMWALL_Y = 50

UNINITIALIZED_BLOCK ='x'
WALL_BLOCK = 'W'
GRASS_BLOCK = 'G'
FRUIT_BLOCK = 'F'
SNAKE_HEAD_BLOCK = 'H'
SNAKE_BODY_BLOCK = 'B'

# colors

RED = (255, 0, 0) # wall color
BLUE = (0, 0, 255)
PINK = (255,105,180)
YELLOW = (255,255,0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0) # background color
WHITE = (255,255,255) # score color

Score_color_list = [RED,BLUE,PINK,YELLOW,GREEN]





# images of the blocks
#[Later] this could be generated 
IMAGE_WHITE = "images/white.png"
IMAGE_RED = "images/red.png"
IMAGE_BLUE = "images/blue.png"
IMAGE_GREEN = "images/green.png"
IMAGE_YELLOW = "images/yellow.png"
IMAGE_PINK = "images/pink.png"
IMAGE_GRASS ="images/grass.png"
IMAGE_WALL = "images/wall.png"
IMAGE_FRUIT = "images/fruit.png"
Image_list = [IMAGE_RED,IMAGE_BLUE,IMAGE_PINK,IMAGE_YELLOW,IMAGE_GREEN ]

# directions - direction operations to be applied to a block to find the new block in that direction
# (0,0) Top left, (100,100) - bottom right
# (x,y) -> up -> (x,y-1)
# (x,y) -> down -> (x,y+1)
# (x,y) -> left -> (x-1,y)
# (x,y) -> right -> (x+1,y)

UP = [0, -1]
DOWN = [0, 1]
LEFT = [-1, 0]
RIGHT = [1, 0]

NE = [(3**(1/2))/2, -1/2]
SE = [1/(2**1/2), 1/(2**1/2)]
NW = [-1/(2**1/2), -1/(2**1/2)]
SW = [-1/(2**1/2), 1/(2**1/2)]

STEP_ANGLE = 5
DIRECTIONS = []

START_LOCATIONS = [(10,15), (15,20), (20, 25), (25, 30), (30, 35)]

LOCAL_SNAKE_ID = 999

# GAME 
MAX_FRUITS = 5
SCORE_PER_FRUIT = 5

#AI
WALL_CHARGE = 1
BODY_BLOCK_CHARGE = 28
FRUIT_CHARGE = 20

# networking 
SERVER ="localhost"
PORT = 9999

# commands
NO_DATA = -1
CMD_GAME = 100
CMD_GET_GAME = CMD_GAME + 1
CMD_UPDATE_GAME = CMD_GAME + 2
CMD_DELETE_FRUIT = CMD_GAME +3
CMD_QUIT_GAME = CMD_GAME + 10

CMD_SNAKE = 200
CMD_NEW_SNAKE = CMD_SNAKE + 1
CMD_UPDATE_SNAKE = CMD_SNAKE + 2

#refresh rate (ms)
REFRESH_RATE = 100
FPS = 30
SPEED = 0.1

#debug flags
DEBUG_CLIENT_PROGRAM = False
DEBUG_GAME_WINDOW = False
DEBUG_GAME = True
DEBUG_SNAKE = True
DEBUG_SERVER_PROGRAM = True
DEBUG_NETWORK = True

# delay settings
