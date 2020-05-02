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
#TODO: import carstat
import dashcam
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
maf_gauge = gui.BarGauge("Mass Airflow Intake", unit="g/s", safe_range=(0, 600))
statusGauges = [rpm_gauge, coolant_temp_gauge, maf_gauge]

# Gauge Coordinates
statusCoords = [(512, 300), (200, 300), (824, 300)]


### GPS Tab


### Dashcam Tab

# Camera
cam = dashcam.Dashcam()
camCoords = (100, 220)
record_button = gui.TouchButton("Record", width=160, height=40, color=gui.colors.GREEN)
stop_button = gui.TouchButton("Stop", width=160, height=40, color = gui.colors.RED)
camButtons = [record_button, stop_button]
camButtonCoords= [(920, 80),(920, 160)]


### Quit Button
quit_button = gui.TouchButton("Quit")



##################
# Animation Loop #
##################

count = 0
start_time = time.time()
currentTab = status_tab

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
                                                if tab is dashcam_tab:
                                                    recording = False
                                                    cam.show(camCoords[0], camCoords[1])
                                                    print("In the camera if statement")
                                                else:
                                                    cam.hide()
                                for button in camButtons:
                                        if button.pressed(pos):
                                            print(f"{button.text} pressed")
                                            if button is record_button:
                                                recording = True
                                                print("recording started")
                                                cam.record()
                                                pygame.draw.circle(screen, gui.colors.RED,(920,80),20)
                                            elif button is stop_button:
                                                cam.stop()
                                                recording = False
                                                print("recording var= ",recording)
                                if quit_button.pressed(pos):
                                    if recording:
                                        cam.stop()
                                    pygame.quit()
                                    exit()

                # Update values
                rpm_gauge.update(count)
                coolant_temp_gauge.update(int(count/50))
                maf_gauge.update(count)
                count+=1

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
                        pass

                # Draw Dashcam tab
                elif currentTab is dashcam_tab:
                    if not recording:
                        camButtons[0].draw(screen, camButtonCoords[0][0], camButtonCoords[0][1]) 
                    elif recording:
                        camButtons[1].draw(screen, camButtonCoords[1][0], camButtonCoords[1][1]) 
                        pygame.draw.circle(screen, gui.colors.RED,(920,80),20)

                # Draw quit button
                quit_button.draw(screen, 512, 500)

                # Update display
                pygame.display.flip()
                
except KeyboardInterrupt:
        pygame.quit()
        exit()
