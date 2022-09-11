import socket
import logging
import time
import datetime
import pygame
from pygame.locals import *
import pickle
import math
import random
import copy
from command import Command

import argparse



from network import *
from gameconfiguration import *
from gamewindow import *

import globals


def client_program():
    run = True
    
    # connect to the server
    # [Later] could add more checks if the server is not running

    network = Network(socket.socket(socket.AF_INET, socket.SOCK_STREAM),SERVER,PORT)
    network.connect()
    globals.debug_obj.info("Connected to Server {}".format(SERVER))
    server_connection_msg = network.recv_text()
    globals.debug_obj.info("Welcome message from Server {}".format(server_connection_msg))
   

    
    # recv the newly created snake 
    cmd = network.recv_cmd()
    my_snake = pickle.loads(cmd.payload)
    
    client_id = my_snake.snake_id

    
    
    # intialize the grahics
    # setup the walls
    gamewindow = GameWindow(my_snake.snake_id)

    clock = pygame.time.Clock()
    last = 0  # control the refresh rate
    loop_count = 0
    old_time = datetime.datetime.now()
    network_enabled = False
    
    while run :
    
        # handle any key presses for change in direction
        run, evt = gamewindow.handle_key_press()
        #now = pygame.time.get_ticks()
        #if now - last >= REFRESH_RATE :
        clock.tick(FPS)
        try:
            # for the delay time, dont send update to the server
            network_enabled = False
            delta_ms = (datetime.datetime.now()-old_time).total_seconds() * 1000
            print("delta {}".format(delta_ms))
            if (delay < delta_ms ):
                old_time = datetime.datetime.now()
                network_enabled = True
                
            if network_enabled: 
                # Get the details of the game from server
                request_cmd = Command(CMD_GET_GAME ,b"None")
                network.send_cmd(request_cmd)
                response_cmd = network.recv_cmd()
                # Update the local game with server updates for other snakes
                # Move the local snake forward
                local_game = pickle.loads(response_cmd.payload)
                print("server update")
                gamewindow.tick(local_game)
                
                #send updated my_snake position to the server
                temp_snake = gamewindow.game.get_snake(client_id)
                cmd = Command(CMD_UPDATE_SNAKE, pickle.dumps(temp_snake))
                network.send_cmd(cmd)
                #
                if gamewindow.game.delete_fruit[0] != -1 and gamewindow.game.delete_fruit[1] != -1:
                    cmd = Command(CMD_DELETE_FRUIT,pickle.dumps(gamewindow.game.delete_fruit))
                    network.send_cmd(cmd)
           
            else:
                print("****** No server update")
                gamewindow.tick_no_server_update()
            
            
            
            # Refresh the game window graphics
            gamewindow.refresh(delay)   # blit the snakes
            pygame.display.flip()  # render the snakes
            
        except Exception as e:
            # quit the game if you are unable to connect
            # this could be the place were code could be added for simulation (later)
            print(e)
            run = False
            
    
    cmd = Command(CMD_QUIT_GAME,b" ")
    network.send_cmd(cmd)

    pygame.quit()

def create_direction_matrix():
    for i in range(0,360,STEP_ANGLE):
        DIRECTIONS.append([math.cos(i*math.pi/180), -math.sin(i*math.pi/180)])
    print(DIRECTIONS)


if __name__ == '__main__':
    
   parser = argparse.ArgumentParser(description = "Snake game client")
   parser.add_argument("-d", "--delay", help = "Example: --delay 60", required = False, default = "0")
   argument = parser.parse_args()
   if argument.delay:
    delay = int(argument.delay)
    if delay > 0:
        delay += 0
    
    globals.init_globals("c")
    
    client_program()

 