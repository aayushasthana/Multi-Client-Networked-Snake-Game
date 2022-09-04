from fileinput import filename
import sys
import logging
import logging.config
import os
from datetime import datetime

# ================== Logger ================================
def debug_log(prefix):
    date_time = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    log_filename = "./debug/" + prefix + "-"+ date_time + str(os.getpid()) + ".log"
    formatter = logging.Formatter(fmt='%(asctime)s[%(levelname)s] %(module)s:%(lineno)d:%(funcName)10s() | %(message)s',
                                    datefmt='%H:%M:%S') # %I:%M:%S %p AM|PM format
    logging.basicConfig(filename = log_filename,format= '%(asctime)s[%(levelname)s] %(module)s:%(lineno)d:%(funcName)10s() | %(message)s',
                                    datefmt='%H:%M:%S', filemode = 'a', level = logging.INFO)
    log_obj = logging.getLogger()
    log_obj.setLevel(logging.DEBUG)
    
    # console printer
    screen_handler = logging.StreamHandler(stream=sys.stdout) #stream=sys.stdout is similar to normal print
    screen_handler.setFormatter(formatter)
    logging.getLogger().addHandler(screen_handler)

    log_obj.info("Logger object created successfully..{}".format(log_filename))
    return log_obj



def init_globals(prefix) :
    global debug_obj
    
    debug_obj = debug_log(prefix)

