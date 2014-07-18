import numpy as np

from mecode import G
import PrintingGlobals

# DEFAULT PRINTING PARAMETERS
default_line_pressure = 85
default_com_port = 9
default_start_stop_dwell_time = 0.2
default_travel_speed = 20
default_matrix_travel_speed = 0.5 # speed to travel in matrix (used for traveling vertically)
default_matrix_print_speed = 0.25
default_mold_top_abs = 1 #relative to ecoflex
default_travel_height_abs = default_mold_top_abs+3
default_print_speed = 1.5
default_z_axis = "A"

#stems

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

# Printing Mode Macros
def move_z_abs(height, z_axis = default_z_axis, vertical_travel_speed = default_matrix_travel_speed):
    cur_pos = PrintingGlobals.g.get_current_position()
    prev_speeds=default_travel_speed
    if (cur_pos):
        prev_speeds = cur_pos[3]
        PrintingGlobals.g.feed(vertical_travel_speed)
    if ((not cur_pos) or (cur_pos[2] != height)):
        PrintingGlobals.g.abs_move(**{z_axis:height})

#TODO: fixme
    if (type(prev_speeds) != type(0)):
#        print "Prev speed: " + str(prev_speeds[1])
        PrintingGlobals.g.feed(prev_speeds[1])
    else:
        PrintingGlobals.g.feed(prev_speeds)
    
#def travel_mode(travel_speed = default_travel_speed, travel_height_abs = default_travel_height_abs):
#    """"Stop Extrusion, move to travel height"""
#    global g
#    turn_pressure_off()
#    PrintingGlobals.g.feed(travel_speed)
#    move_z_abs(travel_height_abs)

def travel_mode(travel_speed = default_travel_speed, travel_height_abs = default_travel_height_abs, whipe_distance=0, whipe_angle=0):
    """"Stop Extrusion, whipe, move to travel height, unwhipe"""
    turn_pressure_off()
    PrintingGlobals.g.dwell(default_start_stop_dwell_time)
    #PrintingGlobals.g.move(x=np.cos*
#    move_x(whipe_distance,whipe_angle)
    move_z_abs(travel_height_abs)  
    PrintingGlobals.g.feed(travel_speed)
#    move_x(whipe_distance,whipe_angle+np.pi)  

    
def print_mode(print_height_abs, travel_speed = default_travel_speed, print_speed = default_print_speed, whipe_distance=0, whipe_angle=0):
    """Move to print height, start Extrusion"""
    PrintingGlobals.g.feed(travel_speed)
#    move_x(whipe_distance,whipe_angle)
    
    #go down to to mold zero if neccisary
    if (PrintingGlobals.g.get_current_position()[2]>default_mold_top_abs):
        move_z_abs(default_mold_top_abs, vertical_travel_speed=travel_speed)
        
    #go the rest of the way in the default_matrix_travel_speed
    move_z_abs(print_height_abs)
    
    #start extrusion
    turn_pressure_on()
    PrintingGlobals.g.dwell(default_start_stop_dwell_time)
    
#    move_x(-whipe_distance,whipe_angle)

    #return with the print_speed being used
    PrintingGlobals.g.feed(print_speed)
  
def move_x(distance, theta=0):
    if (distance!=0):
        PrintingGlobals.g.move(x=np.cos(theta)*distance, y=np.sin(theta)*distance)        
     
def move_y(distance, theta=0):
    if (distance!=0):
        PrintingGlobals.g.move(x=-np.sin(theta)*distance, y=np.cos(theta)*distance)                     
 
def move_xy(x_distance, y_distance, theta=0):
    C=np.cos(theta)
    S=np.sin(theta)
    if (x_distance!=0 and y_distance!=0):
        PrintingGlobals.g.move(x=x_distance*C-y_distance*S, y=x_distance*S+y_distance*C)