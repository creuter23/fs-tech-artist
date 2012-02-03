'''
CRI - Lecture 4 - Procedural Scripting
criLect4.py

Description:


How To Run:


'''


'''
Concept
Podcast 1
'''

'''
Setting up a control
'''

# Break down into steps

# 1) User selected joint then icon
# 	- That means I'm going to have to get selected.
# 2) Control is point and orient constraint to joint
#	- To match orientations
# 3) Constraints are deleted
#	- Because they were only used to match orientations.
# 4) Constrain joint by the control icon
# 	- The type of constraint could be offered though an interface.


'''
# Selection
select -r lt_arm_elbow_bj ;
select -tgl controlIcon ;

# 1st == joint, 2nd == control icon
selection = cmds.ls(sl=True)  # Selection order is preserved
'''


'''
# constraints

doCreatePointConstraintArgList 1 { "0","0","0","0","0","0","0","1","","1" };
pointConstraint -offset 0 0 0 -weight 1;
// Result: controlIcon_pointConstraint1 // 
doCreateOrientConstraintArgList 1 { "0","0","0","0","0","0","0","1","","1" };
orientConstraint -offset 0 0 0 -weight 1;
// Result: controlIcon_orientConstraint1 // 


# There isn't an effected object, will work based on selection!
cmds.pointConstraint( offset=[0,0,0], weight=1 )
cmds.orientConstraint( offset=[0,0,0], weight=1 )

# The return the name of the constrains.
pointConst = cmds.pointConstraint( offset=[0,0,0], weight=1 )
orientConst = cmds.orientConstraint( offset=[0,0,0], weight=1 )
'''

'''
# Delete Constraints
# I need a command to delete the constraint on the control icon
# delete command
cmds.delete(pointConst, orientConst)
'''

'''
Constrain the joint to the control icon
# Choosing orient for now.
# cmds.orientConstraint( offset[0,0,0], weight=1 )
# pc = cmds.pointConstraint([targets], obj, offset=[0,0,0], weight=1 )
# cmds.orientConstraint("controlIcon", "joint", offset=[0,0,0], weight=1 )

cmds.orientConstraint(selected[1], selected[0], offset=[0,0,0], weight=1 )
'''



'''
# Cleaning up the code
# Using last example to refer directly to objects, NOT by selection.
# Podcast 2

selection = cmds.ls(sl=True) # 0 == "joint", 1 == "icon"
pointConst = cmds.pointConstraint(selection[0], selection[1], offset=[0,0,0], weight=1 )
orientConst = cmds.orientConstraint(selection[0], selection[1], offset=[0,0,0], weight=1 )
cmds.delete( pointConst, orientConst )
cmds.orientConstraint(selected[1], selected[0], offset=[0,0,0], weight=1 )
'''

def setupIcon():
	'''
	This function will match the orientations from the first item selected to the second item selected.
	Object will move to match.
	'''
	selection = cmds.ls(sl=True) # 0 == "joint", 1 == "icon"
	pointConst = cmds.pointConstraint(selection[0], selection[1], offset=[0,0,0], weight=1 )
	orientConst = cmds.orientConstraint(selection[0], selection[1], offset=[0,0,0], weight=1 )
	cmds.delete( pointConst, orientConst )
	cmds.orientConstraint(selected[1], selected[0], offset=[0,0,0], weight=1 )



'''
With a group
'''
# Create a group
# Point and Orient Constraint it.
# Delete Constraints.
# Point Control Curve
# Delete Contraint
# Parent Control Icon to Group
# Freeze Transforms on Control Icon
# Constrain joint to control icon


'''
Functions 
Arguments and Return statements.
'''

'''
Give the user the option to point, orient, or parent constraint the affected object.

mode = 0

# mode == 0 is point constraint
if( mode == 0 ):
	cmds.pointConstraint(selected[1], selected[0], offset=[0,0,0], weight=1 )

# mode == 1 is orient constraint
elif( mode == 1 ):
	cmds.orientConstraint(selected[1], selected[0], offset=[0,0,0], weight=1 )

# mode == 2 is parent constraint
else:
	cmds.parentConstraint(selected[1], selected[0], offset=[0,0,0], weight=1 )
'''

def setupIconGrp(mode=0):
	'''
	This function will match the orientations from the first item selected to the second item selected.
	Object will move to match.
	'''
	# Selected items in the secene	
	selection = cmds.ls(sl=True) # 0 == "joint", 1 == "icon"
	
	# Group Created for padding (named after control icon)
	grp = cmds.group( name=selected[0]+"_grp", empty=True, world=True )

	# Matching Constraints
	pointConstIcon = cmds.pointConstraint(selection[0], selection[1], offset=[0,0,0], weight=1 )
	pointConstGrp = cmds.pointConstraint(selection[0], grp, offset=[0,0,0], weight=1 )
	orientConstIcon = cmds.orientConstraint(selection[0], selection[1], offset=[0,0,0], weight=1 )
	orientConstGrp = cmds.orientConstraint(selection[0], grp, offset=[0,0,0], weight=1 )
	
	# Deleting unwanted constraints
	cmds.delete( pointConstIcon, pointConstGrp, orientConstIcon, orientConstGrp )
	
	# Parenting & Matching control icon's orientations to the groups 
	cmds.parent( selection[1], grp )
	
	# Constraining joint to control icon
	if( mode == 0 ):
		cmds.pointConstraint(selected[1], selected[0], offset=[0,0,0], weight=1 )
	
	# mode == 1 is orient constraint
	elif( mode == 1 ):
		cmds.orientConstraint(selected[1], selected[0], offset=[0,0,0], weight=1 )
	
	# mode == 2 is parent constraint
	else:
		cmds.parentConstraint(selected[1], selected[0], offset=[0,0,0], weight=1 )

	# Returning the name of the group
	return grp	
# iconGrp = setupIcon(2)

'''
Automation Switch
'''

# Multiply Node




'''
Nodes
'''

'''
Creating Nodes
- shadingNode
- sets
- createNode
'''

'''
# Basic Shader

# MEL
shadingNode -asShader blinn;
// Result: blinn1 // 
sets -renderable true -noSurfaceShader true -empty -name blinn1SG;
// Result: blinn1SG // 
connectAttr -f blinn1.outColor blinn1SG.surfaceShader;
// Result: Connected blinn1.outColor to blinn1SG.surfaceShader. // 

# Python
# shadingNode command creates a node and organizes it in the hypershader.
cmds.shadingNode( "blinn", asShader=True)
# sets command in this case creates the shader group (but it does more than that).
cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name="blinnSG")
# Connecting attributes
cmds.connectAttr( "blinn1.outColor", "blinn1SG.surfaceShader", f=True)

'''

'''
Connecting Attributes
- connectAttr
'''


'''
Changing Values
- getAttr
- setAttr
'''




'''
# File
shadingNode -asTexture file;
// Result: file1 // 
shadingNode -asUtility place2dTexture;
// Result: place2dTexture1 // 
connectAttr -f place2dTexture1.coverage file1.coverage;
// Result: Connected place2dTexture1.coverage to file1.coverage. // 
connectAttr -f place2dTexture1.translateFrame file1.translateFrame;
// Result: Connected place2dTexture1.translateFrame to file1.translateFrame. // 
connectAttr -f place2dTexture1.rotateFrame file1.rotateFrame;
// Result: Connected place2dTexture1.rotateFrame to file1.rotateFrame. // 
connectAttr -f place2dTexture1.mirrorU file1.mirrorU;
// Result: Connected place2dTexture1.mirrorU to file1.mirrorU. // 
connectAttr -f place2dTexture1.mirrorV file1.mirrorV;
// Result: Connected place2dTexture1.mirrorV to file1.mirrorV. // 
connectAttr -f place2dTexture1.stagger file1.stagger;
// Result: Connected place2dTexture1.stagger to file1.stagger. // 
connectAttr -f place2dTexture1.wrapU file1.wrapU;
// Result: Connected place2dTexture1.wrapU to file1.wrapU. // 
connectAttr -f place2dTexture1.wrapV file1.wrapV;
// Result: Connected place2dTexture1.wrapV to file1.wrapV. // 
connectAttr -f place2dTexture1.repeatUV file1.repeatUV;
// Result: Connected place2dTexture1.repeatUV to file1.repeatUV. // 
connectAttr -f place2dTexture1.offset file1.offset;
// Result: Connected place2dTexture1.offset to file1.offset. // 
connectAttr -f place2dTexture1.rotateUV file1.rotateUV;
// Result: Connected place2dTexture1.rotateUV to file1.rotateUV. // 
connectAttr -f place2dTexture1.noiseUV file1.noiseUV;
// Result: Connected place2dTexture1.noiseUV to file1.noiseUV. // 
connectAttr -f place2dTexture1.vertexUvOne file1.vertexUvOne;
// Result: Connected place2dTexture1.vertexUvOne to file1.vertexUvOne. // 
connectAttr -f place2dTexture1.vertexUvTwo file1.vertexUvTwo;
// Result: Connected place2dTexture1.vertexUvTwo to file1.vertexUvTwo. // 
connectAttr -f place2dTexture1.vertexUvThree file1.vertexUvThree;
// Result: Connected place2dTexture1.vertexUvThree to file1.vertexUvThree. // 
connectAttr -f place2dTexture1.vertexCameraOne file1.vertexCameraOne;
// Result: Connected place2dTexture1.vertexCameraOne to file1.vertexCameraOne. // 
connectAttr place2dTexture1.outUV file1.uv;
// Result: Connected place2dTexture1.outUV to file1.uvCoord. // 
connectAttr place2dTexture1.outUvFilterSize file1.uvFilterSize;
// Result: Connected place2dTexture1.outUvFilterSize to file1.uvFilterSize. // 
defaultNavigation -force true -connectToExisting -source file1 -destination blinn1.color; window -e -vis false createRenderNodeWindow;
connectAttr -force file1.outColor blinn1.color;
// Result: Connected file1.outColor to blinn1.color. // 
// Result: createRenderNodeWindow // 
setAttr -type "string" file1.fileTextureName "testA.tga";

'''



