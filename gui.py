#!/usr/bin/python3

############################################################
# Final Project 2020: gui.py
# Written by: Ryan Phillip Bayne (rpb288), Tyman Sin (ts835)
############################################################

import os
import time
import pygame
from pygame.locals import *
import RPi.GPIO as GPIO

# Set timeout
start_time = time.time()
timeout = 30

# Set up GPIO pin
pin_num = [17,22,23,5,6,27]

GPIO.setmode(GPIO.BCM) # Set for broadcom numbering, not board numbers
for i in pin_num:
    GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Callback function to quit the program
def left_clock_cb(channel):
    print("Left motor clockwise")
    drive('left', 'clockwise', False)
    left_entries.insert(0, ('Clockwise', time.time()-start_time))

def left_counter_cb(channel):
    print("Left motor counterclockwise")
    drive('left', 'counterclockwise', False)
    left_entries.insert(0, ('Counterclockwise', time.time()-start_time))

def left_stop_cb(channel):
    print("Left motor stopped")
    drive('left', '', True)
    left_entries.insert(0, ('Stop', time.time()-start_time))

def right_clock_cb(channel):
    print("Right motor clockwise")
    drive('right', 'clockwise', False)
    right_entries.insert(0, ('Clockwise', time.time()-start_time))

def right_counter_cb(channel):
    print("Right motor counterclockwise")
    drive('right', 'counterclockwise', False)
    right_entries.insert(0, ('Counterclockwise', time.time()-start_time))

def right_stop_cb(channel):
    print("Right motor stopped")
    drive('right', '', True)
    right_entries.insert(0, ('Stop', time.time()-start_time))

# Set callback
GPIO.add_event_detect(pin_num[0], GPIO.FALLING, callback=left_clock_cb, bouncetime=300)
GPIO.add_event_detect(pin_num[1], GPIO.FALLING, callback=left_counter_cb, bouncetime=300)
GPIO.add_event_detect(pin_num[2], GPIO.FALLING, callback=left_stop_cb, bouncetime=300)
GPIO.add_event_detect(pin_num[3], GPIO.FALLING, callback=right_clock_cb, bouncetime=300)
GPIO.add_event_detect(pin_num[4], GPIO.FALLING, callback=right_counter_cb, bouncetime=300)
GPIO.add_event_detect(pin_num[5], GPIO.FALLING, callback=right_stop_cb, bouncetime=300)

# Set environment variables
#os.putenv("SDL_VIDEODRIVER", "fbcon")
#os.putenv("SDL_FBDEV", "/dev/fb1")
#os.putenv("SDL_MOUSEDRV", "TSLIB")
#os.putenv("SDL_MOUSEDEV", "/dev/input/touchscreen")


# Initialize pygame
pygame.init()
#pygame.mouse.set_visible(True)

# Pygame setup
BLACK = 0,0,0
WHITE = 255,255,255
RED = 255,0,0
GREEN = 0,255,0
size = width, height = 320, 240
width = 320
height = 240
big_font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 25)

menu_coord = {'Status': (20,30), 'GPS': (90,30), 'DashCam': (210, 30), 'Time': (300,30)}
status_coord = {'Engine Temp': (width/4, height/4), 'RPM': (width/2, height/4), 'Air Intake': (3*width/4, height/4)}
menu_entries = ['Status', 'GPS', 'DashCam', 'Time']
status_entries = ['Engine Temp', 'RPM', 'Air Intake']

menu_rects = []
#right_rects = []

screen = pygame.display.set_mode(size)
#draw the background rect for the menu bar
#rect = (left, top, width, heigh)
menuRect = (0,240,320,240)
pygame.draw.rect(screen,GREEN,menuRect)

#background rects for the status screen
tempRect = (width/4, 2*height/3, 20, height/3)
mafRect = (3*width/4, 2*height/3, 20, height/3)

#blit the menu text to the screen and store the rect to check for touch input later
#for i in range (0, 3):
#    text_surface = small_font.render(menu_entries[i], True, WHITE)
#    key = f"log{i+1}"
#    rect = text_surface.get_rect(center=menu_coord[key])
#    screen.blit(text_surface, rect)
#    menu_rects.append(rect)

status_text = small_font.render(menu_entries[0], True, WHITE)
status_rect = status_text.get_rect(center=menu_coord['Status'])
screen.blit(status_text, status_rect)
menu_rects.append(status_rect)

gps_text = small_font.render(menu_entries[1],True, WHITE)
gps_rect = gps_text.get_rect(center=menu_coord['GPS'])
menu_rects.append(gps_rect)

cam_text = small_font.render(menu_entries[2], True, WHITE)
cam_rect = cam_text.get_rect(center=menu_coord['DashCam'])
menu_rects.append(cam_rect)

time_text = small_font.render(menu_entries[3], True, WHITE)
time_rect = time_text.get_rect(center=menu_coord['Time'])
menu_rects.append(time_rect)

quit_text = small_font.render("QUIT", True, WHITE)
quit_rect = quit_text.get_rect(center=(160,200))
screen.blit(quit_text, quit_rect)

pygame.display.flip()
#tab variables - status tab is default on boot
status_tab = False
GPS_tab = False
dash_tab = False
try:
    # animation loop
    while True:
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONUP):
                print("getting pos")
                pos = pygame.mouse.get_pos()
                #if the quit button is pressed quit the program
                if quit_rect.collidepoint(pos):
                    print("Quitting...")
                    GPIO.cleanup()
                    exit()
                #if a menu button has been pressed change what is               blit
                #the first rect is for the status page
                elif menu_rects[0].collidepoint(pos):
                    print("Status Tab tapped")
                    i=0
                    GPS_tab = False
                    dash_tab = False
                    status_tab = True
                #the second rect is for the GPS tab
                elif menu_rects[1].collidepoint(pos):
                    print("GPS Tab tapped")
                    dash_tab = False
                    status_tab = False
                    GPS_tab = True
                elif menu_rects[2].collidepoint(pos):
                    print("Dashcam Tab tapped")
                    status_tab = False
                    GPS_tab = False
                    dash_tab = True
        # redraw stuff
        screen.fill(BLACK)

        if status_tab:
            #draw RPM background circle
            pygame.draw.circle(screen, RED, (width/2,height/2), 40)
            #draw temp background rectangle
            pygame.draw.rect(screen, WHITE, tempRect, 1)
            #draw the MAF background rectangle
            pygame.draw.rect(screen, WHITE, tempRect, 1)

            #simulate changing temp
            if 1<30:
                i= i+1
                tempDataRect = (width/4,height/2-height/3,20,i)
                pygame.draw.rect(screen,GREEN,tempDataRect)
                #if i=30:
                #    i = 0
        elif GPS_tab:
            pygame.draw.circle(screen, WHITE, (160,120), 40)
        elif dash_tab:
            pygame.draw.circle(screen, GREEN, (160,120), 40)
        
        
        screen.blit(status_text, status_rect)
        screen.blit(gps_text, gps_rect)
        screen.blit(cam_text, cam_rect)
        screen.blit(time_text, time_rect)
        screen.blit(quit_text, quit_rect)
        pygame.display.flip()

except KeyboardInterrupt:
    print("Ctrl^C pressed, exiting...")
    GPIO.cleanup()
    exit()

GPIO.cleanup()
