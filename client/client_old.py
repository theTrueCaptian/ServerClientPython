from socket import *
import aesapi
import sys
import select
import string

IS_HAS_PASSWORD = False

def prompt() :
	print '\n'
	sys.stdout.write('<You> ')
	sys.stdout.flush()

HOST = '127.0.0.1'
PORT = 8080
ADDR = (HOST, PORT)
if(len(sys.argv) == 2) : #programname password
	password = sys.argv[1]
	IS_HAS_PASSWORD = True

s = socket()
s.connect(ADDR)
prompt()

while 1:
	socket_list = [sys.stdin, s]
	 
	# Get the list sockets which are readable
	read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
	 
	for sock in read_sockets:
		#incoming message from remote server
		if sock == s:
			data = sock.recv(4096)
			if not data :
				print '\nDisconnected from chat server'
				sys.exit()
			else :
				print '\n'
				#Decrypt the message if the user has indicated password
				if IS_HAS_PASSWORD and data[0:3]!='!@!':
					sys.stdout.write(aesapi.decrypt_message(data))
				else:
					sys.stdout.write(data)
				prompt()
		 
		#user entered a message
		else :
			msg = sys.stdin.readline()
			s.send(aesapi.encrypt_message(HOST+':'+str(PORT)+">"+msg))
			prompt()

