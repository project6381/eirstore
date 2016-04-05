from random import randint
from master_handler import MasterHandler
from message_handler import MessageHandler
from constants import SLAVE_TO_MASTER_PORT, MASTER_TO_SLAVE_PORT, DIRN_DOWN, DIRN_UP, DIRN_STOP, N_ELEVATORS
import time
from collections import Counter


def main():
	
	message_handler = MessageHandler()
	master_handler = MasterHandler()
	queue_id = 1

	button_orders = [0]*8
	last_button_orders = [10]*8
	elevator_positions = [[0,1,2],[3,4,5],[6,7,8]]
	elevator_orders = [0]*8
	last_elevator_orders = [10]*8
	elevator_online = [0]*N_ELEVATORS
	elevators_received_current_queue_id = [0]*N_ELEVATORS


	active_slaves = 0
	acknowledges = 0
	execute_queue = 0
	arrived = 0
	acknowledged_queue_id = []
	goto_floor_up = [0]*4
	goto_floor_down = [0]*4

	last_direction = 0

	executer_id = [0]*8
	my_id = 1
	active_master = False
	downtime_elevator_online = [time.time() + 3]*N_ELEVATORS
	downtime_queue_id = time.time() + 3
	timeout_active_slaves = 0
	while True:

		master_handler.update_master_alive(my_id)

		if master_handler.check_master_alive() == my_id:
			active_master = True

		print "I am NOT master, my id is: " + str(my_id)

		time.sleep(0.5)

		while active_master:

			#print "I AM master, my id is: " + str(my_id)

			master_handler.update_master_alive(my_id)

			slave_message = message_handler.receive_from_slave()
			if slave_message is not None:

				#print slave_message
				#print ['floor_up:'] + slave_message['slave_floor_up'] + ['floor_down:'] + slave_message['slave_floor_down'] 
				

				
				if slave_message['last_floor'] == slave_message['next_floor']:
					arrived = slave_message['last_floor']	
					if (last_direction == DIRN_UP) or (last_direction == DIRN_STOP):
						slave_message['slave_floor_up'][arrived] = 0
						button_orders[arrived] = 0
					if (last_direction == DIRN_DOWN) or (last_direction == DIRN_STOP):
						slave_message['slave_floor_down'][arrived] = 0
						button_orders[arrived+4] = 0
						
					

				last_direction = slave_message['direction']
				slave_id = slave_message['slave_id']
				elevator_positions[slave_id-1] = [slave_message['last_floor'],slave_message['next_floor'],slave_message['direction']] 
				
				
				for i in range(0,4):
					if (button_orders[i] == 1) or (slave_message['slave_floor_up'][i] == 1): 
						button_orders[i] = 1

				for i in range(0,4):
					if (button_orders[i+4] == 1) or (slave_message['slave_floor_down'][i] == 1): 
						button_orders[i+4] = 1
				

				#button_orders = slave_message['slave_floor_up'] + slave_message['slave_floor_down']

				

				if queue_id == slave_message['queue_id']:
					elevators_received_current_queue_id[slave_id-1] = 1


				active_slaves = elevator_online.count(1)

				#print (button_orders != last_button_orders) and (active_slaves == elevators_received_current_queue_id.count(1))
				if (button_orders != last_button_orders) and (active_slaves == elevators_received_current_queue_id.count(1) or timeout_active_slaves == 1): # and (0 not in elevators_queue_id):
					print '1111111111111111111111111111111111'
					queue_id += 1
					if queue_id > 9999: 
						queue_id = 1
					last_button_orders = button_orders[:]
					print 'hei'
					downtime_queue_id = time.time() + 1
					timeout_active_slaves = 0

				
				#print elevators_received_current_queue_id
				#print active_slaves
				#print queue_id
				print button_orders
				print last_button_orders
				downtime_elevator_online[slave_id-1] = time.time() + 3
				elevator_online[slave_id-1] = 1
					
				
				
				
				elevator_orders = master_handler.order_elevator(last_button_orders, elevator_positions, elevator_online)

				goto_floor_up[0:4] = elevator_orders[0:4]
				goto_floor_down[0:4] = elevator_orders[4:8]
				#print elevator_orders
			
			message_handler.send_to_slave(goto_floor_up,goto_floor_down,executer_id,execute_queue,queue_id)
			
				

			for i in range(0,N_ELEVATORS):
				if downtime_elevator_online[i] < time.time():
					elevator_online[i] = 0

			if downtime_queue_id < time.time():
				for i in range(0,N_ELEVATORS):
					timeout_active_slaves = 1

			time.sleep(0.1)

			if master_handler.check_master_alive() != my_id:
				active_master = False




if __name__ == "__main__":
    main()