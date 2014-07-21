import numpy as np

from MatrixPrinting import *
from MultiMaterial import *
import PrintingGlobals

default_pressure_chamber_length = 5
default_speed = 0.5
default_total_pressure_chamber_inlet_length = 5

def print_pressure_chamber(print_height_abs, theta=0, travel_speed = default_travel_speed, length = default_pressure_chamber_length, inlet_total_length = default_total_pressure_chamber_inlet_length, speed = default_speed):
    """Print a Pressure chamber below the current travel position, with the given orientation and length"""
    
    """Overall connection geometry is as follows: 
        front flow connector = (0,length+default_inlet_length)
        back flow connector = (0,0)

        
        y
        
        ^
        |
        +-> x
        
        Theta=0
        
        Front Flow connector
        
              .
              |
              []  
              |
         y=0  I
        
        Back Flow Inlet
        
    """
    global g
        
    #inlets
    stem_print_speed = default_print_speed
    inlet_print_speed = 0.5
    inlet_needle_length = 3
    inlet_stem_length = inlet_total_length - inlet_needle_length
    
    def print_inlet():
        """Print an inlet going down, ending at the needle tip"""
        PrintingGlobals.g.feed(inlet_print_speed)
        move_y(-inlet_needle_length, theta)
        PrintingGlobals.g.feed(stem_print_speed)
        move_y(-inlet_stem_length, theta)

    #good connections
    extra_tip_length = 0.5
    connection_dwell_time = 1
    
    PrintingGlobals.g.relative()

    move_y(inlet_total_length-extra_tip_length) #move past the inlet to start of pressure chamber

    # switch extruders, print the presure chamber channel
    change_tool(1)
    
    #print_mode(print_height_abs=print_height_abs, print_speed = speed)
    PrintingGlobals.g.feed(default_travel_speed)
    PrintingGlobals.g.abs_move(**{cur_tool:print_height_abs})
    turn_pressure_on()
    PrintingGlobals.g.dwell(default_start_stop_dwell_time)
    PrintingGlobals.g.feed(speed)
    
    
    # PRINT THE CHAMBER
    PrintingGlobals.g.dwell(connection_dwell_time)
    move_y(length+2*extra_tip_length, theta)
    PrintingGlobals.g.dwell(connection_dwell_time)
    
    #travel_mode()
    turn_pressure_off()
    PrintingGlobals.g.feed(default_matrix_travel_speed)
    PrintingGlobals.g.abs_move(**{cur_tool:default_travel_height_abs})
    PrintingGlobals.g.feed(default_travel_speed)
            
    change_tool(0)
    
    #go over the end of the bottom inlet (non-needle end)
    move_y(-length-extra_tip_length, theta)
                            
    #print the bottom inlet down, ending at the tip where the needle is inserted
    print_mode(print_height_abs=print_height_abs)
    PrintingGlobals.g.dwell(connection_dwell_time)
    print_inlet()
    PrintingGlobals.g.dwell(connection_dwell_time)
    travel_mode()