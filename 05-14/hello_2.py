#!/usr/bin/python2.7
import sys
import time
import socket
import thread
#from naoqi import *
from naoqi import ALProxy
from naoqi import ALModule
from naoqi import ALBroker

check = 0
#gl_value = [0]

# create python module
class myModule(ALModule):
  #"""python class myModule test auto documentation : comment needed to create a new python module"""
	gl_value = [0]
	def onSpeechRecognized(self, strVarName, value, strMessage):
		#callback when data change
		global gl_value 
		gl_value = value
		print "SpeechRecognized", " ", value, " ", len(value)
		#global check
		#check = 1
#Check if Word is in recognized WordListe		
	def onWordRecognizedBool(self, Word):
		value = gl_value
		if Word in value:
			word_index = value.index(Word)
			if value[word_index + 1] > 0.5:
				return True
			
	def _pythonPrivateMethod(self, param1, param2, param3):
		global check
		
class Nao:
	def __init__(self,ip,port):
		self.tts = ALProxy("ALTextToSpeech", ip, port)
		self.motion = ALProxy("ALMotion", ip, port)
		self.posture = ALProxy("ALRobotPosture", ip, port)
		self.memory = ALProxy("ALMemory")
		self.speech = ALProxy("ALSpeechRecognition",ip,port)
		
		#Word Reco
		self.speech.setLanguage("English") 
		wordList=["yes","exit","hello","goodbye"]
		self.speech.setWordListAsVocabulary(wordList)
		self.memory.subscribeToEvent("WordRecognized","pythonModule", "onSpeechRecognized") #  event is case sensitive !
		
		
	def sit_down(self):
		self.posture.goToPosture("Sit", 0.3)
		time.sleep(0.5)
		self.motion.setStiffnesses("Body", 0.3)
		fractionMaxSpeed=0.1
		self.motion.setAngles(["LArm"],[ 0.96, 0.03,-0.71,-1.20, 0.00, 0.30],fractionMaxSpeed)
		self.motion.setAngles(["RArm"],[ 0.96,-0.05, 0.71, 1.20, 0.00, 0.30],fractionMaxSpeed)
		self.motion.setAngles(["RLeg"],[-0.84,-0.30,-1.50, 1.02, 0.92, 0.00],fractionMaxSpeed)
		self.motion.setAngles(["LLeg"],[-0.84, 0.30,-1.50, 1.02, 0.92, 0.00],fractionMaxSpeed)
		time.sleep(0.5)
		self.motion.setStiffnesses("Body", 0.0)
		time.sleep(0.25)
		
		
	def __del__(self):
		print "self.memory.unsubscribeToEvent(WordRecognized,pythonModule)"
		self.memory.unsubscribeToEvent("WordRecognized","pythonModule") #  event is case sensitive !		
# end class Nao


class TCP():
	def __init__(self):
		ip = "141.47.114.38"
		port = 50011
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		s.connect((ip, port))
	
	def socket_listener():
		while True:
			antwort = s.recv(50) 
			print "[%s] %s" % (ip,antwort) 
			
	def console_listener():
		while True: 
			s.send( raw_input("Nachricht: "))

	def mt(self):
		try:
			thread.start_new_thread( self.socket_listener, () )
			thread.start_new_thread( self.console_listener, () )
		except:
			print "Error: unable to start thread"    

	def __del__(self):
		s.close()

#def main():
ip = "127.0.0.1"
port = 9559
broker = ALBroker("pythonBroker","0.0.0.0",0,ip,port)

nao = Nao(ip,port)
pythonModule = myModule("pythonModule")

#	tcp = Tcp()
#	tcp.mt()	#Multithread starten
print "hello World"

while(1):
	if pythonModule.onWordRecognizedBool("exit") == True:
		print "onWordRecognizedBool(exit)"
		time.sleep(2)
#nao.sit_down()


#while (1):
time.sleep(30)
print "timeout"
del nao
#del tcp
# end class main



