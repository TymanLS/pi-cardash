#!/usr/bin/python3


import gpsd # Must have single gpsd instance running
import time

gpsd.connect()

try:
	while True:
		# ensure that the GPS is active and that we can get a response
		while True:
			try:
				gps_response = gpsd.get_current()
			except UserWarning:
				continue
			break

		if gps_response.mode >= 2:
			print(f"{gps_response.position()}: {gps_response.get_time(local_time=True)}")
		else:
			print("No GPS fix")
		time.sleep(0.2)

except KeyboardInterrupt:
	print("Ctrl^C pressed, exiting...")
	exit()
