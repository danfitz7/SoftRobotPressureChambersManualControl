import numpy as np

from MatrixPrinting import *
from PrintingGlobals import *

def print_actuator(print_height_abs, pressure=85, com_port=9, theta=0, travel_speed = default_travel_speed):
    """Prints a soft actuator with the stem starting in the current position and rotated by theta. Assume nozzle is already at the correct height"""
    global g                         
                                                    
    # stems
    stem_print_speed = 1.5
    stem_length =  4+8 # distance to the edge of the mold body +length of the "shoulder-elbow" segment
    pad_separation_stem_length = 4
    
    #pad
    pad_length = 2.6 # length in Y
    pad_width = 2.6 # width in x
    n_meanders = 8
    default_pad_print_speecd = 4.5
    pad_print_speed = default_pad_print_speecd * 0.75
    meander_separation_dist = pad_length/n_meanders
    
    def print_actuator_pad():
        PrintingGlobals.g.feed(pad_print_speed)
        move_x(-pad_width/2, theta) #move to the lower left corner of the pad
        for meander in range(n_meanders-1):
            move_xy(x_distance=pad_width, y_distance=meander_separation_dist,theta=theta)        # horizontal across the whole pad
            move_x(-pad_width,theta)
        move_xy(x_distance=pad_width, y_distance=meander_separation_dist,theta=theta)    
        move_x(-pad_width/2, theta)           # move to the middle of the top of the pad
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    print_mode(print_height_abs = print_height_abs,print_speed = stem_print_speed)
    
    PrintingGlobals.g.relative()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    #print stem to actuator pad 1
    move_y(stem_length, theta)
    
    #print actuator pad 1
    print_actuator_pad()
    
    #print connection stem to actuator pad 2
    PrintingGlobals.g.feed(stem_print_speed)
    move_y(pad_separation_stem_length, theta)
    
    #print actuator pad 2
    print_actuator_pad()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
    travel_mode(whipe_angle = theta+np.pi/2)
    PrintingGlobals.g.absolute()