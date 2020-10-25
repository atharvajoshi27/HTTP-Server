#!/bin/bash

if [ $# -lt 1 ]
then
	echo "Syntax instructions :"
	echo "To start server : ./server.sh start <port_number>"
	echo "To stop server  : ./server.sh stop"
	exit

elif [ $1 == "start" ]
then
	if [ $# -lt 2 ]
	then
		echo "Syntax instructions :"
		echo "To start server : ./server.sh start <port_number>"
		echo "To stop server  : ./server.sh stop"
		exit
	fi
	python3 server.py $2

elif [ $1 == "stop" ]
then 
	pkill -f server.py

else
	echo "Syntax instructions :"
	echo "To start server : ./server.sh start <port_number>"
	echo "To stop server  : ./server.sh stop"
fi