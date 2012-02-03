'''
Nodes
Connecting Nodes
Nodes2.py

Description:
	- This script covers different ways how to connect one attribute to another.
	
How to Run:

import nodes2
reload( nodes2 )
'''


'''
Connecting Attributes
connectAttr Command
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
# force(f) will disconnect any preexisting connections.
# cmds.connectAttr( "ouput.attr", "input.attr", force=True )

#                     Output                 Input     
cmds.connectAttr( "blinn1.outColor", "blinn1SG.surfaceShader", f=True) 


'''
Cleaning up example

# Python
# shadingNode command creates a node and organizes it in the hypershader.
cmds.shadingNode( "blinn", asShader=True)
# sets command in this case creates the shader group (but it does more than that).
cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name="blinnSG")
# Connecting attributes
cmds.connectAttr( "blinn1.outColor", "blinn1SG.surfaceShader", f=True)
'''

blinnName = cmds.shadingNode( "blinn", asShader=True)
blinnSGName = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name=blinnName + "_SG")
cmds.connectAttr( blinnName + ".outColor", blinnSGName + ".surfaceShader", f=True)


'''
Final Version
'''

def createBlinn( shaderName ):
	blinnName = cmds.shadingNode( "blinn", asShader=True, name=shaderName)
	blinnSGName = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name=blinnName + "_SG")
	cmds.connectAttr( blinnName + ".outColor", blinnSGName + ".surfaceShader", f=True)
	return [blinnName, blinnSGName]
	
	
	

