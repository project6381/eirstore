from slave_driver import SlaveDriver
from slave_handler import SlaveHandler
from message_handler import MessageHandler
from constants import SLAVE_TO_MASTER_PORT, MASTER_TO_SLAVE_PORT
import elevator
import time



def main():
	slave_id = 2
	message_handler = MessageHandler(slave_id)
	slave_driver = SlaveDriver()
	slave_handler = SlaveHandler()

	#my_id = get IP address on this computer
	acknowledge = 4
	run_floor = 0
	run_button = 0
	old_f = None
	old_but = None

	floor_up = [0]*4
	floor_down = [0]*4

	while True:

		#slave_handler.update_slave_alive(my_id)

		if slave_handler.check_slave_alive() == slave_id:
			active_slave = True

		
		position = slave_driver.read_position()

		master_message = message_handler.receive_from_master()
		
		(floor,button) = slave_driver.pop_floor_panel_queue()

		if floor is not None:
			if button == 0:
				floor_up[floor] = 1
			elif button == 1: 
				floor_down[floor] = 1 	
			

		for i in range (0,4):
			if (master_message['master_floor_up'][i] != 0):
				floor_up[i] = 0

			if (master_message['master_floor_down'][i] != 0):
				floor_down[i] = 0
		
		time.sleep(0.3)

		

		message_handler.send_to_master(floor_up,floor_down,slave_id,position[0],position[1],position[2],master_message['queue_id'])
		

		print floor_up
		print floor_down


		'''
		(run_floor,run_button) = message_handler.get_my_master_order()
		
		print run_floor
		print run_button

		if run_floor is not None:
			slave_driver.queue_elevator_run(run_floor,run_button)
		'''

		master_queue = master_message['master_floor_up'] + master_message['master_floor_down']
		slave_driver.master_queue_elevator_run(master_queue)
		
		

		print ['floor_up:'] + master_message['master_floor_up'] + ['floor_down:'] + master_message['master_floor_down'] 
		#print master_message['queue_id']
				


		time.sleep(0.5)

		

if __name__ == "__main__":
    main()