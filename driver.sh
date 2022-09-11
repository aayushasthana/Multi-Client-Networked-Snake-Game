#!/bin/bash

for ((i= 0; i < $2 ; i++))
do 
   python server.py &
   SERVER_PID=$!
   echo  $SERVER_PID
   python client.py  --delay 100 &
   C1 =$!
   python client.py &
   C2 =$!
   python client.py &
   C3 =$!
   wait $C1 $C2 $C3
   kill -9 $SERVER_PID
done