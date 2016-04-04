from random import randint
from master_handler import MasterHandler
from message_handler import MessageHandler
from constants import SLAVE_TO_MASTER_PORT, MASTER_TO_SLAVE_PORT, DIRN_DOWN, DIRN_UP, DIRN_STOP
import time



def main():
	
	message_handler = MessageHandler()
	master_handler = MasterHandler()
	queue_id = 1

	button_orders = [0,0,0,0,0,0,0,0]
	elevator_positions = [[0,0,0],[0,0,0],[0,0,0]]
	elevator_orders = [0,0,0,0,0,0,0,0]
	elevator_online = [0,0,0]


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

	while True:

		master_handler.update_master_alive(my_id)

		#print "Check master alive: " + str(master_handler.check_master_alive())
		#print "I am not master, my id is: " + str(my_id) 

		if master_handler.check_master_alive() == my_id:
			active_master = True

		time.sleep(0.5)

		while active_master:

			master_handler.update_master_alive(my_id)

			#print "I am master, my id is: " + str(my_id)

			

			slave_message = message_handler.receive_from_slave()
			#print ['floor_up:'] + slave_message['slave_floor_up'] + ['floor_down:'] + slave_message['slave_floor_down'] 
			#print queue_id

			#if slave_message['direction'] is not DIRN_STOP:
			last_direction = slave_message['direction']



			if slave_message['last_floor'] == slave_message['next_floor']:
				arrived = slave_message['last_floor']	
				if (last_direction == DIRN_UP) or (last_direction == DIRN_STOP):
					slave_message['slave_floor_up'][arrived] = 0
				if (last_direction == DIRN_DOWN) or (last_direction == DIRN_STOP):
					slave_message['slave_floor_down'][arrived] = 0

			slave_id = slave_message['slave_id']


			for elevator in range(0,3):
				#elevator_online[elevator]=randint(0,1)
				elevator_online[0] = 1
				elevator_online[1] = 0
				elevator_online[2] = 0

				if slave_id-1 == 0:
					elevator_positions[elevator][slave_id-1]=slave_message['last_floor']
				else:
					elevator_positions[elevator][0]=randint(0,3)
				#if slave_id-1 == 1:
					#elevator_positions[elevator][slave_id-1]=slave_message['last_floor']
				#else:
					#elevator_positions[elevator][1]=randint(0,3)
				#if slave_id-1 == 2:
					#elevator_positions[elevator][slave_message['slave_id']-1]=slave_message['last_floor']
				#else:
					#elevator_positions[elevator][2]=randint(0,2)

				if (elevator_positions[elevator][0] > elevator_positions[elevator][1]) and (elevator_positions[elevator][2]==2):
					elevator_positions[elevator][2]=0
				if (elevator_positions[elevator][0] < elevator_positions[elevator][1]) and (elevator_positions[elevator][2]==0):
					elevator_positions[elevator][2]=2
				if elevator_positions[elevator][2] == 1:
					elevator_positions[elevator][0]=elevator_positions[elevator][1]
				if (elevator_positions[elevator][0] == 0) and (elevator_positions[elevator][2] == 0):
					elevator_positions[elevator][2] == 1
				if (elevator_positions[elevator][0] == 3) and (elevator_positions[elevator][2] == 2):
					elevator_positions[elevator][2] == 1


	
			button_orders = slave_message['slave_floor_up'] + slave_message['slave_floor_down']
			#print button_orders

			elevator_orders = master_handler.order_elevator(button_orders, elevator_positions, elevator_online)
			#print elevator_orders

			for i in range (0,4):
				goto_floor_up[i] = elevator_orders[i]
				goto_floor_down[i] = elevator_orders[i+4]

			#print "elevator_online"
			#print elevator_online
			#print "elevator_positions:"
			#print elevator_positions
			#print "button_orders:"
			#print button_orders
			
			#print "elevator_orders:"
			#print elevator_orders
			#print "\n"
			

			#if queue_id == int(slave_message['queue_id']): 
			#	acknowledges += 1
			#	print '111111111111111111111111111111111111111111111111111111111'

			#if acknowledges == active_slaves:
			#	execute_queue = 1
			#	print '12222222222222222222222222222222222222222222222222222'
			#	message_handler.send_to_slave(slave_message['slave_floor_up'],slave_message['slave_floor_down'],executer_id,execute_queue,queue_id)
			#	execute_queue = 0
			#	acknowledges = 0
			#	queue_id += 1
			#else: 
			#	message_handler.send_to_slave(slave_message['slave_floor_up'],slave_message['slave_floor_down'],executer_id,execute_queue,queue_id)
			
			message_handler.send_to_slave(goto_floor_up,goto_floor_down,executer_id,execute_queue,queue_id)
			time.sleep(0.5)


			if master_handler.check_master_alive() != my_id:
				active_master = False



if __name__ == "__main__":
    main()