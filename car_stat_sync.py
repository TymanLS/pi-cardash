#!/usr/bin/python3

###########################################################
# car_stat.py: prints information about a car using OBDII #
# By: Tyman Sin                                           #
#                                                         #
# This prints out the data in a synchronous manner by     #
# waiting for each command to return a value. This can    #
# cause blocking in GUI event loops, and the values will  #
# print one after another, so the use of asynchronous     #
# querying is recommended for GUIs instead.               #
###########################################################

import os
import time
import obd # need python-OBD library, install using `pip install obd`

# Serial device to communicate with
device = "/dev/rfcomm0"

# Set of commands to query
cmd_set = { obd.commands.RPM, 
			obd.commands.SPEED,
			obd.commands.COOLANT_TEMP,
			obd.commands.FUEL_LEVEL }

# Connect to the OBD scanner
try:
	if device is not None:
		# connect to the specified serial device
		connection = obd.OBD(device)
	else:
		# connect to a serial device automatically
		connection = obd.OBD()
except SerialException:
	print("ERROR: A serial connection error occured, make sure the serial device is correct")
	exit(1)
except:
	print("ERROR: An error occured while trying to connect")
	exit(1)

# Check if we are successfully connected to the car
if not connection.is_connected():
	print("ERROR: Car is not connected")
	exit(1)

# Add supported commands
supported_cmd_set = set()
for cmd in cmd_set:
	if obd.commands.has_command(cmd) and connection.supports(cmd):
		supported_cmd_set.add(cmd)
	else:
		print(f"WARNING: {cmd.name} command not supported")

if len(supported_cmd_set) == 0:
	print("ERROR: No supported commands specified")
	connection.close()
	exit(1)

try:
	while True:
		os.system('clear')
		print("Car Stats:")
		for cmd in supported_cmd_set:
			response = connection.query(cmd)
			print(response.value)
		time.sleep(0.2)

except KeyboardInterrupt:
	print("\nCtrl^C received, closing connection...")
	connection.close()
	print("Exiting...")

