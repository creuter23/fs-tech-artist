'''
Nodes
Modifing Node Values
Nodes3.py

Description:
	- This script covers different ways how to get and set values of a node.
	
How to Run:

import nodes3
reload( nodes3 )
'''


'''
getAttr and setAttr commands
'''

blinnName = cmds.shadingNode( "blinn", asShader=True)
blinnSGName = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name=blinnName + "_SG")
cmds.connectAttr( blinnName + ".outColor", blinnSGName + ".surfaceShader", f=True)

# Change color to red.
# setAttr "blinn1.color" -type double3 1 0 0.0303049 ;
# cmds.setAttr( "blinn1.color", 1, 0, 0, type="double3" )

cmds.setAttr( blinnName + ".color", 1, 0, 0, type="double3" )


# getting values
value = cmds.getAttr( blinnName + ".color" )
print(value[0])
# Result: [(1.0, 0.0, 0.030304908752441406)] # 
print(value[0]) # Color List (R,G,& B)
print(value[0][0]) # Red Channel


'''
Final Version
'''
def createBlinn( shaderName ):
	blinnName = cmds.shadingNode( "blinn", asShader=True, name=shaderName)
	blinnSGName = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name=blinnName + "_SG")
	cmds.connectAttr( blinnName + ".outColor", blinnSGName + ".surfaceShader", f=True)
	cmds.setAttr( blinnName + ".color", 1, 0, 0, type="double3" )
	return [blinnName, blinnSGName]
	
def createBlinn2( shaderName, color=[1,0,0] ):
	blinnName = cmds.shadingNode( "blinn", asShader=True, name=shaderName)
	blinnSGName = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name=blinnName + "_SG")
	cmds.connectAttr( blinnName + ".outColor", blinnSGName + ".surfaceShader", f=True)
	cmds.setAttr( blinnName + ".color", color[0], color[1], color[2], type="double3" )
	return [blinnName, blinnSGName]	
