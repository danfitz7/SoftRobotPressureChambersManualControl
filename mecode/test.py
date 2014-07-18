
# -*- coding: utf-8 -*-
from mecode import G
from math import sqrt

import numpy as np
import matplotlib.pyplot as plt

#Soft robot printing libraries
from Robomama import *
from MatrixPrinting import *
from QuakeValve import *
from Actuators import *
from PrintingGlobals import *
from PressureChambers import *

g=init_G(r"H:\User Files\Fitzgerald\SoftRobots\SoftRobotPressureChambersManualControl\gcode\TEST.pgm")

g.absolute()
g.abs_move(x=0,y=0)
travel_mode()
g.abs_move(x=-10,y=10)

print_valve(print_height_abs=0,theta = 0, control_stem_corner=False, flow_inlet=False)

g.move(y=10)
print_valve(print_height_abs=0,theta = 0, control_stem_corner=True)


g.view()
g.teardown()
