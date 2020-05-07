#!/usr/bin/python3

############################################################
# pi-cardash: gps/map.py
# Written by: Ryan Phillip Bayne (rpb288), Tyman Sin (ts835)
#
############################################################

### Import modules
import os
import pygame
from gui import SCREEN_WIDTH
from gui import SCREEN_HEIGHT

### Set the assets directory
ASSET_DIR = os.path.join(os.path.dirname(__file__), 'assets/')

### Map: a class to hold GUI elements for GPS map
class Map:

    #class variables
    #__map_background_image = pygame.image.load(os.path.join(ASSET_DIR, 'map1.png'))

    def __init__(self,image:str,max_lat:float,min_lat:float,max_long:float,min_long:float):
        self.__image = pygame.image.load(os.path.join(ASSET_DIR, image))
        self.__max_lat = max_lat
        self.__min_lat = min_lat
        self.__max_long = max_long
        self.__min_long = min_long

    @property
    def max_long(self):
        return self.__max_long
    
    @property
    def min_long(self):
        return self.__min_long
    
    @property
    def max_lat(self):
        return self.__max_lat
    
    @property
    def min_lat(self):
        return self.__min_lat

    
    # Draw on the specified Surface either centered at (x, y) or top-left corner at (x, y)
    def draw(self, screen:pygame.Surface, x:int, y:int, centered:bool=True):
                
                # Draw the RPM background image
                screen.blit(self.__image,(x,y))
