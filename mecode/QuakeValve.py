import numpy as np

from MatrixPrinting import *
from PrintingGlobals import *

def print_valve(print_height_abs, theta=0, stem_print_speed = default_print_speed, flow_connection_x = 3, control_connection_y = 5, x_mirror=False, y_mirror=False, flow_inlet = True, control_inlet = True, control_stem_corner = True):
    """Prints a valve with the stem starting in the current position and rotated by theta. Assume nozzle is already at the correct height"""
    """Overall connection geometry is as follows: 
        back flow connector = (0,-3)
        front flow connector = (0,3)
        control line connector = (5,0)
        
        y
        
        ^
        |
        +-> x
        
        Theta=0
        
        Top Flow Inlet
        
            I  I    
            |  |    Control Inlet
            E--*     
            |
            
        
        Bottom Flow Inlet
        
        or, if control_stem_corner=False,
        
            I
            |
            E--*--H Control inlet
            |
            
        
        Tthe flow inlet (I) will be absent if flow_inlet=False
        
        The control inlet (I or H) will be absent if control_inlet=False   
                    
        """
    
    global g
    
    #mirror and transforms
    x_mirror = (-1 if x_mirror else 1)
    y_mirror = (-1 if y_mirror else 1)
    
    # stems
    stem_print_speed = 1.5
    inlet_print_speed = 0.5
    inlet_stem_length = 2
    inlet_needle_length = 3
    inlet_total_length = inlet_stem_length+inlet_needle_length
    def print_inlet(_theta=theta):
        PrintingGlobals.g.feed(stem_print_speed)
        move_y(inlet_stem_length, _theta)
        PrintingGlobals.g.feed(inlet_print_speed)
        move_y(inlet_needle_length, _theta)
    
    #general
    pad_z_separation = 0.2+0.19
    junction_dist = 1.0
    
    #control pads
    control_pad_width = 2 # width in Y
    control_pad_meander_separation = 0.35
    control_pad_n_meanders = 5
    control_pad_length = control_pad_n_meanders*control_pad_meander_separation # length in X
    control_pad_print_speed = 1
    control_pad_stem_length = control_connection_y - 0.5*control_pad_length
        
    # flow pad
    flow_pad_n_meanders = 8
    flow_pad_meander_separation = 0.175
    flow_pad_length = flow_pad_meander_separation*flow_pad_n_meanders # length in Y
    flow_pad_width = 1.5 #width in X
    flow_stem_length = flow_connection_x-0.5*control_pad_width
    flow_pad_print_speed = 2

    #feeds
    stem_print_speed = 1.5
    #matrix_travel_speed = 2
    #pad_print_speed_1 = 1
    #pad_print_speed_2 = 4
     
    ##### START WRITING THE SCRIPT ####
    PrintingGlobals.g.write("\n\n; PRINT A VALVE rotation = " + str(theta) + ".")      
    
    #assume we start above the center of the pad
    PrintingGlobals.g.relative()
    
    #move from above the pad center to its lower corner
#    travel_mode() #assume we're already in travel mode
    move_xy(x_distance=x_mirror*(-control_pad_length/2.0), y_distance=y_mirror*(-control_pad_width/2.0),theta=theta)
    
    #print the bottom control pad, starting at the edge of the pad
    print_mode(print_height_abs=print_height_abs, print_speed = control_pad_print_speed)
    y_sign = 1
    n_meanders = int(control_pad_length/control_pad_meander_separation)
    for meander in range(n_meanders):
        move_y(y_mirror*(y_sign*control_pad_width), theta)
        move_x(x_mirror*(control_pad_meander_separation), theta)
        y_sign = -1*y_sign
    move_y(y_mirror*(y_sign*control_pad_width/2), theta)
    
    #print the stem from the bottom control pad
    PrintingGlobals.g.feed(stem_print_speed)
    move_x(x_mirror*(control_pad_stem_length), theta) #go to the right before corner to inlet
    
    #print the control stem inlet so it lines up with the flow inlet
    control_stem_alignement_distance = (flow_connection_x if control_stem_corner else 0)   #TODO: why does flow_connection_x=3 work?
    if (control_stem_corner):
        move_y(y_mirror*(control_stem_alignement_distance), theta)
    print_inlet(_theta=theta) #print the control inlet up
    
    #travel to the back (-y) interconect point of flow lines
    travel_mode(whipe_angle=theta+np.pi/2)
    move_xy(x_distance = x_mirror*(-control_pad_stem_length-control_pad_length/2.0), y_distance = y_mirror*(-inlet_total_length - flow_stem_length - 0.5*control_pad_width - control_stem_alignement_distance), theta=theta)
    print_mode(print_height_abs=print_height_abs+pad_z_separation)
        
    #bottom flow line
    PrintingGlobals.g.feed(stem_print_speed)
    move_y(y_mirror*(flow_stem_length+0.5*(control_pad_width-flow_pad_length)), theta)
    
    #flow pad
    n_meanders = int(flow_pad_length/flow_pad_meander_separation)
    x_sign = -1
    PrintingGlobals.g.feed(flow_pad_print_speed)
    move_x(distance=x_mirror*(flow_pad_width/2.0), theta=theta)
    for meander in range(n_meanders-1):
        move_y(y_mirror*(flow_pad_meander_separation),theta)
        move_x(x_mirror*(x_sign * flow_pad_width),theta)
        x_sign = -1*x_sign
    move_y(y_mirror*(flow_pad_meander_separation),theta)    
    move_x(x_mirror*(x_sign*(flow_pad_width/2.0)), theta)
    
    #top flow line
    PrintingGlobals.g.feed(stem_print_speed)
    move_y(y_mirror*(flow_stem_length+(control_pad_width-flow_pad_length)/2.0), theta)
    
    #flow inlet
    print_inlet()
    
    #travel over control pad junction
    travel_mode(whipe_angle=theta+np.pi)
    move_xy(x_distance=x_mirror*(junction_dist+0.5*control_pad_length), y_distance = y_mirror*(-inlet_total_length -flow_stem_length-(control_pad_width-flow_pad_length)/2.0-flow_pad_length/2.0), theta=theta)
    
    #print stem up to control top pad
    print_mode(print_height_abs=print_height_abs)
    PrintingGlobals.g.feed(default_matrix_print_speed)
    PrintingGlobals.g.move(**{default_z_axis:2*pad_z_separation})
    PrintingGlobals.g.feed(stem_print_speed)
    move_x(x_mirror*(-junction_dist), theta)
    # BUG TODO FIX ME: can;t move relative x y and z for connection from bottom stem to top control pad
    #move_xy(x_distance=-junction_dist, y_distance=0, z_distance=2*pad_z_separation, theta=theta)
#    move_x(-0.5*(control_pad_width-flow_pad_length), theta=theta)
    
    #print the top flow pad
    PrintingGlobals.g.feed(control_pad_print_speed)
    y_sign = 1
    n_meanders = int(control_pad_length/control_pad_meander_separation)
    move_y(y_mirror*(-control_pad_width/2.0), theta)
    move_x(x_mirror*(-control_pad_meander_separation), theta)
    for meander in range(n_meanders-1):
        move_y(y_mirror*(y_sign*control_pad_width), theta)
        move_x(x_mirror*(-control_pad_meander_separation), theta)
        y_sign = -1*y_sign
    move_y(y_mirror*(y_sign*control_pad_width), theta)
    travel_mode(whipe_angle=theta+1.0*np.pi)