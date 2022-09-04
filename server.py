import socket
import os
from _thread import *
import pickle
from game import *
from gameconfiguration import *
from command import *
import copy

from network import *
from globals import *
    



def server_program(hostname, port, game):
    
    server_socket = socket.socket()     

    server_socket.bind((hostname, port))  # bind host address and port together
    clientID = -1; # one per client



    # waiting for the clients to connect
    # for now max of 5 clients
    server_socket.listen(5)

    while True:
        conn, addr = server_socket.accept()
        
        network = Network(conn,addr[0],addr[1])

        clientID += 1
        start_new_thread(threaded_client, (network, clientID, game))


def threaded_client(network, client_id,game):

    try: 
        # first send the welcome msg to confirm connection
        welcome_msg = "[{}] Welcome client: {}".format(client_id,client_id)
        globals.debug_obj.info(welcome_msg)
        network.send_text(welcome_msg)
    
    
        # when the client connects for the first time give add its snake to the game
        
        game.add_snake(client_id) # [Later] This should be protected as multiple clients could add to the 'game'
        globals.debug_obj.info("Snake added {}".format(client_id))
        
       
        client_snake = game.get_snake(client_id)
       
        d = pickle.dumps(client_snake)
        
        command = Command(CMD_NEW_SNAKE,pickle.dumps(client_snake))
        network.send_cmd(command)
    

        # continous running client thread
        while True:
            
            command = network.recv_cmd()
            

            if command.cmd == NO_DATA:
                
                pass

            elif command.cmd == CMD_GET_GAME:
                
                #game.dump_snake_list()
                temp_cmd = Command(CMD_UPDATE_GAME,pickle.dumps(game))
                network.send_cmd(temp_cmd)
                
            
            elif command.cmd == CMD_UPDATE_SNAKE:
                # update the client snake information on the server game
                # this needs to be guarded as many clients might update their snakes
                
                snake = pickle.loads(command.payload)
                
                game.server_update_snake(snake)

            elif command.cmd == CMD_DELETE_FRUIT:

                fruit = pickle.loads(command.payload)
                
                game.remove_and_add_fruit(fruit)
                
                #game.dump_snake_list()

            elif command.cmd == CMD_QUIT_GAME:
            
                game.remove_snake(client_id)
                return 1
              
            
        
    except :
     
        network.close()


if __name__ == '__main__':
    globals.init_globals("s")
    game = Game(-1)
    server_program(SERVER,PORT,game)