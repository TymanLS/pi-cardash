#!/usr/bin/python3

############################################################
# pi-cardash: gui/TextBox.py
# Written by: Ryan Phillip Bayne (rpb288), Tyman Sin (ts835)
# Depends on: colors.py
############################################################

### Import modules
import pygame

### Import project modules
from .colors import GRAY, WHITE

### TextBox: a class to hold GUI elements for a text box
class TextBox:
	# Create a TextBox instance
	def __init__(self, text:str, width:int=100, height:int=40, color=GRAY, textcolor=WHITE, fontsize:int=25):
		self.__text = text
		self._box = pygame.Surface((width, height))
		self.__color = color
		self.__textcolor = textcolor
		self.__fontsize = fontsize
		self._box.fill(self.__color)
		self._text_surface = pygame.font.Font(None, self.__fontsize).render(self.__text, True, self.__textcolor)

	@property
	def text(self):
		return self.__text

	# Update the text in the TextBox
	def update_text(self, text, textcolor=None, fontsize:int=None):
		# Update text data
		self.__text = text

		# Update text color (if provided)
		if textcolor:
			self.__textcolor = textcolor

		# Update font size (if provided
		if fontsize:
			self.__fontsize = fontsize

		# Re-render the text surface
		self._text_surface = pygame.font.Font(None, self.__fontsize).render(self.__text, True, self.__textcolor)

	# Draw the TextBox either centered at (x, y) or top-left corner at (x, y)
	def draw(self, screen: pygame.Surface, x: int, y: int, centered:bool=True):
		if not centered:
			x += self._box.get_width()//2
			y += self._box.get_height()//2

		# Draw the text and the bounding box
		screen.blit(self._box, self._box.get_rect(center=(x, y)))
		screen.blit(self._text_surface, (x - self._text_surface.get_width()//2, y - self._text_surface.get_height()//2))
