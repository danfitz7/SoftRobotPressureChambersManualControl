
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

g.abs_move(x=-10,y=0)
print_valve(print_height_abs=0,theta = 0)

g.move(x=-10,y=10)
print_valve(print_height_abs=0,theta = 0, control_stem_corner=False)

g.move(x=-10, y=20)
print_valve(print_height_abs=0,theta = 0, control_connection_y = 0.1, control_stem_corner=False)

g.move(x=-10, y=30)
print_valve(print_height_abs=0,theta = 0, flow_inlet=False)

g.move(x=-10, y=40)
print_valve(print_height_abs=0,theta = 0, flow_inlet=False, control_inlet=False)


g.move(x=-10, y=50)
print_valve(print_height_abs=0,theta = 0, x_mirror=False, control_stem_corner=False, flow_inlet=False)

g.move(x=-10, y=60)
print_valve(print_height_abs=0,theta = 0, x_mirror=True, control_stem_corner=False, flow_inlet=False)

g.view()
g.teardown()
