'''
mecProxyShape.py
By: Michael Clavan

Description:
	This script creates another shape nodes that reflexes the first one.
	- The second object can be smoothed and rendered as a high res version 
		of the character.

How to Run:
	
- Select the object you want to replicate.

import mecProxyShape
mecProxyShape.proxyShape()

- or -
mecProxyShape.proxyShape(2)

'''
import maya.cmds as cmds


def proxyShape(myDiv=1):
	'''
	ProxyShape function is the main function for this script.
	- Select a poly object in the scene.
	- then call proxyShape.
	
	Arguments
	myDiv(int) == Divisions the proxy will be smoothed.
		- defaults to 1	
	'''
	
	# getShapeNodes of selected.
	selected = cmds.ls(sl=True)[0]
	sourceShape = cmds.ls(selected, shapes=True, dag=True)[0]
	
	# Create a mesh
	targShape = cmds.createNode('mesh')
	targObj = cmds.listRelatives( targShape, p=True )[0]
	
	
	
	'''
	# Selected position
	selPos = cmds.xform(selected, q=True, ws=True, piv=True ) 
	cmds.xform( targObj, ws=True, piv=selPos[0:3] )
	
	selTrans = cmds.xform(selected, q=True, ws=True, piv=True )
	cmds.xform( targObj, t=selTrans[0:3] )	
	'''
	# Connect the outMesh to the inMesh
	cmds.connectAttr( "%s.outMesh" %sourceShape, "%s.inMesh" %targShape )
	
	cmds.xform(targObj, cp=True)
	
	selTrans = cmds.xform(selected, q=True, ws=True, t=True )
	cmds.xform( targObj, t=selTrans[0:3] )	
	
	# Smooth (optional)
	cmds.polySmooth( targObj, dv=myDiv )
	
	
	
	# cmds.sets("initialShadingGroup", e=True, forceElement=True )
	cmds.sets(targObj, e=True, forceElement="initialShadingGroup")
	
	cmds.select(targObj, r=True )
	cmds.rename( targObj, selected + "_hRez" )

"""
global proc proxyShape(string $myDiv)
{
	string $selected[] = `ls -sl`;
	string $sourceShape[] = `ls -shapes -dag $selected[0]`;
	
	string $targShape[] = `createNode -n "mesh"`;
	string $targObj[] = `listRelatives -p $targShape[0]`;
	
	connectAttr ($sourceShape[0] + ".outMesh") ($targShape[0] + ".inMesh"); 
	
	polySmooth -dv $myDiv;
	rename $targObj ($selected[0] + "_hRez");
	
	sets -e -forceElement "initialShadingGroup" $targObj[0];
	select -r $targObj[0];
	
}
"""
	
	
