

# Blend shapes

# How to create a blend shape (from scratch)
import maya.cmds as cmds

# blendshape command returns a list [u'blendShape1']
# cmds.blendshape( target, target, baseShape )
blend = cmds.blendShape( "a", "b", "base" )


# How to add a target shape to a blend shape
cmds.blendShape( blend, edit=True, target=["base", 3, "c", 1] )

# target flag
[string, int, string, float]
[baseShape, index, target, weight]
weight 

# How to list how many blend shapes are on an object.
# Returns a list of all the target attribute names
# ['a', 'b', 'c'] 
# target shapes id start at 1 NOT 0 so the index from the list is a little offset.
cmds.blendShape( blend, query=True, target=True)

# How to remove a blend shape.
#  blendShape -e  -tc 0 -rm -t base 3 a 1 -t base 3 base 1 base;
cmds.blendShape( base, e=1, tc=0, rm=True, t=[[base, 3, 'a', 1], [base, 3, base, 1]])
cmds.blendShape( 'base' , e=1, rm=True, t=[['base', 0, 'a', 1]])

# adding an inbetween
# shape c and d are apart of index 3 (which is called c)
# from 0 - 1, c target is used.  Then from 1-2 c is turned off and d is turned on.
cmds.blendShape( blend, edit=True, inBetween=True, target=["base", 3, "d", 2] )


# Deleting the blendShapes
# delete blendShape1;
cmds.delete( "blendShape1" )



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
		
	
'''
Using a dictionary.
'''
		
# Getting the blendShape(s) from a selected geometry
# Get first selected object
selected = cmds.ls(sl=True)[0]

# Get the shape nodes on the selected geometry.
shapes = cmds.listRelatives( selected, shapes=True )
# Creating an empty list to store the blendShape names.
blends = []
blendTargets = {}
# Loop through each shape node looking for blend shapes
for shape in shapes:
	# blend shapes are connected to shapde nodes the type flag here will only return connected blendShape nodes.
	conn = cmds.listConnections( shape, type="blendShape" )
	# If there is a least one blend shape then add it onto the blend list.
	if(conn):
		blends.extend(conn)
		for blend in blends:
			blendTargets[blend] = cmds.blendShape( blend, q=True, target=True )
			




