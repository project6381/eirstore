from random import randint
from master_handler import MasterHandler
from message_handler import MessageHandler
from constants import SLAVE_TO_MASTER_PORT, MASTER_TO_SLAVE_PORT, DIRN_DOWN, DIRN_UP, DIRN_STOP, N_ELEVATORS
import time



def main():
	
	message_handler = MessageHandler()
	master_handler = MasterHandler()
	queue_id = 1

	button_orders = [0,0,0,0,0,0,0,0]
	elevator_positions = [[0,0,0],[0,0,0],[0,0,0]]
	elevator_orders = [0,0,0,0,0,0,0,0]
	elevator_online = [0]*N_ELEVATORS

	active_slaves = 1
	acknowledges = 0
	execute_queue = 0
	arivied = 0
	acknowledged_queue_id = []
	goto_floor_up = [0]*4
	goto_floor_down = [0]*4

	last_direction = 0

	executer_id = [0]*8
	my_id =1
	active_master = False
	downtime = [time.time() + 3]*N_ELEVATORS

	while True:

		master_handler.update_master_alive(my_id)

		if master_handler.check_master_alive() == my_id:
			active_master = True

		time.sleep(0.5)

		while active_master:

			master_handler.update_master_alive(my_id)

			slave_message = message_handler.receive_from_slave()

			#print ['floor_up:'] + slave_message['slave_floor_up'] + ['floor_down:'] + slave_message['slave_floor_down'] 
			#print queue_id

			last_direction = slave_message['direction']
			slave_id = slave_message['slave_id']

			print slave_id
			
			
			downtime[slave_id-1] = time.time() + 3
			elevator_online[slave_id-1] = 1
				
			for i in range(0,N_ELEVATORS):
				if downtime[i] < time.time():
					elevator_online[i] = 0

			print elevator_online
			
			if slave_message['last_floor'] == slave_message['next_floor']:
				arrived = slave_message['last_floor']	
				if (last_direction == DIRN_UP) or (last_direction == DIRN_STOP):
					slave_message['slave_floor_up'][arrived] = 0
				if (last_direction == DIRN_DOWN) or (last_direction == DIRN_STOP):
					slave_message['slave_floor_down'][arrived] = 0

			button_orders = slave_message['slave_floor_up'] + slave_message['slave_floor_down']

			elevator_orders = master_handler.order_elevator(button_orders, elevator_positions, elevator_online)

			goto_floor_up[0:4] = elevator_orders[0:4]
			goto_floor_down[4:] = elevator_orders[4:]
			
			message_handler.send_to_slave(goto_floor_up,goto_floor_down,executer_id,execute_queue,queue_id)
			time.sleep(0.5)


			if master_handler.check_master_alive() != my_id:
				active_master = False
			



if __name__ == "__main__":
    main()