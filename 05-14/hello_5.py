#!/usr/bin/python2.7
import sys
import time
import socket
import thread
from naoqi import ALProxy
from naoqi import ALModule
from naoqi import ALBroker

check = 0
#gl_value = [0]

# create python module
class myModule(ALModule):
  #"""python class myModule test auto documentation : comment needed to create a new python module"""
	#global gl_value
	def onSpeechRecognized(self, strVarName, value, strMessage):
		#callback when data change
		#gl_value = value
		print "SpeechRecognized", " ", value, " ", len(value)
		nao.tts.say(value[0])
		time.sleep(1)
		if "exit" in value:
			if value[value.index("exit") + 1] > 0.5:
				nao.tts.say("I understood exit")
		if "sit down" in value:
			if value[value.index("sit down") + 1] > 0.5:
				nao.sit_down()
	
	def WordDetection(wordList)
		nao.speech.setWordListAsVocabulary(wordList)
		nao.memory.subscribeToEvent("WordRecognized","pythonModule", "onSpeechRecognized") #  event is case sensitive !
		nao.memory.unsubscribeToEvent("WordRecognized","pythonModule") #  event is case sensitive !

	def _pythonPrivateMethod(self, param1, param2, param3):
		global check

class Nao:
	def __init__(self,ip,port):
		self.tts = ALProxy("ALTextToSpeech", ip, port)
		self.motion = ALProxy("ALMotion", ip, port)
		self.posture = ALProxy("ALRobotPosture", ip, port)
		self.memory = ALProxy("ALMemory")
		self.speech = ALProxy("ALSpeechRecognition",ip,port)

		#Word Recognition
		self.speech.setLanguage("English") 
		wordList=["hello","goodbye","yes","no", "exit", "sit down"]
		pythonModule.WordDetection(wordList)


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
		#print "memory.unsubscribeToEvent(WordRecognized,pythonModule)"
		#self.memory.unsubscribeToEvent("WordRecognized","pythonModule") #  event is case sensitive !		

class TCP():
    def __init__(self, TCP_IP, TCP_PORT):
		print "connecting..."
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

#def main():
#ip 192.168.1.101
NAO_IP = "127.0.0.1"
NAO_PORT = 9559
#TCP_IP = "141.47.114.36"
TCP_IP = "192.168.1.100"
TCP_PORT = 50012

broker = ALBroker("pythonBroker","0.0.0.0",0,NAO_IP,NAO_PORT)

nao = Nao(NAO_IP, NAO_PORT)
pythonModule = myModule("pythonModule")

tcp = TCP(TCP_IP, TCP_PORT)

#Thread handling
try:
	thread.start_new_thread( tcp.socket_listener, () )
	thread.start_new_thread( tcp.console_listener, () )
except:
	print "Error: unable to start tcp threads"

#nao.sit_down()


time.sleep(15)
print "timeout"
del tcp
print "tcp killed"
del nao
print "nao killed"
