'''
Nodes
Creating Nodes
nodes1.py

Description:
	- This script covers different ways how to create nodes in 
		maya through scripting.
	
How to Run:

import nodes1
reload( nodes1 )
'''


'''
Creating Nodes
shadingNode, sets, & createNode
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
shadingNode command
'''
# cmds.shadingNode( "blinn", asShader=True)
blinnName = cmds.shadingNode( "blinn", asShader=True)

'''
sets command
'''
# cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name="blinnSG")
blinnSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name=blinnName + "_SG")

'''
createNode command
'''
multName = cmds.createNode( 'multiplyDivide', name="auto" )
blendName = cmds.createNode( 'blendColors', name="armSwitch1_blend" )






