'''
Blend Shapes
blendShapes.py

Description:
	This script covers the different ways to create and modify a blend shape through code.
	
How to Run:

'''

import maya.cmds as cmds

print("Blend Shapes")

'''
# Creating a new blendShape
'''
# cmds.blendshape( target, target, etc.., baseShape )
blend = cmds.blendShape( "a", "b", "base" )
# blendshape command returns a list [u'blendShape1']

'''
# deleting a blendShape (all targets)
'''
cmds.delete( 'blendShape1' )

'''
# Adding a target shape
'''
# How to add a target shape to a blend shape

# target flag
# target=["baseShape", index, "targetShape", weight]
# Querks
# weight is how much it targets to, so weight==1 means 0 -> 1
# index has to be unique (starts at 1 NOT 0)
cmds.blendShape( 'blendShape1', edit=True, target=["base", 3, "target", 1] )

# How to list how many blend shapes are on an object.
# Returns a list of all the target attribute names
# ['a', 'b', 'c'] 
cmds.blendShape( blend, query=True, target=True)
# index starts at 1 so index will be offset.

'''
# Removing Target Blend shape
'''
# Index is ignored blendShape and target matter.
cmds.blendShape( 'baseShape' , e=1, remove=True, target=[['baseShape', 1, 'a', 1]])


'''
Getting BlendShape Node
by selecting a piece of geometry.
'''
# Getting the blendShape(s) from a selected geometry
# Get first selected object
selected = cmds.ls(sl=True)[0]

# Get the shape nodes on the selected geometry.
shapes = cmds.listRelatives( selected, shapes=True )
# Creating an empty list to store the blendShape names.
blends = []

# Loop through each shape node looking for blend shapes
for shape in shapes:
	# blend shapes are connected to shapde nodes the type flag here will only return connected blendShape nodes.
	conn = cmds.listConnections( shape, type="blendShape" )
	# If there is a least one blend shape then add it onto the blend list.
	if(conn):
		blends.extend(conn)
		
		

