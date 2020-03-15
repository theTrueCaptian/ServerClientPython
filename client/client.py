from socket import *
from Crypto.Cipher import AES
import sys
import select
import string
import thread
import socket
import select
import socket
import threading
import time
#from cryptography.fernet import Fernet
from Crypto.Cipher import AES

'''
shutdown = False
  
def receiving(name,sock):
	#print "Client"
	while 1:
		try:
			from cryptography.fernet import Fernet
			from Crypto.Cipher import AES
			#while true:
			data, addr = sock.recvfrom(2048)      # returns string and address from source.
			# Decryption
			#print data
			decryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
			# print data + "suite obj active" 
			#print data + "---->this is the encrypted form \n"
			plain_text = decryption_suite.decrypt((data))
			#f = Fernet('UN_CY-VmhvnvG28OPJSKr7k4CrJyIfQeJuyuvhAIWOg=')
			#plain_text = f.decrypt(data)
			 
			print time.ctime(time.time()) +"::" + plain_text


		except:
			pass
		  
		finally:
			pass
		#tlock.release()           # end of critical section.
			      
host='127.0.0.1'  #to be changed.
port=0
server=(host,8080)
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #using IPV4, UDP.
s.bind((host,port))   #s.bind takes one argument address.
#s.setblocking(0)  # going to accept all connection requests.
rt = threading.Thread(target = receiving,args = ("recvthread", s))  # passing the initialised socket to thread.
rt.start()    #start thread

alias = raw_input("\n\Name: ")
key = raw_input("\n\Password: ")
message= raw_input(alias + "-> ")
s.sendto(alias + "::" + message, server)
while message !=  'q' :
	if message != '' :
		message = raw_input()
		message = alias + ":" + message
	
	# Encryption
	encryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
	cipher_text = encryption_suite.encrypt(message.ljust(32))
	# s.sendto(alias + "::" + message, server)     #if u want to send plain text.
	#f = Fernet('UN_CY-VmhvnvG28OPJSKr7k4CrJyIfQeJuyuvhAIWOg=')   #predetermined key
	#token = f.encrypt(message)

	s.sendto(cipher_text,server)  #sending encrypted message to server.
	#s.sendto(alias + "::" + token,server)  #sending encrypted message to server.
	#print data   

shutdown = True
rt.join()
s.close()
'''
HOST = '127.0.0.1'
PORT = 8080
ADDR = (HOST, PORT)

 
def chat_client():
	#if(len(sys.argv) == 2) :
	#	print 'Usage : python chat_client.py hostname port'
	#	sys.exit()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)
	 
	# connect to remote host
	try :
		s.connect(ADDR)
	except :
		print 'Unable to connect'
		sys.exit()
     
	print 'Connected to remote host. You can start sending messages'
	sys.stdout.write(''); sys.stdout.flush()
     
	while 1:
		socket_list = [sys.stdin, s]
		 
		# Get the list sockets which are readable
		ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
		 
		for sock in ready_to_read:             
			if sock == s:
				# incoming message from remote server, s
				data = sock.recv(4096)
				if not data :
					print '\nDisconnected from chat server'
					sys.exit()
				else :
					
					#Decrypt the message if the user has indicated password
					if data[0:7]!='Server>' and key!='':
						
						# Decryption
						decryption_suite = AES.new(key, AES.MODE_CBC, 'This is an IV456')
						plain_text = decryption_suite.decrypt(data)
						
						#print data
						sys.stdout.write('\n'+plain_text)

					else:
						#print data
						sys.stdout.write('\n'+data)
					
					sys.stdout.write('\n'); sys.stdout.flush()     


            
			else :
				# user entered a message
				msg = sys.stdin.readline()

				if key!='':
					whole_message = alias+">"+msg
					padding = (int)(float(16*(int)(len(whole_message)/16+1)))	# float(16*(int)(100/16+1)) = 112
					whole_message = whole_message.ljust(padding)
					
					#Encryption
					encryption_suite = AES.new(key, AES.MODE_CBC, 'This is an IV456')
					cipher_text = encryption_suite.encrypt(whole_message)
		
					s.send(cipher_text)
				else:
					s.send(alias+">"+msg)
				sys.stdout.write('Me>'+msg); sys.stdout.flush() 


if __name__ == "__main__":

	alias = raw_input("\nName: ")

	#Prompt the key that will decode the messages
	key = raw_input("\nPassword: ")
	if key!='':
		padding = (int)(float(16*(int)(len(key)/16+1)))
		key = key.ljust(padding)

	sys.exit(chat_client())

