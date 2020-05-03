#!/usr/bin/python3

###########################################################
# car_stat.py: prints information about a car using OBDII #
# By: Tyman Sin                                           #
#                                                         #
# This script uses asynchronous querying to get OBDII     #
# data from a car's ECU. The OBDII adapter must be set    #
# up as a serial device.                                  #
###########################################################

### Import modules
import obd # need python-OBD library, install using `pip install obd`

# Export modules
commands = obd.commands

class CarStat:
	def __init__(self, commands:set, portstr:str=None):
		self.__connection = obd.Async(portstr) # connect to the specified serial device
		if not is_connected(self):
			# Not connected
			raise Exception

		self.__cmd_set = commands.intersection(self.__connection.supported_commands)
		# Remove unsupported commands
		for cmd in commands.difference(self.__connection.supported_commands):
			print(f"Warning: {cmd.name} command not supported")
		if not self.__cmd_set:
			# No supported commands
			self.__connection.close()
			raise Exception

		for cmd in self.__cmd_set:
			print(f"Watching {cmd.name}")
			connection.watch(cmd)

		self.__connection.start()

	def is_connected(self)
		return self.__connection.is_connected()

	def query(self, command, unit:str=None):
		if unit:
			return self.__connection.query(command).to(unit)
		else:
			return self.__connection.query(command)
		
	def __del__(self):
		self.__connection.close()
