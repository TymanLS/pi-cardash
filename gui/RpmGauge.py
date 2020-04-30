#!/usr/bin/python3

############################################################
# pi-cardash: gui/RpmGauge.py
# Written by: Ryan Phillip Bayne (rpb288), Tyman Sin (ts835)
# Depends on: colors.py
############################################################

### Import modules
import os
import pygame

### Import project modules
from .colors import WHITE, RED

### Set the assets directory
ASSET_DIR = os.path.join(os.path.dirname(__file__), 'assets/')

### RpmGauge: a class to hold GUI elements for RPM gauges
class RpmGauge:
	# Class variables
	__rpm_gauge_image = pygame.image.load(os.path.join(ASSET_DIR, 'rpmBackground.png'))
	__min_rpm = 0
	__max_rpm = 8000
	__min_angle = 55 
	__max_angle = 305

	# Create an RpmGauge instance
	def __init__(self, radius:int=128, rpm:int=0, redline:int=6000):
		# Set instance variables
		self.__radius = radius
		self.__rpm = rpm
		self.__redline = redline
		self.__gauge = pygame.transform.scale(self.__rpm_gauge_image, (int(radius*2), int(radius*2))) # Scale the RPM background image to the radius
		self.__needle = pygame.Surface((radius // 32, radius), pygame.SRCALPHA) # Create the surface for the RPM needle
		self.__needle.fill(RED) # Make the RPM needle red
		self.__needle.set_alpha(0) # Set an alpha value so transform does not add padding
		self.__needle_angle = self.__max_angle

	@property
	def radius(self):
		return self.__radius

	@property
	def rpm(self):
		return self.__rpm

	@property
	def redline(self):
		return self.__redline

	# Update the RPM value and recalculate the needle angle
	def update(self, rpm: int):
		self.__rpm = rpm
		self.__needle_angle = RpmGauge.__update_needle_angle(self)

	# Calculate the needle angle
	@staticmethod
	def __update_needle_angle(gauge):
		if gauge.__rpm < RpmGauge.__min_rpm:
			return RpmGauge.__max_angle
		elif gauge.__rpm > RpmGauge.__max_rpm:
			return RpmGauge.__min_angle
		else:
			return int(RpmGauge.__max_angle - (gauge.__rpm * ((RpmGauge.__max_angle - RpmGauge.__min_angle)/(RpmGauge.__max_rpm - RpmGauge.__min_rpm))))

	# Draw the RPM gauge on the specified Surface either centered at (x, y) or top-left corner at (x, y)
	def draw(self, screen:pygame.Surface, x:int, y:int, centered:bool=True):
		if not centered:
			x += self.__radius
			y += self.__radius
		
		# Draw the RPM background image
		screen.blit(self.__gauge, (x - self.__radius, y - self.__radius))

		# Draw the RPM needle
		rot_needle = pygame.transform.rotate(self.__needle, self.__needle_angle)
		if self.__needle_angle > 90 and self.__needle_angle <= 180:
			screen.blit(rot_needle, (x, y - rot_needle.get_height()))
		elif self.__needle_angle > 180 and self.__needle_angle <= 270:
			screen.blit(rot_needle, (x - rot_needle.get_width(), y - rot_needle.get_height()))
		elif self.__needle_angle > 270 and self.__needle_angle <= 360:
			screen.blit(rot_needle, (x - rot_needle.get_width(), y))
		else:
			screen.blit(rot_needle, (x, y))

		# Draw the RPM text
		if self.__rpm > self.__redline:
			text_surface = pygame.font.Font(None, 25).render(f"RPM: {self.__rpm}", True, RED)
		else:
			text_surface = pygame.font.Font(None, 25).render(f"RPM: {self.__rpm}", True, WHITE)
		text_surface = pygame.transform.rotozoom(text_surface, 0, self.__radius * (1/128))
		rect = text_surface.get_rect(center=(x, y + self.__radius//2)) 
		screen.blit(text_surface, rect)
