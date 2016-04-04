from constants import SLAVE_TO_SLAVE_PORT, N_ELEVATORS
from socket import *
from threading import Thread, Lock
import time 
import broadcast 

class SlaveHandler:


	def __init__(self):
	
		self.__active_slave = [0]*N_ELEVATORS
		self.__active_slave_key = Lock()
		self.__slave_alive_thread_started = False
		self.__thread_buffering_slave_alive = Thread(target = self.__buffering_slave_alive_messages, args = (),)


	def update_slave_alive(self, elevator_id):
			self.__send(str(elevator_id),SLAVE_TO_SLAVE_PORT)

	def check_slave_alive(self):	

		if self.__slave_alive_thread_started is not True:
			self.__start(self.__thread_buffering_slave_alive)

		for i in range(0,N_ELEVATORS):
			if self.__active_slave[i] == 1:
				return i+1
		return -1 

	def __buffering_slave_alive_messages(self):

			last_message = 'This message will never be heard'
			self.__slave_alive_thread_started = True

			port = ('', SLAVE_TO_SLAVE_PORT)
			udp = socket(AF_INET, SOCK_DGRAM)
			udp.bind(port)
			udp.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

			downtime = [time.time() + 3]*N_ELEVATORS
			 

			while True:
				data, address = udp.recvfrom(1024)
				message = self.__errorcheck(data)
				#print "Message: " + message
				if message is not None:
					with self.__active_slave_key:
						self.__active_slave[int(message)-1] = 1		
						downtime[int(message)-1] = time.time() + 3
				
				for i in range(0,N_ELEVATORS):
					if downtime[i] < time.time():
						self.__active_slave[i] = 0


	def __send(self, data, port):
		send = ('<broadcast>', port)
		udp = socket(AF_INET, SOCK_DGRAM)
		udp.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
		message='<%s;%s>' % (str(len(data)), data)
		udp.sendto(message, send)
		udp.close()

	def __start(self,thread):
				thread.daemon = True # Terminate thread when "main" is finished
				thread.start()

	def __errorcheck(self,data):
		if data[0]=='<' and data[len(data)-1]=='>':

			counter=1
			separator=False
			separator_pos=0
			for char in data:
				if char == ";" and separator==False:
					separator_pos=counter
					separator=True
				counter+=1

			message_length=str(len(data)-separator_pos-1)
			test_length=str()
			for n in range(1,separator_pos-1):
				test_length+=data[n]

			if test_length==message_length and separator==True:
				message=str()
				for n in range(separator_pos,len(data)-1):
					message+=data[n]
				return message
			else:
				return None
		else:
			return None