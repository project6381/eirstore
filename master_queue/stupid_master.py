from message_handler import MessageHandler
from constants import SLAVE_TO_MASTER_PORT, MASTER_TO_SLAVE_PORT
import time


def main():
	message_handler = MessageHandler()
	queue_id = 1


	active_slaves = 1
	acknowledges = 0
	execute_queue = 0

	acknowledged_queue_id = []
	low_id = 999



	executer_id = [0]*8
	while True:
		
		slave_message = message_handler.receive_from_slave()
		#print ['floor:'] + slave_message['master_queue_floor'] + ['button:'] + slave_message['master_queue_button'] 

		if slave_message['slave_id'] < low_id:
			low_id = slave_message['slave_id']
			print low_id
	
			


		if queue_id == int(slave_message['queue_id']): 
			acknowledges += 1
			print '------------Acknowledge------------'

		if acknowledges == active_slaves:
			execute_queue = 1
			print '------------Execute queue------------'
			message_handler.send_to_slave(slave_message['master_queue_floor'],slave_message['master_queue_button'],executer_id,execute_queue,queue_id, low_id)
			execute_queue = 0
			acknowledges = 0
			queue_id += 1
		else: 
			message_handler.send_to_slave(slave_message['master_queue_floor'],slave_message['master_queue_button'],executer_id,execute_queue,queue_id, low_id)
		time.sleep(0.1)


if __name__ == "__main__":
    main()

