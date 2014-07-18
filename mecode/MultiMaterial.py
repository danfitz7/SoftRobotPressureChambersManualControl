# -*- coding: utf-8 -*-
from MatrixPrinting import *
from PrintingGlobals import *

strTools = ["A","B","C","D"]
cur_tool_index = 0
def setStrTool(index, strNewName):
    strTools[index]=strNewName

def change_tool(to_tool_index):
    global cur_tool_index
    global g
    from_tool  = strTools[cur_tool_index]
    cur_tool = strTools[to_tool_index]
    PrintingGlobals.g.write("; Change Tools from " + from_tool + " to " + cur_tool + ".")
    PrintingGlobals.g.write("G1 X(($" + cur_tool + "x-$" + from_tool + "x-($" + cur_tool + "x_dif-$" + from_tool + "x_dif))) F" + str(default_travel_speed))
    PrintingGlobals.g.write("G1 Y(($" + from_tool + "y-$" + cur_tool + "y+($" + from_tool + "y_dif-$" + cur_tool + "y_dif)))")
    cur_tool_index = to_tool_index

multiNozzle_start_code = """
;########### Variables For Functions ########################

DVAR $comport
DVAR $found, $floor $delta $deltafast $Ax $Ay $Bx $By $Cx $Cy $Dx $Dy $Px $Py $posA $posB $posC $posD $posZ $fastfeed $midfeed $slowfeed $Astart $Bstart $Cstart $Dstart $Pstart $comma1 $comma2 $comma1plus $comma2plus
DVAR $Ax_dif $Ay_dif $Bx_dif $By_dif $Cx_dif $Cy_dif $Dx_dif $Dy_dif $Px_dif $Py_dif $zo_ref $nozzles $set_home $reference_nozzle 
DVAR $nozzle $nozzleA $nozzleB $nozzleC $nozzleD $profilometerRod $xStart $yStart $zStart 
DVAR $zMeasureA $zMeasureB $zMeasureC $zMeasureD $Az_dif $Bz_dif $Cz_dif $Dz_dif $xOffset $yOffset
DVAR $zA $zB $zC $zD $check
DVAR $zSweepRange $zSweepStep $numsteps $tempdistance $zDwell $count $z_dif $z_past $z_num $indicator $step $start $x_dist
DVAR $align_save
DVAR $comma1 $comma2 $comma3 $comma4 $comma1plus $comma2plus $comma3plus $comma1min $comma3min $alignment_file

;########### Duel Material Pressure ########################
DVAR $COM 
DVAR $COM2
DVAR $linepressure1 ; Pressure in PSI
DVAR $linepressure2 ; Pressure in PSI

;########### ??? very important ??? ########################
DVAR $heighta
DVAR $heightb
DVAR $heightc
DVAR $heightd

"""

multiNozzle_start_code_2 = """
$DO0.0=0
$DO1.0=0
$DO2.0=0
$DO3.0=0
Call togglePress P$COM  ; Turns on/off pressure box for A

; Below, we call several required GCode commands; these commands begin with a G:
G71            ; Standard GCode command for metric units
G76            ; Standard GCode command for time base seconds
G68            
G65 F3000        ; Sets an acceleration speed in mm/s^2
G66 F3000        ; Sets a deceleration speed in mm/s^2

; The “ENABLE” command allows us to enable axes on the printer; this is required for printing
ENABLE X Y A B C D U     ; enables all the axis 


Incremental                ; “Incremental” tells the printer to referring to relative coordinates


;############### User Code################################
"""


multi_nozzle_end_code = """
;#############################################################################
;################ Setup ########################
POSOFFSET CLEAR X Y U A B C D
FILECLOSE
;################################################################################

; ###########function calls ##########
;call recall_alignment Q1
; Q1 means recall allignment value for nozzle A

;call calc_relative_z Q1
; Q1 means nozzle A is reference nozzle, and $zo_ref was set for the zero of nozzle A

;call save_value Q1
; Q1 means you are saving the alignment values for nozzle A

;call NozzleChange Q12 R1
; Q12 means change from nozzle 1 to nozzle 2 ; R1 means reset home to zero R0 means don't

;call alignZeroNozzle L=Nozzle Q=startheight R=2nd_sweep_increment I=absolute_floor J= 1st_sweep_increment
;call alignZeroNozzle L1 Q-15 R0.1 I-49.25 J=0.85

Call setPress P$COM Q$linepressure1 ; Calls the box and sets pressure for A
call recall_alignment Q1
call recall_alignment Q2
call recall_alignment Q3
call recall_alignment Q4

call alignZeroNozzle L1 Q-15 R0.1 I-49.25 J=0.85 ; Uncomment when you need to align axis A. 
call alignZeroNozzle L2 Q-15 R0.1 I-49.25 J=0.85 ; Uncomment when you need to align axis B.
;call alignZeroNozzle L3 Q-15 R0.1 I-49.25 J=0.85
;call alignZeroNozzle L4 Q-15 R0.1 I-49.25 J=0.85

call save_value_aerotech Q1
call save_value_aerotech Q2
call save_value_aerotech Q3
call save_value_aerotech Q4

call calc_relative_z Q1
call set_z_home
MSGDISPLAY 1 "Ax_dif: " + $Ax_dif
MSGDISPLAY 1 "Ay_dif: " + $Ay_dif
MSGDISPLAY 1 "Az_dif: " + $Az_dif
MSGDISPLAY 1 "zMeasure A: " + $zMeasureA

MSGDISPLAY 1 "Bx_dif: " + $Bx_dif
MSGDISPLAY 1 "By_dif: " + $By_dif
MSGDISPLAY 1 "Bz_dif: " + $Bz_dif
MSGDISPLAY 1 "zMeasure B: " + $zMeasureB

MSGDISPLAY 1 "Cx_dif: " + $Cx_dif
MSGDISPLAY 1 "Cy_dif: " + $Cy_dif
MSGDISPLAY 1 "Cz_dif: " + $Cz_dif
MSGDISPLAY 1 "zMeasure C: " + $zMeasureC

MSGDISPLAY 1 "Dx_dif: " + $Dx_dif
MSGDISPLAY 1 "Dy_dif: " + $Dy_dif
MSGDISPLAY 1 "Dz_dif: " + $Dz_dif
MSGDISPLAY 1 "zMeasure D: " + $zMeasureD
$heighta = .26 ; layer1
$heightb = .390 ; layer2
$heightc = .525 ; layer3
$heightd = .710 ; layer4 
"""

