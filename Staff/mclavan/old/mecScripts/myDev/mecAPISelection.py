

import maya.cmds as cmds
import maya.OpenMaya as om

# Get the selected dag nodes
selection = om.MSelectionList()
om.MGlobal.getActiveSelectionList(selection)

# print out what is selected
selItems = []
selection.getSelectionStrings(selItems)
print(selItems)

# print out the contents of the list one by one.
for i in range( 0, selection.length() ):
	selItem = []
	selection.getSelectionStrings(i, selItem)
	print(selItem[0])

# Print out the full & partial path
for i in range( 0, selection.length() ):
	# Get MDagPath object
	myDag = om.MDagPath()
	# Technically MSelection.getDagPath requires a MObject as well but these 
	# are used for components so if left off it will except Null.
	selection.getDagPath( i, myDag ) 
	
	# Get the full and partial path names
	fullPath = myDag.fullPathName()
	partialPath = myDag.partialPathName()
	# Print them out.
	print( "Object: %s  -  FullPath: %s" %(partialPath,fullPath))
	
	
	
# Returns optionVar values
om.MGlobal.optionVarDoubleValue( "")

# Selects the component by name
om.MGlobal.selectByName( "" )


