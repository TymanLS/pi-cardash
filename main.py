#!/usr/bin/python3

############################################################
# pi-cardash: main.py
# Written by: Ryan Phillip Bayne (rpb288), Tyman Sin (ts835)
# Depends on: gui module
############################################################

timeout = 60

############################
# Setup and Initialization #
############################

### Import modules
import time
import pygame
from pygame.locals import MOUSEBUTTONUP

### Import project modules
import gui
import carstat
#TODO: import dashcam
#TODO: import gps

### Initialize pygame
pygame.init()
screen = pygame.display.set_mode(gui.SCREEN_SIZE)
#pygame.mouse.set_visible(False)


#######################
# Define GUI Elements #
#######################

### Menu Bar

# Background Rect
menuRect = (0, 0, gui.SCREEN_WIDTH, 40)

# Tabs
status = gui.TouchButton("Status", width=gui.SCREEN_WIDTH//4 - 2, height=40, color=gui.colors.BEIGE)
gps = gui.TouchButton("GPS", width=gui.SCREEN_WIDTH//4 - 2, height=40, color=gui.colors.BEIGE)
dashcam = gui.TouchButton("Dashcam", width=gui.SCREEN_WIDTH//4 - 1, height=40, color=gui.colors.BEIGE)
clock = gui.TextBox("Clock", width=gui.SCREEN_WIDTH//4 - 2, height=40)
menuTabs = [status, gps, dashcam, clock]

# Tab coordinates
menuCoords = [(0, 0), (gui.SCREEN_WIDTH//4, 0), (gui.SCREEN_WIDTH//2, 0), (3*gui.SCREEN_WIDTH//4 + 2, 0)]

# Buttons (used for event handling)
menuButtons = [status, gps, dashcam]


### Status Tab

# Gauges
rpm = gui.RpmGauge(redline=6000)
coolant_temp = gui.BarGauge("Coolant Temperature", unit="degC", val_range=(-10, 120), safe_range=(10,85))
maf = gui.BarGauge("Mass Airflow Intake", unit="g/s", safe_range=(0, 600))
statusGauges = [rpm, coolant_temp, maf]

# Gauge Coordinates
statusCoords = [(512, 300), (200, 300), (824, 300)]

# CarStat
obdCommands = {carstat.commands.RPM, carstat.commands.COOLANT_TEMP, carstat.commands.MAF}
car = carstat.CarStat(obdCommands)
car.start()

### GPS Tab


### Dashcam Tab


### Quit Button
quit_button = gui.TouchButton("Quit")



##################
# Animation Loop #
##################

count = 0
start_time = time.time()
currentTab = status

try:
	while time.time() - start_time < timeout:
		time.sleep(0.002)

		# Handle events
		for event in pygame.event.get():
			if(event.type is MOUSEBUTTONUP):
				pos = pygame.mouse.get_pos()
				for tab in menuButtons:
					if tab.pressed(pos):
						print(f"Switching to {tab.text} tab")
						currentTab = tab
				if quit_button.pressed(pos):
					car.stop()
					pygame.quit()
					exit()

		# Update values
		rpm.update(car.query(carstat.commands.RPM))
		coolant_temp.update(car.query(carstat.commands.COOLANT_TEMP))
		maf.update(car.query(carstat.commands.MAF))
		count+=1

		### Redraw screen
		# Black out the screen
		screen.fill(gui.colors.BLACK)
		
		# Draw menu bar
		pygame.draw.rect(screen, gui.colors.GRAY, menuRect)
		for tab in range(0, len(menuTabs)):
			menuTabs[tab].draw(screen, menuCoords[tab][0], menuCoords[tab][1], centered=False)

		# Draw Status tab
		if currentTab is status:
			for gauge in range(0, len(statusGauges)):
				statusGauges[gauge].draw(screen, statusCoords[gauge][0], statusCoords[gauge][1])

		# Draw GPS tab
		elif currentTab is gps:
			pass

		# Draw Dashcam tab
		elif currentTab is dashcam:
			pass

		# Draw quit button
		quit_button.draw(screen, 512, 500)

		# Update display
		pygame.display.flip()
		
except KeyboardInterrupt:
	car.stop
	pygame.quit()
	exit()
