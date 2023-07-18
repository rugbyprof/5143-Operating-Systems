# Import socket module 
import socket 
import json
import sys
from time import sleep
from helper_functions import random_id
from helper_functions import generate_stock
from helper_functions import mykwargs

produced_stocks = []

def Produce(id=None,ip='167.99.224.154',pp=8100,tq=.5):


	# local host IP '127.0.0.1' 
	host = ip

	# Define the port on which you want to connect 
	port = pp

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

	# connect to server on local computer 
	s.connect((host,port)) 

	# message you send to server 

	#while True: 

	sd = generate_stock() 
	packet = {'type':'producer','uid':id,'stock':sd['stock'],'price':sd['price']}
	packet = json.dumps(packet)

	# message sent to server 
	s.send(packet.encode('utf-8')) 

	# messaga received from server 
	response = s.recv(1024) 

	# print the received message 
	# here it would be a reverse of sent message 
	print('Received from the server :',str(response.decode('utf-8'))) 

	sleep(tq)

	# close the connection 
	s.close() 


if __name__ == '__main__': 
	uid = random_id()
	
	argv = sys.argv[1:]

	if len(argv) == 0:
		# if params are required ...  
		print("Usage: cc.py ip=167.99.224.154 tq=.25 port=8100")
		sys.exit()

	args,kargs = mykwargs(argv)

	ip = kargs.get('ip','167.99.224.154')
	port = kargs.get('port',8100)
	tq = kargs.get('tq',.5)

	Produce(uid,ip,int(port),float(tq)) 
    