# -*- coding: utf-8 -*-
"""
Soft Robot mecode
Version 3
Daniel Fitzgerald, Harvard lewis Research Group
07/21/2014

This version includes two pressure chambers which power actuator channels A and B through two valves.
Functions for valves, actuators, and pressure chambers have also been moves to seperate files, as has standard matrix printing functionality and the starting and ending G Code for robomama.
"""

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

#init_G from PrintingGlobals.py
g=init_G(r"H:\User Files\Fitzgerald\SoftRobots\SoftRobotPressureChambersManualControl\gcode\SoftRobotPressureChambersManualControl.pgm")


def print_robot():
    global g

    # PRINT_SPECIFIC PARAMETERS
    MACHINE_ZERO = -58 #-58.36 #zero on the top of the left ecoflex layer
    MACHINE_ZERO_RIGHT = -58#-58.273 #the top of the left ecoflex layer
    right_side_offset = MACHINE_ZERO_RIGHT-MACHINE_ZERO # added to the print height of the right actuators
    #Absolute Machine Coordinates of the top left corner of the mold
    MOLD_MACHINE_X = 367.67
    MOLD_MACHINE_Y = 180.034
                                   
    # mold parameters
    mold_z_zero_abs = 0     # absolute zero of the top of the mold
    mold_center_x = 53.5    # x coordinate of the center of the robot, relative to mold top left corner
    mold_front_leg_row_y = - 13  # y cooredinate of the center of the front/foreward actuators, relative to mold top left corner
    mold_back_leg_row_y = -34 # Y coordiante of the centerline of the back legs/actuators
    mold_depth = 7.62 # total depth of the body of the robot
    mold_body_width = 25.4 # width of the body of the robot
    mold_body_length = 65.2 #length of the body of the robot
    mold_head_y = -4.9 # y coordinate of the tip of the head of the robot
    
    # travel height above the mold
    travel_height_abs = mold_z_zero_abs + 5
    
    # needle inlet connections in the abdomen
    inlet_length = 2
    inlet_print_speed = 0.5
    inlet_distance_from_edge = 4 
    
    #actuators 
    n_actuator_rows=4
    actuator_print_height_offset = 0.1 # nozzle height above ecoflex
    actuator_print_height = mold_z_zero_abs + actuator_print_height_offset
    actuator_separation_y = 7 #distance between the "legs"    actuator_z_connect_inset = 5
    actuator_z_connect_inset = 5
    left_actuators_interconnects_x = mold_center_x - mold_body_width/2 + actuator_z_connect_inset
    right_actuators_interconnects_x = mold_center_x + mold_body_width/2 - actuator_z_connect_inset
    
    def print_right_actuator():
        print_actuator(theta = 1.5*np.pi, print_height_abs = actuator_print_height+right_side_offset)
    
    def print_left_actuator():
        print_actuator(theta = 0.5*np.pi, print_height_abs = actuator_print_height)
 
    # control lines
    control_line_height_abs = mold_z_zero_abs - mold_depth/2.0 # height of control line channels A and B
    control_line_bridge_height_abs = control_line_height_abs + 2 # height to bridge over the control lines
    control_line_x_dist_from_center_line = (1.0/6.0)*mold_body_width # distance control lines A and B are from the centerline of the robot (to the left and right respectivly)
    control_line_A_x = mold_center_x - control_line_x_dist_from_center_line
    control_line_B_x = mold_center_x + control_line_x_dist_from_center_line
 
    ################ START PRINTING ################
    
    # Print headers and Aerotech appeasement
    g.write(multiNozzle_start_code)
    g.write("$zo_ref  = "+str(MACHINE_ZERO)) # set the $zo_ref as the reference zero for axis homing (why does homing/offsets need a reference?)
    g.write(multiNozzle_homing_code) # comment this to not home axis
    g.write(multiNozzle_start_code_2)
    
    # set the current X and Y as the origin of the current work coordinates
    g.absolute()     
    
    # go to our absolute work zero (mold top left corner)
    g.write("POSOFFSET CLEAR A ; clear all position offsets and work coordinates.") #We should start in machine coordinates because the homing routine clears all position offsets, but clear them again anyway just incase
    g.feed(default_travel_speed)
    g.abs_move(x=MOLD_MACHINE_X, y=MOLD_MACHINE_Y)  
    move_z_abs(default_travel_height_abs) #MACHINE_ZERO+
    
    # set this current mold zero as the work zero (set clearany current position offsets
#    move_z_abs(MACHINE_ZERO+default_travel_height_abs)
    g.write("\nG92 X0 Y0 "+default_z_axis+str(default_travel_height_abs)+" ; set the current position as the absolute work coordinate zero origin")
    g.feed(default_travel_speed)
    #travel_mode()
    g.write(" ; READY TO PRINT")

    ################ Valves ################
    abdomen_length = 41.5
    control_line_start_y = mold_back_leg_row_y -2
    valve_separation_dist = 02 #distance from the back legs to the valves
    valve_flow_connection = 3
    valve_control_connection = 1
    valve_print_height = control_line_height_abs -0.39 #this is the pad_z_separation from the print_valve function
    valve_flow_height = valve_print_height + 0.39 
    valve_y = control_line_start_y - valve_flow_connection - valve_separation_dist
    valve_x_distance = 1.5 #distance from the center of the body to the valve is center
    valve_angle = np.pi
    valve_connection_dwell_time = 2 # when connecting to the valve flowstems, dwell for this long to make a good blob junction
    
    right_valve_x = mold_center_x+valve_x_distance 
    left_valve_x = mold_center_x-valve_x_distance
        
    # pressure chambers    
    pressure_chamber_separation_distance = 2
    pressure_chamber_front_y = valve_y-valve_flow_connection-pressure_chamber_separation_distance
                                                        
    #print the left pressure chamber
    g.abs_move(control_line_A_x, y=valve_y-valve_flow_connection-default_total_pressure_chamber_inlet_length-default_pressure_chamber_length-pressure_chamber_separation_distance)
    print_pressure_chamber(print_height_abs=control_line_height_abs)

    #print left valve
    g.abs_move(x=left_valve_x, y = valve_y)
    print_valve(flow_connection_x = valve_flow_connection, control_connection_y = valve_control_connection, print_height_abs=valve_print_height, theta=valve_angle, control_stem_corner=False, flow_inlet=False)

    #connect the left pressure chamber to the bottom flow line of the right valve
    g.abs_move(x=control_line_A_x, y = pressure_chamber_front_y)
    print_mode(print_height_abs = valve_flow_height)
    g.abs_move(x=left_valve_x,y=valve_y-valve_flow_connection)
    travel_mode()        
                        
    #print control line A (left side)
    g.abs_move(left_valve_x, valve_y+valve_flow_connection) #go over the top flow line of the left valve
    print_mode(print_height_abs = valve_flow_height) #connect to flow line
    g.dwell(valve_connection_dwell_time)
    g.abs_move(x=control_line_A_x, y = control_line_start_y, z=control_line_height_abs) # print just below the flow control A start
    g.abs_move(y = mold_front_leg_row_y) #move up to flow line A
            
    #print the top left actuator (A1) directly from the end of  control line A
    g.abs_move(x=left_actuators_interconnects_x)
    move_z_abs(actuator_print_height)
    print_left_actuator()
    
    #print the right pressure chamber
    g.abs_move(control_line_B_x, y=pressure_chamber_front_y-default_total_pressure_chamber_inlet_length-default_pressure_chamber_length)
    print_pressure_chamber(print_height_abs=control_line_height_abs)
    
    #connect the right pressure chamber to the bottom flow line of the right valve
    g.abs_move(x=control_line_B_x, y = pressure_chamber_front_y)
    print_mode(print_height_abs = valve_flow_height)
    g.abs_move(x=right_valve_x,y=valve_y-valve_flow_connection)
    travel_mode()
    
    #print right valve
    g.abs_move(x=right_valve_x,y=valve_y)
    print_valve(flow_connection_x = valve_flow_connection, control_connection_y = valve_control_connection, print_height_abs=valve_print_height, x_mirror=True, theta=valve_angle, control_stem_corner=False, flow_inlet=False)
    
    #print control line B (right side)
    g.abs_move(x=right_valve_x, y=valve_y+valve_flow_connection) #move over the top flow connector of the right valve
    print_mode(print_height_abs = valve_flow_height) #connect to flow line
    g.dwell(valve_connection_dwell_time)
    g.abs_move(x=control_line_B_x, y = control_line_start_y, z=control_line_height_abs)
    g.abs_move(y = mold_front_leg_row_y)
    
    #print actuator B1 (top right) directly from end of control line B
    g.abs_move(x=right_actuators_interconnects_x)
    move_z_abs(actuator_print_height)
    print_right_actuator()
    
    
    #Print the rest of the actuators off of the control lines
    
    def print_mode_control_line_B():
        print_mode(print_height_abs = control_line_height_abs, whipe_distance = 1, whipe_angle = np.pi)
    
    def print_mode_control_line_A():
        print_mode(print_height_abs = control_line_height_abs, whipe_distance = 1, whipe_angle = 0)
        
    #print actuator A3 (second from top, right) bridging over control line B
    g.abs_move(x=control_line_A_x, y=mold_front_leg_row_y - 1*actuator_separation_y)
    print_mode_control_line_A()
    move_z_abs(control_line_bridge_height_abs)
    g.feed(default_print_speed)
    g.abs_move(right_actuators_interconnects_x)
    print_right_actuator()
    
    #print actuator B3 (second from top, left) going around the control line of A3
    g.abs_move(x=control_line_B_x, y=mold_front_leg_row_y - 1.5*actuator_separation_y)
    print_mode_control_line_B()
    move_z_abs(control_line_bridge_height_abs)
    g.feed(default_print_speed)
    g.abs_move(x=left_actuators_interconnects_x)
    g.abs_move(y=mold_front_leg_row_y - 1.0*actuator_separation_y)
    print_left_actuator()
    
    ##print actuator A2 (second from bottom, left)
    g.abs_move(x=control_line_A_x, y = mold_front_leg_row_y - 2*actuator_separation_y)
    print_mode_control_line_A()
    g.abs_move(x=left_actuators_interconnects_x)
    print_left_actuator()
    
    #print actuator B2 (second from bottom, right)
    g.abs_move(x=control_line_B_x, y = mold_front_leg_row_y - 2*actuator_separation_y)
    print_mode_control_line_B()
    g.abs_move(x=right_actuators_interconnects_x)
    print_right_actuator()
    
    #print actuator B4 (bottom, left) bridging over control line A
    g.abs_move(x=control_line_B_x, y = mold_front_leg_row_y - 3*actuator_separation_y)
    print_mode_control_line_B()
    move_z_abs(control_line_bridge_height_abs)
    g.feed(default_print_speed)
    g.abs_move(x=left_actuators_interconnects_x)
    print_left_actuator()
        
    #print actuator A4 (bottom right) going around the control line of B4
    g.abs_move(x=control_line_A_x, y = mold_front_leg_row_y - 2.5*actuator_separation_y)
    print_mode_control_line_A()
    move_z_abs(control_line_bridge_height_abs)
    g.feed(default_print_speed)
    g.abs_move(x=right_actuators_interconnects_x)
    g.abs_move(y=mold_front_leg_row_y - 3*actuator_separation_y)
    print_right_actuator()

    #go back to home
    g.abs_move(x=0,y=0,**{default_z_axis:default_travel_height_abs})


    #Cleanup/Aerotech functions at the end
    #g.write(end_script_string)  
    g.write(multiNozzle_end_code)

#main program
print_robot()     

  
                        
g.view()
g.teardown()