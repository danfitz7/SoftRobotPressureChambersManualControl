# -*- coding: utf-8 -*-
"""
Soft Robot mecode
Version 3
Daniel Fitzgerald, Harvard lewis Research Group
07/17/2014

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
from PrintingGlobals import init_G, g

init_G(r"H:\User Files\Fitzgerald\SoftRobots\SoftRobotV1\gcode\SoftRobotFourActuatorsV2.pgm")
PrintingGlobals.g.write(start_script_string)

def print_robot():
    
    # PRINT_SPECIFIC PARAMETERS
    MACHINE_ZERO = -58.36 #zero on the top of the left ecoflex layer
    MACHINE_ZERO_RIGHT = -58.273 #the top of the left ecoflex layer
    right_side_offset = MACHINE_ZERO_RIGHT-MACHINE_ZERO # added to the print height of the right actuators
                    
    # mold parameters
    mold_z_zero_abs = 0     # absolute zero of the top of the mold
    mold_center_x = 53.5    # x coordinate of the center of the robot, relative to mold top left corner
    mold_front_leg_row_y = - 13  # y cooredinate of the center of the front/foreward actuators, relative to mold top left corner
    mold_back_leg_row_y = -34
    mold_actuator_z_bottom_abs = mold_z_zero_abs - 1.5 # relative to top of mold
#    mold_actuator_z_top = 0 #mold_z_zero_abs - 1 # relative top top of mold (expected)
    mold_depth = 7.62
    mold_body_width = 25.4
    mold_body_length = 65.2
    mold_head_y = -4.9
    
    # travel
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
 
    ## control lines
    control_line_height_abs = mold_z_zero_abs - mold_depth/2.0
    control_line_bridge_height_abs = control_line_height_abs + 2
    control_line_x_dist_from_center_line = (1.0/6.0)*mold_body_width
    control_line_A_x = mold_center_x - control_line_x_dist_from_center_line
    control_line_B_x = mold_center_x + control_line_x_dist_from_center_line
 
    ################ START PRINTING ################
    
    # set the current X and Y as the origin of the current work coordinates
    PrintingGlobals.g.absolute()
    PrintingGlobals.g.write("POSOFFSET CLEAR A ; clear all position offsets and work coordinates.") 
    PrintingGlobals.g.feed(default_travel_speed)
    move_z_abs(MACHINE_ZERO+default_travel_height_abs)
    PrintingGlobals.g.write("\nG92 X0 Y0 "+default_z_axis+str(default_travel_height_abs)+" ; set the current position as the absolute work coordinate zero origin")
    PrintingGlobals.g.feed(default_travel_speed)
    travel_mode()
    PrintingGlobals.g.write(" ; ready to print")
#    PrintingGlobals.g.abs_move(x=0,y=0,**{default_z_axis:0})
    
    ################ Valves ################
    abdomen_length = 41.5
    n_valves = 4
    abdomen_clearence = 4
    abdomen_offset = -1
    valve_separation_y = (abdomen_length-2*abdomen_clearence)/(n_valves+1.0)
    valve_flow_connection = 3
    valve_control_connection = 3
    valve_print_height = control_line_height_abs -0.39 #this is the pad_z_separation from the print_valve function
    valve_flow_height = valve_print_height + 0.39 
    valve_y_positions = [mold_head_y - mold_body_length + abdomen_offset+abdomen_clearence+(n_valves-n)*valve_separation_y for n in range(n_valves)]
#    print "Valve Y Positions: " + str(valve_y_positions)
    valve_x = mold_center_x
    valve_angle = np.pi*0.5
    valve_connection_dwell_time = 2 # when connecting to the valve flowstems, dwell for this long to make a good blob junction
#    travel_mode(whipe_distance=0)
    
    #print ALL  the valves
    PrintingGlobals.g.write(" ; PPRINT FOUR VALVES\n")
    for valve_y in valve_y_positions:
        PrintingGlobals.g.abs_move(x=valve_x, y = valve_y)
        print_valve(flow_connection_x = valve_flow_connection, control_connection_y = valve_control_connection, print_height_abs=valve_print_height, theta=valve_angle)
    PrintingGlobals.g.write(" ; DONE PRININGT FOUR VALVES\n")
    valve_flow_connection_gopast_distance = 1
    valve_connection_turn_offset = 1
    
    #connect the flow lines of the front two valves together, then to control line A
    PrintingGlobals.g.abs_move(x=valve_x+valve_flow_connection, y=valve_y_positions[1]) # go over the flow connector of the back valve
    print_mode(print_height_abs = valve_flow_height)
    PrintingGlobals.g.dwell(valve_connection_dwell_time)
    PrintingGlobals.g.abs_move(y=valve_y_positions[0])
    PrintingGlobals.g.dwell(valve_connection_dwell_time)
    PrintingGlobals.g.abs_move(y=valve_y_positions[0]+valve_flow_connection_gopast_distance) #go past the connection point a little before turning
    PrintingGlobals.g.abs_move(y=valve_y_positions[0]+valve_control_connection+valve_connection_turn_offset) # valve_control_connection+
    PrintingGlobals.g.abs_move(y=mold_back_leg_row_y+abdomen_offset, x=control_line_A_x)
    ################ Control Lines and Actuators ################
    
    #print control line A
#    travel_mode(whipe_distance=0)
    PrintingGlobals.g.abs_move(x=control_line_A_x, y = mold_back_leg_row_y)
#    print_mode(print_height_abs = control_line_height_abs)
    PrintingGlobals.g.abs_move(y = mold_front_leg_row_y)
            
    #print the top left actuator (A1) directly from the end of  control line A
    PrintingGlobals.g.abs_move(x=left_actuators_interconnects_x)
    move_z_abs(actuator_print_height)
    print_left_actuator()
    
    # Connect the flow lines of the back two valves together, then to control line B
    PrintingGlobals.g.abs_move(x=valve_x+valve_flow_connection, y=valve_y_positions[3]) #Start at the back valve flow line
    print_mode(print_height_abs = valve_flow_height)
    PrintingGlobals.g.dwell(valve_connection_dwell_time)
    PrintingGlobals.g.abs_move(y=valve_y_positions[2]) # Connect to the second-to-back valve flow line
    PrintingGlobals.g.dwell(valve_connection_dwell_time) # dwell for good connnection
    PrintingGlobals.g.abs_move(y=valve_y_positions[2]+valve_flow_connection_gopast_distance) # go past the connection point a little before turning, to not "tear" the connection
    PrintingGlobals.g.abs_move(x = valve_x+valve_flow_connection + 2, y = valve_y_positions[2]+2+valve_flow_connection_gopast_distance) # turn diagonally so we don't hit the flow conneciton line for the first two valves
    PrintingGlobals.g.abs_move(y=valve_y_positions[0]+valve_control_connection+valve_connection_turn_offset) # valve_control_connection+  #go foreward the the first valve y position
    PrintingGlobals.g.abs_move(y=mold_back_leg_row_y+abdomen_offset, x=control_line_B_x) # align with control line B so we can go straight in Y for a bit before printing it (turn point isn't a z-connection point)
    
    #print control line B
    PrintingGlobals.g.abs_move(x=control_line_B_x, y = mold_back_leg_row_y)
#    print_mode(print_height_abs = control_line_height_abs)
    PrintingGlobals.g.abs_move(y = mold_front_leg_row_y)
    
    #print actuator B1 (top right) directly from end of control line B
    PrintingGlobals.g.abs_move(x=right_actuators_interconnects_x)
    move_z_abs(actuator_print_height)
    print_right_actuator()
    
    def print_mode_control_line_B():
        print_mode(print_height_abs = control_line_height_abs, whipe_distance = 1, whipe_angle = np.pi)
    
    def print_mode_control_line_A():
        print_mode(print_height_abs = control_line_height_abs, whipe_distance = 1, whipe_angle = 0)
        
    #print actuator A3 (second from top, right) bridging over control line B
    PrintingGlobals.g.abs_move(x=control_line_A_x, y=mold_front_leg_row_y - 1*actuator_separation_y)
    print_mode_control_line_A()
    move_z_abs(control_line_bridge_height_abs)
    PrintingGlobals.g.feed(default_print_speed)
    PrintingGlobals.g.abs_move(right_actuators_interconnects_x)
    print_right_actuator()
    
    #print actuator B3 (second from top, left) going around the control line of A3
    PrintingGlobals.g.abs_move(x=control_line_B_x, y=mold_front_leg_row_y - 1.5*actuator_separation_y)
    print_mode_control_line_B()
    move_z_abs(control_line_bridge_height_abs)
    PrintingGlobals.g.feed(default_print_speed)
    PrintingGlobals.g.abs_move(x=left_actuators_interconnects_x)
    PrintingGlobals.g.abs_move(y=mold_front_leg_row_y - 1.0*actuator_separation_y)
    print_left_actuator()
    
    ##print actuator A2 (second from bottom, left)
    PrintingGlobals.g.abs_move(x=control_line_A_x, y = mold_front_leg_row_y - 2*actuator_separation_y)
    print_mode_control_line_A()
    PrintingGlobals.g.abs_move(x=left_actuators_interconnects_x)
    print_left_actuator()
    
    #print actuator B2 (second from bottom, right)
    PrintingGlobals.g.abs_move(x=control_line_B_x, y = mold_front_leg_row_y - 2*actuator_separation_y)
    print_mode_control_line_B()
    PrintingGlobals.g.abs_move(x=right_actuators_interconnects_x)
    print_right_actuator()
    
    #print actuator B4 (bottom, left) bridging over control line A
    PrintingGlobals.g.abs_move(x=control_line_B_x, y = mold_front_leg_row_y - 3*actuator_separation_y)
    print_mode_control_line_B()
    move_z_abs(control_line_bridge_height_abs)
    PrintingGlobals.g.feed(default_print_speed)
    PrintingGlobals.g.abs_move(x=left_actuators_interconnects_x)
    print_left_actuator()
        
    #print actuator A4 (bottom right) going around the control line of B4
    PrintingGlobals.g.abs_move(x=control_line_A_x, y = mold_front_leg_row_y - 2.5*actuator_separation_y)
    print_mode_control_line_A()
    move_z_abs(control_line_bridge_height_abs)
    PrintingGlobals.g.feed(default_print_speed)
    PrintingGlobals.g.abs_move(x=right_actuators_interconnects_x)
    PrintingGlobals.g.abs_move(y=mold_front_leg_row_y - 3*actuator_separation_y)
    print_right_actuator()

    #go back to home
    PrintingGlobals.g.abs_move(x=0,y=0,**{default_z_axis:default_travel_height_abs})

#main program
print_robot()     

#print (PrintingGlobals.g.get_bounding_box())

PrintingGlobals.g.write(end_script_string)                            
PrintingGlobals.g.view()
PrintingGlobals.g.teardown()