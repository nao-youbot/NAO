#!/usr/bin/python2.7
import sys
import time
import socket
import thread


class TCP():
    def __init__(self, TCP_IP, TCP_PORT):
		#ip = "141.47.114.36"
		#port = 50011
		print "connecting"
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		self.sock.connect((TCP_IP, TCP_PORT))
		print "connected"
    def socket_listener(self):
		while True:
			antwort = self.sock.recv(50) 
			print antwort
    def console_listener(self):
		while True: 
			self.sock.send(raw_input("Nachricht: "))
    def __del__(self):
		self.sock.close()


TCP_IP = "141.47.114.36"
TCP_PORT = 50011

tcp = TCP(TCP_IP, TCP_PORT)
try:
	thread.start_new_thread( tcp.socket_listener, () )
	thread.start_new_thread( tcp.console_listener, () )
#	thread.start_new_thread( reco.WordListener, () )
except:
	print "Error: unable to start one or more threads"

time.sleep(45)
print "timeout"
del tcp