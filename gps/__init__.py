#!/usr/bin/python3

############################################################
# pi-cardash: gps module
# Written by: Ryan Phillip Bayne (rpb288), Tyman Sin (ts835)
# Depends on: map.py
############################################################

### Define Constants
# Screen Size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT

### Import modules
import gpsd

### Import classes
from .Map import Map

### Define functions
def get_lat_lon():
	packet = gpsd.get_current()
	return packet.position()

### Initialize gpsd
gpsd.connect()

