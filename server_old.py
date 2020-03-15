from socket import *
import thread

import signal

# The key is a 16 byte arrray in hex
shared_key = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f]

BUFF = 1024
HOST = '127.0.0.1'
PORT = 8080
MAX_CLIENTS = 10
CONNECTION_LIST = []

def close_handler(signum, frame):
	#This is called when the terminal session is closed
	serversocket.close()
	pass

#Safely close sockets when ctrl+c happens
# Otherwise this error would happen: http://stackoverflow.com/questions/19071512/socket-error-errno-48-address-already-in-use
#run> ps -fA | grep python
# kill <2nd num, proc num>
signal.signal( signal.SIGHUP, close_handler )

def broadcast_data (sock, message):
	#Do not send the message to master socket and the client who has send us the message
	for socket in CONNECTION_LIST:
		if socket != serversocket and socket != sock :
			try :
				socket.send(message)
			except :
				# broken socket connection may be, chat client pressed ctrl+c for example
				socket.close()
				CONNECTION_LIST.remove(socket)

#Call this when received
def client_handler(clientsocket, addr):
	print "Connected client from: "+str(addr)
	broadcast_data(clientsocket, "!@!Connected client from: "+str(addr))

	while 1:
		data = clientsocket.recv(1024)
		if not data:
			break
		print "Received Message: "+repr(data)
		broadcast_data(clientsocket, data)

	clientsocket.close()

#Listen for a max 10 clients
ADDR = (HOST, PORT)
serversocket = socket(AF_INET, SOCK_STREAM)
serversocket.bind(ADDR)
serversocket.listen(MAX_CLIENTS) 
# Add server socket to the list of readable connections
CONNECTION_LIST.append(serversocket)

print "Listening at "+str(HOST)+":"+str(PORT)

#Continuously listen for incoming clients and then pass the handler to client_handler()
while 1:
	clientsocket, addr = serversocket.accept()
	CONNECTION_LIST.append(clientsocket)
	thread.start_new_thread(client_handler, (clientsocket, addr))
	broadcast_data(clientsocket, "!@![%s:%s] entered room\n" % addr)

serversocket.close()