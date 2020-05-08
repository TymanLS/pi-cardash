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
		if not self.__connection.is_connected():
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
			self.__connection.watch(cmd)

	def start(self):
		self.__connection.start()

	def stop(self):
		self.__connection.stop()

	def is_connected(self):
		return self.__connection.is_connected()

	def query(self, command, unit:str=None):
		quantity = self.__connection.query(command).value
		if not quantity:
			return 0
		elif unit:
			return quantity.to(unit).magnitude
		else:
			return quantity.magnitude

	def __del__(self):
		self.__connection.stop()
		self.__connection.close()
