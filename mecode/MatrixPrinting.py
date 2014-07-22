# -*- coding: utf-8 -*-
"""
MatrixPrinting.py
Daniel Fitzgerald, Harvard Lewis Research Group
07/21/2014

This library contains global default variables and functions for general 3D Matrix printing on the momacaster.
These include default feeds, speeds, travel heighs, line pressures, and associated functions.
"""

# -*- coding: utf-8 -*-

import numpy as np

from mecode import G
import PrintingGlobals

# DEFAULT PRINTING PARAMETERS
default_line_pressure = 85  # default nozzle pressure in psi
default_com_port = 9        # com port for efd pressure box
default_start_stop_dwell_time = 0.2 # ink hysteresis compensation. Dwell for this long after starting extrusion but before moving, and after stopping but before stopping extrusion
default_travel_speed = 20 # travel speed in air (movement above the mold)
default_matrix_travel_speed = 0.5 # speed to travel in matrix (used for traveling vertically)
#default_matrix_print_speed = 0.25
default_mold_top_abs = 1 #relative to ecoflex= zero
default_travel_height_abs = default_mold_top_abs+3 # height above the work zero (ecoflex top) to travel in air
default_print_speed = 1.5
default_z_axis = ("A" if PrintingGlobals.Aerotech else "z")

# Pressure control Macros
pressure_on = False
def turn_pressure_off(com_port = default_com_port, start_stop_dwell_time = default_start_stop_dwell_time):
    global pressure_on
    if (pressure_on):
        PrintingGlobals.g.toggle_pressure(com_port)
        PrintingGlobals.g.dwell(start_stop_dwell_time)
        pressure_on = False

def turn_pressure_on(com_port = default_com_port, start_stop_dwell_time = default_start_stop_dwell_time):
    global pressure_on
    if (not pressure_on):
        PrintingGlobals.g.dwell(start_stop_dwell_time)
        PrintingGlobals.g.toggle_pressure(com_port)
        pressure_on = True

def move_z_abs(height, z_axis = default_z_axis, vertical_travel_speed = default_matrix_travel_speed):
    """Move the given z axis in work absolute coordinates"""
    global ng
    cur_pos = PrintingGlobals.g.get_current_position()
    prev_speeds=default_travel_speed
    if (cur_pos):
        prev_speeds = cur_pos[3]
        PrintingGlobals.g.feed(vertical_travel_speed)
    if ((not cur_pos) or (cur_pos[2] != height)):
        PrintingGlobals.g.abs_move(**{z_axis:height})

    #TODO: fixme
    if (type(prev_speeds) != type(0)):
        PrintingGlobals.g.feed(prev_speeds[1])
    else:
        PrintingGlobals.g.feed(prev_speeds)

def travel_mode(travel_speed = default_travel_speed, travel_height_abs = default_travel_height_abs, whipe_distance=0, whipe_angle=0):
    """"Stop Extrusion, move to travel height"""
    global g
    turn_pressure_off()
    PrintingGlobals.g.dwell(default_start_stop_dwell_time)
    move_z_abs(travel_height_abs)  
    PrintingGlobals.g.feed(travel_speed)

    
def print_mode(print_height_abs, travel_speed = default_travel_speed, print_speed = default_print_speed, whipe_distance=0, whipe_angle=0):
    """Move to print height, start Extrusion"""
    global g
    PrintingGlobals.g.feed(travel_speed)

    #go down to to mold zero if neccisary
    if (PrintingGlobals.g.get_current_position()[2]>default_mold_top_abs):
        move_z_abs(default_mold_top_abs, vertical_travel_speed=travel_speed)
        
    #go the rest of the way in the default_matrix_travel_speed
    move_z_abs(print_height_abs)
    
    #start extrusion
    turn_pressure_on()
    PrintingGlobals.g.dwell(default_start_stop_dwell_time)

    #return with the print_speed being used
    PrintingGlobals.g.feed(print_speed)
  
def move_x(distance, theta=0):
    global g
    if (distance!=0):
        PrintingGlobals.g.move(x=np.cos(theta)*distance, y=np.sin(theta)*distance)        
     
def move_y(distance, theta=0):
    global g
    if (distance!=0):
        PrintingGlobals.g.move(x=-np.sin(theta)*distance, y=np.cos(theta)*distance)                     
 
def move_xy(x_distance, y_distance, theta=0):
    global g
    C=np.cos(theta)
    S=np.sin(theta)
    if (x_distance!=0 and y_distance!=0):
        PrintingGlobals.g.move(x=x_distance*C-y_distance*S, y=x_distance*S+y_distance*C)