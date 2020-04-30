#!/usr/bin/python3

############################################################
# pi-cardash: gui module
# Written by: Ryan Phillip Bayne (rpb288), Tyman Sin (ts835)
# Depends on: colors.py, TextBox.py, TouchButton.py,
#             RpmGauge.py, BarGauge.py
############################################################

### Define Constants
# Screen Size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT

### Import submodules
from . import colors

### Import classes
from .TextBox import TextBox
from .TouchButton import TouchButton
from .BarGauge import BarGauge
from .RpmGauge import RpmGauge
