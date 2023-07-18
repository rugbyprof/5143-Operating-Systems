# Import socket module 
import socket 
import json
import sys
from time import sleep
from helper_functions import random_id
from helper_functions import mykwargs

import threading
from threading import *   

consumed_stocks = []

def Consume(**kwargs):

	host = kwargs.get('host','167.99.224.154')
	port = int(kwargs.get('port',8100))
	tq = kwargs.get('tq',.5)

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

	# connect to server using ip address and port number
	s.connect((host,port)) 

	# message you send to server 
	message = {'type':'consumer','uid':id}
	#while True: 

	# turn message data into a string
	packet = json.dumps(message)

	# packet sent to server 
	s.send(packet.encode('utf-8')) 

	# response received from server 
	response = s.recv(1024) 

	# print the received message 
	print('Received from the server :',str(response.decode('utf-8'))) 
	
	sleep(tq)
	# close the connection 
	s.close() 


if __name__ == '__main__': 
	uid = random_id()
	
	argv = sys.argv[1:]

	if len(argv) == 0:
		# if params are required ...  
		print("Usage: cc.py ip=1167.99.224.154 port=8100 tq=.25 instances=1")
		sys.exit()

	args,kargs = mykwargs(argv)


	mykwargs = {}
	mykwargs['uid'] = uid
	mykwargs['host'] = kargs.get('ip','167.99.224.154')
	mykwargs['port'] = kargs.get('port',8100)
	mykwargs['tq'] = kargs.get('tq',.5)
	instances = kargs.get('instances',1)

	Consume(**mykwargs) 

    