#!/usr/bin/python3

############################################################
# pi-cardash: main.py
# Written by: Ryan Phillip Bayne (rpb288), Tyman Sin (ts835)
# Depends on: gui module
############################################################

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
import dashcam
import gps

### Initialize pygame
pygame.init()
screen = pygame.display.set_mode(gui.SCREEN_SIZE)
pygame.mouse.set_visible(False)



#######################
# Define GUI Elements #
#######################

### Menu Bar

# Background Rect
menuRect = (0, 0, gui.SCREEN_WIDTH, 40)

# Tabs
status_tab = gui.TouchButton("Status", width=gui.SCREEN_WIDTH//4 - 2, height=40, color=gui.colors.BEIGE)
gps_tab = gui.TouchButton("GPS", width=gui.SCREEN_WIDTH//4 - 2, height=40, color=gui.colors.BEIGE)
dashcam_tab = gui.TouchButton("Dashcam", width=gui.SCREEN_WIDTH//4 - 1, height=40, color=gui.colors.BEIGE)
clock_tab = gui.TextBox("Clock", width=gui.SCREEN_WIDTH//4 - 2, height=40)
menuTabs = [status_tab, gps_tab, dashcam_tab, clock_tab]

# Tab coordinates
menuCoords = [(0, 0), (gui.SCREEN_WIDTH//4, 0), (gui.SCREEN_WIDTH//2, 0), (3*gui.SCREEN_WIDTH//4 + 2, 0)]

# Buttons (used for event handling)
menuButtons = [status_tab, gps_tab, dashcam_tab]


### Status Tab

# Gauges
rpm_gauge = gui.RpmGauge(redline=6000)
coolant_temp_gauge = gui.BarGauge("Coolant Temperature", unit="degC", val_range=(-10, 120), safe_range=(10,85))
maf_gauge = gui.BarGauge("Mass Airflow Intake", unit="g/s", val_range=(0,30), safe_range=(0, 20))
statusGauges = [rpm_gauge, coolant_temp_gauge, maf_gauge]

# Gauge Coordinates
statusCoords = [(512, 300), (200, 300), (824, 300)]

# CarStat
obdCommands = {carstat.commands.RPM, carstat.commands.COOLANT_TEMP, carstat.commands.MAF}
car = carstat.CarStat(obdCommands)
car.start()


### GPS Tab
min_long = -111.9087
max_long = -111.8209
max_lat = 33.2752
min_lat = 33.2352
map_height = 560
map_width = 1024
Map = gps.Map(image='Map.png',max_lat=33.2752,min_lat=33.2352,max_long=-111.8209,min_long=-111.9087)

### Dashcam Tab

# Camera
cam = dashcam.Dashcam()
camCoords = (20, 40)
record_button = gui.TouchButton("Record", width=160, height=40, color=gui.colors.GREEN)
stop_button = gui.TouchButton("Stop", width=160, height=40, color = gui.colors.RED)
camButtons = [record_button, stop_button]
camButtonCoords= [(920, 80),(920, 160)]



##################
# Animation Loop #
##################

recording = False
currentTab = status_tab
lon = 0.0
lat = 0.0

try:
	while True:
		time.sleep(0.002)

		### Handle events
		for event in pygame.event.get():
			if(event.type is MOUSEBUTTONUP):
				pos = pygame.mouse.get_pos()

				# Tab buttons
				for tab in menuButtons:
					if tab.pressed(pos):
						print(f"Switching to {tab.text} tab")
						currentTab = tab
						if tab is dashcam_tab:
							cam.show(camCoords[0], camCoords[1])
						else:
							cam.hide()

				# Dashcam buttons
				for button in camButtons:
					if currentTab is dashcam_tab:
						if button.pressed(pos):
							print(f"{button.text} pressed")
							if button is record_button and not recording:
								recording = True
								cam.record()
							elif button is stop_button and recording:
								cam.stop()
								recording = False


		### Update values
		rpm_gauge.update(car.query(carstat.commands.RPM))
		coolant_temp_gauge.update(car.query(carstat.commands.COOLANT_TEMP))
		maf_gauge.update(round(car.query(carstat.commands.MAF), 2))
		lat, lon = gps.get_lat_lon()
		now = gps.get_time()
		clock_tab.update_text(f"{now.date().isoformat()}  {now.time().isoformat()}")


		### Redraw screen
		# Black out the screen
		screen.fill(gui.colors.BLACK)
                
		# Draw menu bar
		pygame.draw.rect(screen, gui.colors.GRAY, menuRect)
		for tab in range(0, len(menuTabs)):
			menuTabs[tab].draw(screen, menuCoords[tab][0], menuCoords[tab][1], centered=False)

		# Draw Status tab
		if currentTab is status_tab:
			for gauge in range(0, len(statusGauges)):
				statusGauges[gauge].draw(screen, statusCoords[gauge][0], statusCoords[gauge][1])

		# Draw GPS tab
		elif currentTab is gps_tab:
			Map.draw(screen,0,40)
			x=(map_width/(min_long-max_long))*(min_long - lon)
			y=(map_height/(max_lat-min_lat))*(max_lat-lat) + 40
			pygame.draw.circle(screen, gui.colors.RED, (int(x),int(y)),5)

		# Draw Dashcam tab
		elif currentTab is dashcam_tab:
			if not recording:
				camButtons[0].draw(screen, camButtonCoords[0][0], camButtonCoords[0][1]) 
			elif recording:
				camButtons[1].draw(screen, camButtonCoords[1][0], camButtonCoords[1][1]) 
				pygame.draw.circle(screen, gui.colors.RED,(920,80),20)

		# Update display
		pygame.display.flip()
                
except KeyboardInterrupt:
        if recording:
            cam.stop()
        car.stop()
        pygame.quit()
        exit()
