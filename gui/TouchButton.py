#!/usr/bin/python3

############################################################
# pi-cardash: gui/TouchButton.py
# Written by: Ryan Phillip Bayne (rpb288), Tyman Sin (ts835)
# Depends on: colors.py, TextBox.py
############################################################

### Import modules
import pygame

### Import project modules
from .colors import WHITE, RED
from .TextBox import TextBox

### TouchButton: a class to hold GUI elements for a touch button, child class of TextBox
class TouchButton(TextBox):
	# Create a TouchButton instance
	def __init__(self, text:str, width:int=100, height:int=40, color=RED, textcolor=WHITE, fontsize:int=25):
		super().__init__(text, width, height, color, textcolor, fontsize)
		self.__box_rect = None

	# Inherits text method form TextBox

	# Inherits update_text method from TextBox

	# Draw the button either centered at (x, y) or top-left at (x, y) and save its position
	def draw(self, screen: pygame.Surface, x:int, y:int, centered:bool=True):
		super().draw(screen, x, y, centered)

		# Save the last drawn position of the button (used to detect presses)
		if centered:
			self.__box_rect = self._box.get_rect(center=(x, y))
		else:
			self.__box_rect = self._box.get_rect(topleft=(x, y))

	# Indicates whether the button is pressed with the given coordinates, uses the button's last drawn position
	def pressed(self, pos) -> bool:
		pressed = False

		# Check if the position collides with the last drawn bounding box
		if self.__box_rect:
			pressed = self.__box_rect.collidepoint(pos)

		return pressed 
