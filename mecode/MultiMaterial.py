# -*- coding: utf-8 -*-
from MatrixPrinting import *
import PrintingGlobals

strTools = (["A","B","C","D"] if PrintingGlobals.Aerotech else ["z","z","z","z"])
cur_tool_index = 0
cur_tool = strTools[cur_tool_index]

def setStrTool(index, strNewName):
    strTools[index]=strNewName

def change_tool(to_tool_index):
    global cur_tool_index
    global cur_tool
    global g
    from_tool  = cur_tool #strTools[cur_tool_index]
    cur_tool = strTools[to_tool_index]
    PrintingGlobals.g.write("; Change Tools from " + from_tool + " to " + cur_tool + ".")
    PrintingGlobals.g.write("G1 X(($" + cur_tool + "x-$" + from_tool + "x-($" + cur_tool + "x_dif-$" + from_tool + "x_dif))) F" + str(default_travel_speed))
    PrintingGlobals.g.write("G1 Y(($" + from_tool + "y-$" + cur_tool + "y+($" + from_tool + "y_dif-$" + cur_tool + "y_dif)))")
    cur_tool_index = to_tool_index

multiNozzle_start_code = """
;########### Variables For Functions ########################
DVAR $hFile        
DVAR $cCheck
DVAR $press
DVAR $length
DVAR $lame  


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


multiNozzle_homing_code = """
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


multiNozzle_end_code = """
;################ Teardown ########################################
M2


;#######################################################################
;##################### FUNCTIONS!!!!!! Yay! ############################
;#######################################################################


DFS recall_alignment
	$nozzle = $Q
	$Ax = 586.075
	$Ay = 367.8285
	$Bx = 482.075
	$By = 367.8285
	$Cx = 378.075
	$Cy = 367.8285
	$Dx = (299.075 - 25) ; Added 25 mm to 299.075 because we shifted the holder
	$Dy = 367.8285



IF $nozzle = 1
    $alignment_file = FILEOPEN "C:\Users\Lewis Group\Desktop\Alignment\Aerotech Alignment Files\alignment_values_1_aerotech.txt", 1    
ENDIF
IF $nozzle = 2
    $alignment_file = FILEOPEN "C:\Users\Lewis Group\Desktop\Alignment\Aerotech Alignment Files\alignment_values_2_aerotech.txt", 1
ENDIF
IF $nozzle = 3
    $alignment_file = FILEOPEN "C:\Users\Lewis Group\Desktop\Alignment\Aerotech Alignment Files\alignment_values_3_aerotech.txt", 1
ENDIF
IF $nozzle = 4
    $alignment_file = FILEOPEN "C:\Users\Lewis Group\Desktop\Alignment\Aerotech Alignment Files\alignment_values_4_aerotech.txt", 1
ENDIF

 
FILEREAD $alignment_file, 0, $strglob[0], $strglob[1], $strglob[2], $strglob[3]
$comma1 = STRFIND($strglob0, ",", 0)
$comma1plus = $comma1 + 1 
$STRGLOB1 = STRMID ($STRGLOB0, $comma1plus, 80)
$comma2 = STRFIND($strglob1, ",", 1)
$comma2 = $comma1 + $comma2
$comma2plus = $comma2 + 2
$strglob2 = STRMID ($STRGLOB0 , $comma2plus , 80)
$comma3= STRFIND($strglob2, ",", 1)
$comma3= $comma3 + $comma2
$comma3plus = $comma3 + 3
$strglob3 = STRMID ($STRGLOB0, 0, $comma1)
$strglob4 = STRMID ($STRGLOB0, $comma1plus, $comma2)
$strglob5 = STRMID ($STRGLOB0, $comma2plus, $comma3)
$strglob6 = STRMID ($STRGLOB0, $comma3plus, 80)
IF $nozzle = 1
    $Ax_dif = STRTODBL($strglob3)
	$Ay_dif = STRTODBL($strglob4)
	$zMeasureA = STRTODBL($strglob5)
	$Az_dif = STRTODBL($strglob6)
ENDIF
IF $nozzle = 2
    $Bx_dif = STRTODBL($strglob3)
	$By_dif = STRTODBL($strglob4)
	$zMeasureB = STRTODBL($strglob5)
	$Bz_dif = STRTODBL($strglob6)
ENDIF
IF $nozzle = 3
    $Cx_dif = STRTODBL($strglob3)
	$Cy_dif = STRTODBL($strglob4)
	$zMeasureC = STRTODBL($strglob5)
	$Cz_dif = STRTODBL($strglob6)
ENDIF
IF $nozzle = 4
    $Dx_dif = STRTODBL($strglob3)
	$Dy_dif = STRTODBL($strglob4)
	$zMeasureD = STRTODBL($strglob5)
	$Dz_dif = STRTODBL($strglob6)
ENDIF

FILECLOSE $alignment_file

ENDDFS




; ----- Nozzle Change Function --------------------------------------

DFS NozzleChange

	
$nozzles = $Q
	
$set_home = $R
	
	
	
F40
	
IF $set_home = 1
		
G90
		
G1 A50 B50 C50 D50
		
G1 X0 Y0
		
G91
	
ENDIF    
    
    
dwell(0.25)
    
    
if $nozzles = 12
        
G90
	
G1 A=50
	
G91
        
G1 X($Bx-$Ax-($Bx_dif-$Ax_dif))  Y($Ay-$By+($Ay_dif-$By_dif))
    
else if $nozzles = 13
        
G90
	
G1 A=50
	
G91
        
G1 X($Cx-$Ax-($Cx_dif-$Ax_dif))  Y($Ay-$Cy+($Ay_dif-$Cy_dif))   
    
else if $nozzles = 14
        
G90
	
G1 A=50
	
G91
        
G1 X($Dx-$Ax-($Dx_dif-$Ax_dif))  Y($Ay-$Dy+($Ay_dif-$Dy_dif))
    
else if $nozzles = 21
        
G90
	
G1 B=50
	
G91
        
G1 X($Ax-$Bx-($Ax_dif-$Bx_dif))  Y($By-$Ay+($By_dif-$Ay_dif))  
    
else if $nozzles = 23
        
G90
	
G1 B=50
	
G91
        
G1 X($Cx-$Bx-($Cx_dif-$Bx_dif))  Y($By-$Cy+($By_dif-$Cy_dif))
    
else if $nozzles = 24
        
G90
	
G1 B=50
	G91
        
G1 X($Dx-$Bx-($Dx_dif-$Bx_dif))  Y($By-$Dy+($By_dif-$Dy_dif))
    
else if $nozzles = 31
        
G90
	
G1 C=50
	
G91
       
G1 X($Ax-$Cx-($Ax_dif-$Cx_dif))  Y($Cy-$Ay+($Cy_dif-$Ay_dif))
    
else if $nozzles = 32
        
G90
	
G1 C=50
	
G91
        
G1 X($Bx-$Cx-($Bx_dif-$Cx_dif))  Y($Cy-$By+($Cy_dif-$By_dif))
    
else if $nozzles = 34
        
G90
	
G1 C=50
	
G91
        
G1 X($Dx-$Cx-($Dx_dif-$Cx_dif))  Y($Cy-$Dy+($Cy_dif-$Dy_dif))
    
else if $nozzles = 41
        
G90
	
G1 D=50
	
G91
        
G1 X($Ax-$Dx-($Ax_dif-$Dx_dif))  Y($Dy-$Ay+($Dy_dif-$Ay_dif))
    
else if $nozzles = 42
        
G90
	
G1 D=50
	
G91
        
G1 X($Bx-$Dx-($Bx_dif-$Dx_dif))  Y($Dy-$By+($Dy_dif-$By_dif))
    
else if $nozzles = 43
        
G90
	
G1 D=50
	
G91
        
G1 X($Cx-$Dx-($Cx_dif-$Dx_dif))  Y($Dy-$Cy+($Dy_dif-$Cy_dif))
    
else
        MSGDISPLAY 1 "Improper Nozzle Change Input"  
    
ENDIF
  
	
	IF $set_home = 1			
		POSOFFSET CLEAR X Y U				
		G92 X0 Y0     		
	ENDIF	

ENDDFS



; ------------ Set z Home Function --------------------

DFS set_z_home
	G90
	G1 A-5 B-5 C-5 D-5 F20
	G91
	G92 A(-$zA-5) B(-$zB-5) C(-$zC - 5) D(-$zD - 5)
ENDDFS





;-------------- Calculate Relative Z Function --------------------
DFS calc_relative_z
	$reference_nozzle = $Q

	if $reference_nozzle = 1
        	$zA = $zo_ref
        	$zB = $zA + ($zMeasureB - $zMeasureA) + ($Az_dif-$Bz_dif)
        	$zC = $zA + ($zMeasureC - $zMeasureA) + ($Az_dif-$Cz_dif)
        	$zD = $zA + ($zMeasureD - $zMeasureA) + ($Az_dif-$Dz_dif)
    	else if $reference_nozzle = 2
            	$zB = $zo_ref
            	$zA = $zB + ($zMeasureA - $zMeasureB) + ($Bz_dif-$Az_dif)
            	$zC = $zB + ($zMeasureC - $zMeasureB) + ($Bz_dif-$Cz_dif)
            	$zD = $zB + ($zMeasureD - $zMeasureB) + ($Bz_dif-$Dz_dif)
    	else if $reference_nozzle = 3
           	$zC = $zo_ref
            	$zA = $zC + ($zMeasureA - $zMeasureC) + ($Cz_dif-$Az_dif)
            	$zB = $zC + ($zMeasureB - $zMeasureC) + ($Cz_dif-$Bz_dif)
            	$zD = $zC + ($zMeasureD - $zMeasureC) + ($Cz_dif-$Dz_dif)
    	else if $reference_nozzle = 4
            	$zD = $zo_ref
           		$zA = $zD + ($zMeasureA - $zMeasureD) + ($Dz_dif-$Az_dif)
            	$zB = $zD + ($zMeasureB - $zMeasureD) + ($Dz_dif-$Bz_dif)
            	$zC = $zD + ($zMeasureC - $zMeasureD) + ($Dz_dif-$Cz_dif)
	ENDIF
	MSGDISPLAY 1 "zA is: " $zA
	MSGDISPLAY 1 "zB is: " $zB
	MSGDISPLAY 1 "zC is: " $zC
	MSGDISPLAY 1 "zD is: " $zD
ENDDFS

;######## Align and zero function ###################

DFS alignZeroNozzle

	$zStart = $Q
	$delta = $R
	$nozzle = $L
	$floor = $I
	$deltafast = $J
	$fastfeed = 30
	$midfeed = 10
	$slowfeed = 2

        ;#$Ax = 483
	;#$Ay = 317
	;#$Bx = 379
	;#$By = 317
	;#$Cx = 275
	;#$Cy = 317
	;#$Dx = 196
	;#$Dy = 317
	;#$Px = 148
	;#$Py = 345
	
	$Ax = 586.075
	$Ay = 367.8285
	$Bx = 482.075
	$By = 367.8285
	$Cx = 378.075
	$Cy = 367.8285
	$Dx = (299.075 - 25) ; Add 25mm beacuse we changed the holder position
	$Dy = 367.8285

	
	$xOffset = 0.7
	$yOffset = -0.7
	$DO7.0=0
	$comport = FILEOPEN "COM8", 2
	COMMINIT $comport, "baud=115200 parity=N data=8 stop=1" ; Initialize comport
	COMMSETTIMEOUT $comport, -1, 0, 0
	
	
	FILEWRITE $comport "PW,3" ; Select Program #3
	FILEREAD $comport 0 $strglob1

	
	G90
	G1 A-1 B-1 C-1 D-1 F$fastfeed
	IF $nozzle = 1
		$xStart = $Ax
		$yStart = $Ay
		G1 X$xStart Y$yStart
		G1 A$zStart
	ELSE IF $nozzle = 2
		$xStart = $Bx
		$yStart = $By
		G1 X$xStart Y$yStart
		G1 B$zStart
	ELSE IF $nozzle = 3
		$xStart = $Cx
		$yStart = $Cy
		G1 X$xStart Y$yStart
		G1 C$zStart
	ELSE IF $nozzle = 4
		$xStart = $Dx
		$yStart = $Dy
		G1 X$xStart Y$yStart
		G1 D$zStart
	ELSE IF $nozzle = 5
		$xStart = $Px
		$yStart = $Py
		G1 X$xStart Y$yStart
		G1 D$zStart
	ELSE 
		G1 A-1 B-1 C-1 D-1
	ENDIF
	G91


	$found = 0
	WHILE $found != -1
	
		FILEWRITE $comport "M0,0"
		FILEREAD $comport 0 $strglob0	
		
		$found = STRFIND($strglob0, "--", 1)
		IF $nozzle == 1
			$posZ = AXISSTATUS(A, DATAITEM_PositionFeedback)
			ELSEIF $nozzle ==2
			$posZ = AXISSTATUS(B, DATAITEM_PositionFeedback)
			ELSEIF $nozzle ==3
			$posZ = AXISSTATUS(C, DATAITEM_PositionFeedback)
			ELSEIF $nozzle ==4
			$posZ = AXISSTATUS(D, DATAITEM_PositionFeedback)
			ELSEIF $nozzle ==5
			$posZ = AXISSTATUS(D, DATAITEM_PositionFeedback)
		ENDIF
		
		
		IF ($posZ - $deltafast) < $floor
			$found = -1
		ELSE
			IF $nozzle == 1
				G1 A-$deltafast F$midfeed
				ELSEIF $nozzle == 2
				G1 B-$deltafast F$midfeed
				ELSEIF $nozzle == 3
				G1 C-$deltafast F$midfeed
				ELSEIF $nozzle == 4
				G1 D-$deltafast F$midfeed
				ELSEIF $nozzle == 5
				G1 D-$deltafast F$midfeed
				ELSE
				MSGDISPLAY 1 "something is messed up"
			ENDIF
		ENDIF
		
	ENDWHILE

; move up slightly and redo it again slowly
IF $nozzle == 1
			G1 A3.5 F$fastfeed
			ELSEIF $nozzle == 2
			G1 B3.5 F$fastfeed
			ELSEIF $nozzle == 3
			G1 C3.5 F$fastfeed
			ELSEIF $nozzle == 4
			G1 D3.5 F$fastfeed
			ELSEIF $nozzle == 5
			G1 D3.5 F$fastfeed
			ELSE
			MSGDISPLAY 1 "something is messed up"
ENDIF



	$found = 0
WHILE $found != -1

	FILEWRITE $comport "M0,0"
	FILEREAD $comport 0 $strglob0	
	$found = STRFIND($strglob0, "--", 1)
	IF $nozzle ==1
		$posZ = AXISSTATUS(A, DATAITEM_PositionFeedback)
		ELSEIF $nozzle ==2
		$posZ = AXISSTATUS(B, DATAITEM_PositionFeedback)
		ELSEIF $nozzle ==3
		$posZ = AXISSTATUS(C, DATAITEM_PositionFeedback)
		ELSEIF $nozzle ==4
		$posZ = AXISSTATUS(D, DATAITEM_PositionFeedback)
		ELSEIF $nozzle ==5
		$posZ = AXISSTATUS(D, DATAITEM_PositionFeedback)
	ENDIF
	
	IF ($posZ - $deltafast) < $floor
		$found = -1
	ELSE
		IF $nozzle == 1
			G1 A-$delta F$slowfeed
			ELSEIF $nozzle == 2
			G1 B-$delta F$slowfeed
			ELSEIF $nozzle == 3
			G1 C-$delta F$slowfeed
			ELSEIF $nozzle == 4
			G1 D-$delta F$slowfeed
			ELSEIF $nozzle == 5
			G1 D-$delta F$slowfeed
			ELSE
			MSGDISPLAY 1 "something is messed up"
		ENDIF
	ENDIF
ENDWHILE

IF $nozzle == 1
			G1 A-0.4 F$midfeed
			ELSEIF $nozzle == 2
			G1 B-0.4 F$midfeed
			ELSEIF $nozzle == 3
			G1 C-0.4 F$midfeed
			ELSEIF $nozzle == 4
			G1 D-0.4 F$midfeed
			ELSEIF $nozzle == 5
			G1 D-0.4 F$midfeed
			ELSE
			MSGDISPLAY 1 "something is messed up"
ENDIF

;Dwell to get accurate Reading
DWELL 0.75

; read from keyance
FILEWRITE $comport "M0,0"
FILEREAD $comport 0 $strglob0

; Assign Reading To Variables

	$comma1 = STRFIND($strglob0, ",", 1)
	$comma1plus=$comma1+1
	$STRGLOB1 = STRMID ($STRGLOB0, $comma1plus, 40)
	$comma2 = STRFIND($strglob1, ",", 1)
	$comma2 = $comma2 + $comma1
	$comma2plus = $comma2+2
	$STRGLOB2 = STRMID ($STRGLOB0, $comma1plus, $comma2)
	$STRGLOB3 = STRMID ($STRGLOB0, $comma2plus, 40)

		IF $nozzle = 1
			$Ax_dif = STRTODBL($STRGLOB2)
			$Ay_dif = STRTODBL($STRGLOB3)
			ELSEIF $nozzle == 2
			$Bx_dif = STRTODBL($STRGLOB2)
			$By_dif = STRTODBL($STRGLOB3)
			ELSEIF $nozzle == 3
			$Cx_dif = STRTODBL($STRGLOB2)
			$Cy_dif = STRTODBL($STRGLOB3)
			ELSEIF $nozzle == 4
			$Dx_dif = STRTODBL($STRGLOB2)
			$Dy_dif = STRTODBL($STRGLOB3)
			ELSEIF $nozzle == 5
			$Px_dif = STRTODBL($STRGLOB2)
			$Py_dif = STRTODBL($STRGLOB3)
		ENDIF


;switch keyence programs
$DO7.0=1
FILEWRITE $comport "PW,4" ; Select Program #4
FILEREAD $comport 0 $strglob1

; Attain zero value
        IF $nozzle = 1
			G91
			G1 X-$Ax_dif Y-$Ay_dif F5
			G1 X$xOffset Y$yOffset
			$zMeasureA = AXISSTATUS(A, DATAITEM_PositionFeedback)
			DWELL 3
			CALL zHold Q2 R0.075 L0.25
	                $Az_dif = $z_dif
	                MSGDISPLAY 1 "Az_dif: " + $Az_dif
			MSGDISPLAY 1 "zMeasureA: " + $zMeasureA
			
			ELSEIF $nozzle == 2
			G91
			G1 X-$Bx_dif Y-$By_dif F5
			G1 X$xOffset Y$yOffset
			DWELL 3
			$zMeasureB = AXISSTATUS(B, DATAITEM_PositionFeedback)
			CALL zHold Q2 R0.025 L0.25
	                $Bz_dif = $z_dif
	                MSGDISPLAY 1 "Bz_dif: " + $Bz_dif
			MSGDISPLAY 1 "zMeasureB: " + $zMeasureB
	                
			ELSEIF $nozzle == 3
			G91
			G1 X-$Cx_dif Y-$Cy_dif F5
			G1 X$xOffset Y$yOffset
			DWELL 3
			$zMeasureC = AXISSTATUS(C, DATAITEM_PositionFeedback)
			CALL zHold Q2 R0.025 L0.25
	                $Cz_dif = $z_dif
	                MSGDISPLAY 1 "Cz_dif: " + $Cz_dif
			MSGDISPLAY 1 "zMeasureC: " + $zMeasureC
	                
			ELSEIF $nozzle == 4
			G91
			G1 X-$Dx_dif Y-$Dy_dif F5
			G1 X$xOffset Y$yOffset
			DWELL 3
			$zMeasureD = AXISSTATUS(D, DATAITEM_PositionFeedback)
			CALL zHold Q2 R0.025 L0.25
	                $Dz_dif = $z_dif
	                MSGDISPLAY 1 "Dz_dif: " + $Dz_dif
			MSGDISPLAY 1 "zMeasureD: " + $zMeasureD
		ENDIF

$DO7.0=0
FILEWRITE $comport "PW,3" ; Select Program #3
FILEREAD $comport 0 $strglob1
	G90
	G1 A-1 B-1 C-1 D-1 F25
	G91
	
	

	FILECLOSE $comport
ENDDFS

DFS zHold
    $zSweepRange = $Q
    $zSweepStep = $R
    $zDwell = $L
    $start = (($zSweepRange/2)/1.414213)
    $x_dist = (($zSweepRange)/1.414213)
    $z_dif = 8
    G91
    G1 X-($start) Y$start F2

    FILEWRITE $comport "U1"
    FILEREAD $comport 0 $strglob0
    G1 X$x_dist Y-$x_dist F0.25
    FILEWRITE $comport "L1,0"
    FILEREAD $comport 0 $strglob0
    $STRGLOB1 = STRMID ($STRGLOB0, 4, -1)
    $z_dif = STRTODBL($STRGLOB1)
    WHILE $z_dif < 0.1
        FILECLOSE $comport
       
        $z_dif = 8
        G91
        G1 X-$x_dist Y$x_dist F4
        
        $comport = FILEOPEN "COM8", 2
	COMMINIT $comport, "baud=115200 parity=N data=8 stop=1" ; Initialize comport
	COMMSETTIMEOUT $comport, -1, 0, 0
        FILEREAD $comport 0 $strglob5
        FILEWRITE $comport "PW,4" ; Select Program #4
        FILEREAD $comport 0 $strglob1
        DWELL(0.25)
        FILEWRITE $comport "U1"
        FILEREAD $comport 0 $strglob0
        G1 X$x_dist Y-$x_dist F0.1
        FILEWRITE $comport "L1,0"
        DWELL(0.25)
        FILEREAD $comport 0 $strglob0
        $STRGLOB1 = STRMID ($STRGLOB0, 4, -1)
        $z_dif = STRTODBL($STRGLOB1)
        IF $z_dif > 7.8
            $z_dif = 0
        ENDIF
    ENDWHILE

ENDDFS

;##### Toggle Press and set press ################
DFS setPress        
         
        $strtask1 = DBLTOSTR( $P, 0 )            
        $strtask1 = "COM" + $strtask1
        $hFile = FILEOPEN $strtask1, 2
        COMMINIT $hFile, "baud=115200 parity=N data=8 stop=1"
        COMMSETTIMEOUT $hFile, -1, -1, 1000
                             
        $press = $Q * 10.0                             
        $strtask2 = DBLTOSTR( $press , 0 )  
      
      
        $length = STRLEN( $strtask2 )      
        WHILE $length < 4.0
                $strtask2 = "0" + $strtask2    
                $length = STRLEN( $strtask2 ) 
        ENDWHILE


        $strtask2 = "08PS  " + $strtask2
                                    
        $cCheck = 0.00     
        $lame = STRTOASCII ($strtask2, 0)
        $cCheck = $cCheck - $lame
        $lame = STRTOASCII( $strtask2, 1) 
        $cCheck = $cCheck - $lame
        $lame = STRTOASCII( $strtask2, 2) 
        $cCheck = $cCheck - $lame
        $lame = STRTOASCII( $strtask2, 3) 
        $cCheck = $cCheck - $lame
        $lame = STRTOASCII( $strtask2, 4)
        $cCheck = $cCheck - $lame
        $lame = STRTOASCII( $strtask2, 5) 
        $cCheck = $cCheck - $lame
        $lame = STRTOASCII( $strtask2, 6) 
        $cCheck = $cCheck - $lame
        $lame = STRTOASCII( $strtask2, 7) 
        $cCheck = $cCheck - $lame
        $lame = STRTOASCII( $strtask2, 8) 
        $cCheck = $cCheck - $lame
        $lame = STRTOASCII( $strtask2, 9)  
        $cCheck = $cCheck - $lame
                        
        WHILE( $cCheck) < 0
                $cCheck = $cCheck + 256
        ENDWHILE                        


        $strtask3 = makestring "{#H}" $cCheck   
        $strtask3 = STRUPR( $strtask3 )
        $strtask2 = "\x02" + $strtask2 + $strtask3 + "\x03"
            
        FILEWRITE $hFile "\x05"
        FILEWRITE $hFile $strtask2
        FILEWRITE $hFile "\x04"


        FILECLOSE $hFile


ENDDFS


DFS togglePress        
         
        $strtask1 = DBLTOSTR( $P, 0 )            
        $strtask1 = "COM" + $strtask1
        $hFile = FILEOPEN $strtask1, 2
        COMMINIT $hFile, "baud=115200 parity=N data=8 stop=1"
        COMMSETTIMEOUT $hFile, -1, -1, 1000


        $strtask2 = "04DI  "
                                    
        $cCheck = 0.00     
        $lame = STRTOASCII ($strtask2, 0)
        $cCheck = $cCheck - $lame
        $lame = STRTOASCII( $strtask2, 1) 
        $cCheck = $cCheck - $lame
        $lame = STRTOASCII( $strtask2, 2) 
        $cCheck = $cCheck - $lame
        $lame = STRTOASCII( $strtask2, 3) 
        $cCheck = $cCheck - $lame
        $lame = STRTOASCII( $strtask2, 4)
        $cCheck = $cCheck - $lame
        $lame = STRTOASCII( $strtask2, 5) 
        $cCheck = $cCheck - $lame
                        
        WHILE( $cCheck) < 0
                $cCheck = $cCheck + 256
        ENDWHILE                        


        $strtask3 = makestring "{#H}" $cCheck   
        $strtask3 = STRUPR( $strtask3 )
        $strtask2 = "\x02" + $strtask2 + $strtask3 + "\x03"
                  
        FILEWRITE $hFile "\x05"
        FILEWRITE $hFile $strtask2
        FILEWRITE $hFile "\x04"


        FILECLOSE $hFile
        G4 P0.15

ENDDFS

; ############### Alignment save function ########################


DFS save_value_aerotech

    $nozzle = $Q
IF $nozzle = 1
    $align_save = FILEOPEN "C:\Users\Lewis Group\Desktop\Alignment\Aerotech Alignment Files\alignment_values_1_aerotech.txt", 0
    FILEWRITE $align_save $Ax_dif  "," $Ay_dif ","  $zMeasureA ","  $Az_dif
    
ENDIF
IF $nozzle = 2
    $align_save = FILEOPEN "C:\Users\Lewis Group\Desktop\Alignment\Aerotech Alignment Files\alignment_values_2_aerotech.txt", 0
    FILEWRITE $align_save $Bx_dif  "," $By_dif ","  $zMeasureB ","  $Bz_dif
ENDIF
IF $nozzle = 3
    $align_save = FILEOPEN "C:\Users\Lewis Group\Desktop\Alignment\Aerotech Alignment Files\alignment_values_3_aerotech.txt", 0
    FILEWRITE $align_save $Cx_dif  "," $Cy_dif ","  $zMeasureC ","  $Cz_dif
ENDIF
IF $nozzle = 4
    $align_save = FILEOPEN "C:\Users\Lewis Group\Desktop\Alignment\Aerotech Alignment Files\alignment_values_4_aerotech.txt", 0
    FILEWRITE $align_save $Dx_dif  "," $Dy_dif ","  $zMeasureD ","  $Dz_dif
ENDIF


FILECLOSE $align_save
ENDDFS

"""

