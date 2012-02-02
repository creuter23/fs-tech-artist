'''
IK/FK Script

Description:
	Generates an IKFK system
How to run


'''


import maya.cmds as cmds
import pymel.core as pm
import rigTools

win = "mecIKFKWin"
winWidth = 300
winHeight = 300

# What type of elements are required from the user to make this script work?
# - Control Icons

# What needs to be created by the script?
# - Control Icons? Yes
# - FK and or IK joint chain? Yes
# - How are the systems going to be named? By the binding joint


controlIcons = []
fkJoints = []
ikJoints = []

def gui():
	
	if( cmds.window( win, ex=True ) ):
		cmds.deleteUI(win)
	if( cmds.windowPref(win, ex=True) ):
		cmds.windowPref(win, r=True)
		
	cmds.window(win, title="IK / FK System Generator", w=winWidth, h=winHeight)
	mainCol = cmds.columnLayout()
	
	cmds.button( label="Build System", w=100,
		command=pm.Callback( mainBuild ) )
	
	cmds.showWindow(win)

def mainBuild():
	
	# Use will select the joints to build the system on.
	selected = cmds.ls(sl=True)
	
	buildFKSystem(selected)

def buildFKSystem(bindingJoints):
	'''
	This FK system builder will build a fk control system for the joint system provided by the functions arguments.
	'''
	
	# Duplicate the joints
	fkJoints = cmds.duplicate( rc=True )
	
	# Control Icons
	icons = []
	groups = []
	for i, fkJoint in enumerate( fkJoints ):
		# Rename duplicated joints
		pieces = bindingJoints[i].split("_")
		if( pieces > 1 ):
			pieces[-1] = "fk"
		newName = "_".join(pieces)
		cmds.rename( fkJoint, newName )
		
		# Build the control curves
		# circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 0.01 -s 8 -ch 0;
		icon = cmds.circle( c=[0,0,0], nr=[0,1,0], sw=360, r=1, d=3, ut=0, tol=0.01, s=1, ch=0 )[0];
		
		
		# Prime Control
		primeInfo = rigTools.primeControl(fkJoint, icon)
		groups.append(primeInfo[1])
		icons.append(icon)
		
		# Orient Constrain FK System
		cmds.orientConstraint( icon, fkJoint )
		
	# Parent System together
	for i, icon in enumerate( icons ):
		parent( icon, group[i] )
		if( i != 0 ):
			parent( group[i], icons[i-1] )

def primeGUI(curParent):
	frm = cmds.formLayout( parent=curParent )
	

	'''
	btn1 = cmds.button( label="Prime Control", w=110,
		c=pm.Callback(primeOptions))
	global primeChoice
	primeChoice = cmds.radioButtonGrp( nrb=4, labelArray4=['Point', 'Orient', 'Parent', 'None'],
		label="", cw=[[1,5],[2,60],[3,60],[4,60],[5,60]], sl=4)
	
	cmds.formLayout( frm, e=1, af=[[btn1, "left", 5],[btn1, "top", 5]] )
	cmds.formLayout( frm, e=1, ac=[primeChoice, "left", 5, btn1], af=[primeChoice, "top", 5] )
	'''
	cmds.setParent(frm)
	return frm

