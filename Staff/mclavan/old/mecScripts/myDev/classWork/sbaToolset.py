'''
Rigging Toolset
sbaToolsetRig.py
Michael Clavan

Description:
	This script includes a grouping of common tools for rigging.
	Constraints
		- Point
		- Orient
		- Parent
			- offset options for these three.
		- Pole Vector
		- Delete History
		- Freeze Transforms
	Control Icons
		- Circle
		- Square
		- Cube
		- COG
	Control Colors
		- Standard
			- Red, Yellow, Blue
		- Field Option
	
How to Run:
import sbaToolset
reload( sbaToolset )
sbaToolset.gui()

Help:
help( sbaToolset )
'''

import maya.cmds as cmds

print( "SBA - Rigging Toolset" )

def gui():
	
	win = "sbaRigTool"
	winWidth = 220
	# Checking to see if the window exists.
	if( cmds.window( win, ex=True ) ):
		cmds.deleteUI(win)
	if( cmds.windowPref( win, ex=True ) ):
		cmds.windowPref( win, r=True )
	
	# Creating the window.
	cmds.window(win, title="Rigging Toolset", w=winWidth, h=360 )
	mainCol = cmds.columnLayout(co=["both", 5], rs=3)
	# GUI controls go here.
	
	# Rigging toolset
	cmds.frameLayout( label="Rigging Tools",  labelAlign="center" )
	rigCol = cmds.columnLayout(co=["both", 5], rs=3)
	cmds.text( label="Constraints", w=180 )	
	cmds.rowColumnLayout( nc=2, cw=[[1,115],[2,70]], co=[[1,"right", 5],[2, "left", 5]])
	cmds.button( label="Point")
	cmds.checkBox( label="Offset" )
	cmds.button( label="Orient")
	cmds.checkBox( label="Offset" )
	cmds.button( label="Parent")
	cmds.checkBox( label="Offset" )
	cmds.setParent(rigCol)
	
	cmds.button( label="Pole Vector", w=180 )
	
	cmds.button( label="Delete History", w=180 )
	cmds.button( label="Freeze Tranforms", w=180 )
	cmds.setParent( mainCol )
	
	# Control Icons
	cmds.frameLayout( label="Control Icons Tools",  labelAlign="center" )
	iconCol = cmds.columnLayout(co=["both", 5], rs=3)

	cmds.text( label="Create Control Icons", w=185 )
	colVal = 185
	cmds.rowColumnLayout(nc=4, cw=[[1,colVal/4],[2,colVal/4],[3,colVal/4],[4,colVal/4]])
	cmds.button( label="Circle" )
	cmds.button( label="Square" )
	cmds.button( label="Cube" )
	cmds.button( label="COG" )
	
	cmds.setParent(iconCol)
	cmds.text( label="Color Control Icons", w=185 )
	cmds.rowColumnLayout(nc=3, cw=[[1,colVal/3],[2,colVal/3],[3,colVal/3]])
	cmds.button( label="Red" )
	cmds.button( label="Yellow" )
	cmds.button( label="Blue" )
	cmds.setParent(iconCol)
	cmds.rowColumnLayout(nc=2, cw=[[1,50],[2,colVal-50]], co=[[1,"right",5],[2,"left", 5]])
	cmds.intField( v=1, min=1, max=15 )
	cmds.button( label="Apply Color" )
	
	cmds.showWindow()
	

