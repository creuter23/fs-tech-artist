'''
Michael Clavan
mecRenameAPI.py

Description:
	- This renaming script is different because it uses Maya's API to grab 
	  directly access the names of the objects.  So, it doesn't matter 
	  which heirarchy they belong to it still will stay connected.

How To Run:

import mecRenameAPI
mecRenameAPI.gui()

Debug:
import mecRenameAPI
reload(mecRenameAPI)
mecRenameAPI.gui()
'''

print( "mecRenameAPI imported" )

import maya.cmds as cmds
import maya.OpenMaya as om

'''
def nameToDag( name ):
> >  sel = api.MSelectionList()
> >  sel.add( name )
> >  node = api.MDagPath()
> >  sel.getDagPath( 0, node )
> >  return node
'''

# Get what is currently selected and rename them.

# Get what is currently selected

# Add what is currently selected.

def seq( curSeq, count ):
	'''
	Creates a sequence with the given arguments and then returns it as a list.
		- curSeq (string list) - 
		- count (int) - how many items to count through.
		- counter (which is the starting point of the counter)
	'''
	newSeq = curSeq
	

	# find the different
	# loop using that different 
	# starting and ending point will be offset by how many elements are in the seq - 1.

	# count = 10
	diff = count - len(newSeq) 
	if( diff > 0 ):

		for i in range( 0, diff ):
			counter = "%02d" %len(newSeq)
			newSeq.insert( len(newSeq)-1, str(counter) )
			
	return newSeq

def seqChar( curSeq, count ):
	'''
	Creates a sequence with the given arguments and then returns it as a list.
		- curSeq (string list) - 
		- count (int) - how many items to count through.
		- counter (which is the starting point of the counter)
	'''
	newSeq = curSeq[0:]
	

	# find the different
	# loop using that different 
	# starting and ending point will be offset by how many elements are in the seq - 1.

	# count = 10
	diff = count - len(newSeq) 
	stamp = newSeq[-2]
	if( diff > 0 ):

		for i in range( 0, diff ):
			if( len(newSeq) - 2 < 0 ):
				counter = "%02d" %len(newSeq)
			else:	
				counter = "%s%02d" %(curSeq[-2], len(newSeq))
			newSeq.insert( len(newSeq)-1, counter )
			
	return newSeq

def charSeq( reChar, start, count ):
	seq = []
	for i in range( start, count+1 ):
		seq.append( "%s%02d" %(reChar, i) )
		
	return seq
	
"""
seq = mecRenameAPI.seq( ['root', 'end'], len(cmds.ls(sl=True)) )
seq = mecRenameAPI.charSeq( "c", 1, len(cmds.ls(sl=True)) )
seq = mecRenameAPI.seqChar( ["arm", "elbow", "twist", "wrist"], len(cmds.ls(sl=True)) )
mecRenameAPI.rename( "ct", "back", seq, ["bind","end"] )



aList = ['a', 'b', 'c']
aList.insert(len(aList)-1, "b2" )
print( aList )

aList = ['shoulder', 'elbow', 'wrist']
count = 10
diff = count - len(aList) 
if( diff > 0 ):
	print("adding to seq")
	for i in range( 0, diff ):
		counter = "%02d" %len(aList)
		aList.insert( len(aList)-1, str(counter) )

print( aList )

# Adding a character to a sequence.
seq = []
char = "C"
# Adding to a seq
start = 1
count = 11
for i in range( start, count ):
	seq.append( "%s%02d" %(char, i) )	
print( seq )
"""

def rename( ori, name, seq, nType, un="_" ):
	'''
	This function will rename the selected sequence from the scene.
		ori(string) - is the orientation of the node.
		name(string) - is the name of the system. 
		seq(string list) - Numbering sequence
		nType(string list) - type of node.  It also allows you to end a 
			sequence with a different node type.
	'''
	
	# Grab what is currently selected.
	
	selected = om.MSelectionList()
	om.MGlobal.getActiveSelectionList(selected)
	
	
	
	for i in range( 0, selected.length() ):
		# compile the elements
		if( i == (selected.length() - 1) and (len(nType) != 1)):
			newName = ori + un + name + un + seq[i] + un + nType[1]
		else:
			newName = ori + un + name + un + seq[i] + un + nType[0]
		
		# Get the old name
		mDag = om.MDagPath()
		selected.getDagPath( i, mDag )
		
		oldName = mDag.fullPathName()
		if( not cmds.objExists(newName) ):
			newName = cmds.rename( oldName, newName )
			print( "Renaming %s  -->  %s" %(mDag.partialPathName(), newName))
		else:
			newNameTemp = cmds.rename( oldName, newName )
			om.MGlobal.displayWarning("\n\t%s already exists in the scene!  \n\tMaya's naming it %s" %(newName, newNameTemp) )
	

'''
selList = om.MSelectionList()
om.MGlobal.getActiveSelectionList(selList)

node = om.MDagPath()
selList.getDagPath( 0, node )
'''

# Getting the shapeNode (if only one)

# Getting how many shape nodes are below.


# Adding 

