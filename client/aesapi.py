''''
Maeda Hanafi
This file interfaces the aes methods
'''

import binascii
import aes
import numpy as np
np.set_printoptions(formatter={'int':hex})
import textwrap


API_DEBUG = False
INPUT_BLOCK_LEN = 128

def convert2ascii(arr):
	'''
	Convert an array of hex, [0x6d, 0x69, 0x63] --> mic
	First it converts each element into binary of length 8 and then calling chr to convert to ascii
	Finally concats all and returns the string
	'''
	concat = map(lambda x:chr(int(bin(x)[2:].zfill(8), 2)), arr)
	return ''.join(concat)


'''
@message is the full message
@return a string of numbers, where each two numbers represent a byte in the message i.e. 35 ==> 0x23 
This method will prepare the message for encryption
'''
def encrypt_message(message):
	#Turn the string length into a some multiple of 16
	padding = 16-(len(message)%16)
	factor16len = padding + len(message)
	message = message.ljust(factor16len)

	#Divide the message into blocks of 16 chars
	messageblocks =  list(map(''.join, zip(*[iter(message)]*16)))
	allciphers = []
	#messageblock = 'microprogramming'
	for messageblock in messageblocks:
		if API_DEBUG: print messageblock+"|"
		#msg_hex = [0x73L 0x61L 0x67L 0x65L 0x20L 0x66L 0x6fL 0x72L 0x20L 0x65L 0x6eL 0x63L 0x72L 0x79L 0x70L 0x74L]
		msg_hex =  map(lambda x: int(binascii.hexlify(x), 16), list(messageblock))

		#cipher = [0x40L 0x9eL 0xb4L 0x5L 0x3bL 0x66L 0x27L 0xc3L 0x4dL 0xdaL 0x5cL 0x70L 0x63L 0xcfL 0x50L 0xb7L]
		cipher =  aes.encrypt(msg_hex)

		allciphers = allciphers + cipher

		if API_DEBUG: print "messageblock:"+messageblock
		if API_DEBUG: print "msg_hex:"+str(np.array(msg_hex))
		if API_DEBUG: print "cipher:"+str(np.array(cipher)) 

	#allciphers = [8, 46, 162] ==> concat = [0008, 0046, 0162] ==> 000800460162
	if API_DEBUG: print allciphers
	concat = reduce(lambda x, y: str(x).zfill(4)+str(y).zfill(4),allciphers)
	if API_DEBUG: print concat 
	return concat
		
'''
@cipher is a concatenation of int values representing the cipher
@return the message
'''
def decrypt_message(cipher):
	#cipher  = 000800460162
	if API_DEBUG: print 'recieved cipher: '+cipher
	#Divide the message into blocks of 4 chars and turn each one into hex
	#messageblocks =  ['0008', '0046', '0162']
	messageblocks =  list(map(''.join, zip(*[iter(cipher)]*4)))
	#convert to hex
	messageblocks = map(lambda x: int(hex(int(str(x))), 16),messageblocks)
	if API_DEBUG: print 'messageblocks: '+str(np.array(messageblocks))

	totdeciphered = []
	st = 0
	end = 16
	#send blocks 16 bytes to decipher 
	while end<=len(messageblocks):
		deciphered = aes.decrypt(messageblocks[st:end])
		if API_DEBUG: print "deciphered:"+str(np.array(deciphered))
		totdeciphered = totdeciphered + deciphered

		#set the pointers to to the next block
		st = st + 16
		end = end + 16

	if API_DEBUG: print "total deciphered:"+str(np.array(totdeciphered))
	combined = convert2ascii(totdeciphered)
	if API_DEBUG: print "final:"+combined
	return combined

def test():
	API_DEBUG = True

	cipher = encrypt_message('This method will prepare the message for encryption')
	if API_DEBUG: print '******************************'
	message = decrypt_message(cipher)

test()
