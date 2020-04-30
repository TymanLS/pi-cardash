#!/usr/bin/python3

############################################################
# pi-cardash: gui/BarGauge.py
# Written by: Ryan Phillip Bayne (rpb288), Tyman Sin (ts835)
# Depends on: colors.py
############################################################

### Import modules
import pygame

### Import project modules
from .colors import WHITE, RED, GREEN, BLUE

### BarGauge: a class to hold GUI elements for bar gauges
class BarGauge:
	# Create a BarGauge instance
	def __init__(self, parameter:str, width:int=100, height:int=250, val=0, unit:str=None, val_range:tuple=(0, 1000), safe_range:tuple=None):
		self.__parameter = parameter
		self.__width = width # Does not include text elements
		self.__height = height # Does not include text elements
		self.__value = val
		self.__unit = unit
		self.__val_range = val_range
		self.__safe_range = safe_range
		self.__bar = self.__bar_height()
		self.__color = self.__bar_color()
		self.__param_surface = pygame.font.Font(None, 25).render(self.__parameter, True, WHITE)
		self.__val_surface = self.__render_val_surface()

	@property
	def value(self):
		return self.__value

	# Update the value and text surface, recalculate the height and color of the bar
	def update(self, val):
		self.__value = val
		self.__bar = self.__bar_height()
		self.__color = self.__bar_color()
		self.__val_surface = self.__render_val_surface()

	# Calculate the height of the bar
	def __bar_height(self):
		if self.__value > self.__val_range[1]:
			return self.__height
		elif self.__value < self.__val_range[0]:
			return 0
		else:
			return int(self.__height * (self.__value - self.__val_range[0]) / (self.__val_range[1] - self.__val_range[0]))

	# Calculate the color of the bar
	def __bar_color(self):
		color = GREEN
		if self.__safe_range:
			if self.__value > self.__safe_range[1]:
				factor = int(255 * (self.__value - self.__safe_range[1]) / (self.__val_range[1] - self.__safe_range[1]))
				color = (factor, 255 - factor, 0)
			elif self.__value < self.__safe_range[0]:
				factor = int(255 * (self.__value - self.__val_range[0]) / (self.__safe_range[0] - self.__val_range[0]))
				color = (0, factor, 255 - factor)
			if self.__value > self.__val_range[1]:
				color = RED
			if self.__value < self.__val_range[0]:
				color = BLUE
		return color

	# Render the text surface with the value and unit (if provided)
	def __render_val_surface(self):
		if self.__unit:
			return pygame.font.Font(None, 25).render(f"{self.__value} {self.__unit}", True, WHITE)
		else:
			return pygame.font.Font(None, 25).render(f"{self.__value}", True, WHITE)

	# Draw the bar gauge on the specified surface either centered at (x, y) or top-left corner at (x, y)
	def draw(self, screen:pygame.Surface, x:int, y:int, centered:bool=True):
		if not centered:
			x += self.__width//2
			y += self.__height//2

		# Render the text of the parameter name
		screen.blit(self.__param_surface, (x - self.__param_surface.get_width()//2, y - self.__param_surface.get_height() - self.__height//2))

		# Draw the rect of the border
		border_rect = (x - self.__width//2, y - self.__height//2, self.__width, self.__height)
		pygame.draw.rect(screen, WHITE, border_rect, 1)

		# Draw the rect of the bar
		value_rect = (x - self.__width//2, y + self.__height//2, self.__width, -self.__bar)
		pygame.draw.rect(screen, self.__color, value_rect)

		# Render the text of the value
		screen.blit(self.__val_surface, (x - self.__val_surface.get_width()//2, y + self.__val_surface.get_height() + self.__height//2))
