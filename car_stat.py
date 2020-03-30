#!/usr/bin/python3

###########################################################
# car_stat.py: prints information about a car using OBDII #
# By: Tyman Sin                                           #
#                                                         #
# This script uses asynchronous querying to get OBDII     #
# data from a car's ECU. The OBDII adapter must be set    #
# up as a serial device.                                  #
###########################################################

import os
import time
import argparse
import obd # need python-OBD library, install using `pip install obd`

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("portstr", nargs='?', default=None, help="The serial device file or COM port of the OBDII adapter")
args = parser.parse_args()

# Serial device to communicate with
port = args.portstr

# Set of commands to query
cmd_dict = { 'RPM': obd.commands.RPM, 
			 'SPEED': obd.commands.SPEED,
			 'COOLANT_TEMP': obd.commands.COOLANT_TEMP,
			 'FUEL_LEVEL': obd.commands.FUEL_LEVEL }
cmd_set = set()
for key, cmd in cmd_dict.items():
	cmd_set.add(cmd)

# Connect to the OBDII adapter
try:
	if port is not None:
		# connect to the specified serial device
		connection = obd.Async(port)
	else:
		# connect to a serial device automatically
		connection = obd.Async()
except SerialException:
	print("ERROR: A serial connection error occured, make sure the serial device is correctly set up")
	exit(1)
except:
	print("ERROR: An error occured while trying to connect")
	exit(1)

# Check if we are successfully connected to the car
if not connection.is_connected():
	print("ERROR: Car is not connected")
	exit(1)

# Remove unsupported commands
for cmd in cmd_set.difference(connection.supported_commands):
	cmd_dict.pop(cmd.name, None)
	print(f"WARNING: {cmd.name} command not supported")

# Exit if there are not valid commands
if len(cmd_dict) == 0:
	print("ERROR: No supported commands specified")
	connection.close()
	exit(1)
else:
	for key, cmd in cmd_dict.items():
		connection.watch(cmd)

# Wait a little, then start the update loop
time.sleep(3)
connection.start()

try:
	while True:
		os.system('clear')
		print("Car Stats:")
		for key, cmd in cmd_dict.items():
			val = connection.query(cmd).value
			if val is not None:
				if key == "SPEED": 
					print(key + ": " + str(val.to('mph')))
				else:
					print(key + ": " + str(val))
		time.sleep(0.02)

except KeyboardInterrupt:
	print("\nCtrl^C received, closing connection...")
	connection.close()
	print("Exiting...")

