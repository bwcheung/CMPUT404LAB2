#/usr/bin/env python

#Copyright (c) Brandon Cheung

import socket, os

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("0.0.0.0", 12345))

serverSocket.listen(5)

while True:
	(incomingSocket, address) = serverSocket.accept()
	
	childPid = os.fork()
	if (childPid != 0):
		#we must be still in the connection accepting process
		continue
	#we must be in a client talking process	

	outGoingSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	outGoingSocket.connect(("www.google.com", 80))

	done = False
	while not done:
		#fix cpu use with poll() or select
		incomingSocket.setblocking(0)

		try:
			part = incomingSocket.recv(2048)
		except IOError, exception:
			if exception.errno == 11:
				part = None
			else:
				raise
		if (part):
			outGoingSocket.sendall(part)

		outGoingSocket.setblocking(0)
		try:
			part = outGoingSocket.recv(2048)

		except IOError, exception:
			if exception.errno == 11:
				part = None
			else:
				raise

		if (part):
			incomingSocket.sendall(part)









