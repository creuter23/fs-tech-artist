'''
Attribute reset script
mecAttrReset.py


How to use:
import mecAttrReset



'''
# The next step would be getting all the keyable attributes from each selected object.

import maya.cmds as cmds

def attrReset( ):
	'''
	This function will reset the attributes on the selected objects in the scene.

	'''
	selected = cmds.ls(sl=True)
	
	# selCB = cmds.channelBox( "mainChannelBox", q=True, sma=True)
	
	for sel in selected:
		# Gathering all the attributes from the object.
		selCB = cmds.listAttr(sel, k=True)
		# Duplicating list because removing from the list your are looping through causes problems.
		newAttrs = selCB[:]
		try:
			[selCB.remove(x) for x in newAttrs if x in cmds.listAttr( selected , k=True, l=True )]
		except TypeError:
			print( "None of the attributes are locked.")
		for attr in selCB:
			attrName = "%s.%s" %(sel,attr)
			print(attrName)

			# Check to see if keyable
			if( cmds.getAttr( attrName, k=True) ):
				# Get default value
				# cmds.attributeQuery( "sx", node="nurbsCircle1", listDefault=True )
					
				attrDV = cmds.attributeQuery( attr, node=sel, listDefault=True)[0]
				print( "Object: %s Setting to Default: %s" %(attrName, attrDV))
				cmds.setAttr( attrName, attrDV )
	
def attrReset2( obj ):
	'''
	This function will reset the attributes to of the given object their default values 
	'''
	# Channel box is required so the object will have to be selected to have this work.
	# selCB = cmds.channelBox( "mainChannelBox", q=True, sda=True)
	selCB = cmds.listAttr(sel, k=True)
		
	for attr in selCB:
		attrName = "%s.%s" %(obj,attr)
		
		# Check to see if keyable
		if( cmds.attributeQuery( attr, node=sel, k=True )):
			# Get default value
			# cmds.attributeQuery( "sx", node="nurbsCircle1", listDefault=True )
			attrDV = cmds.attributeQuery( attr, node=sel, listDefault=True)[0]
			cmds.setAttr( attrName, attrDV )
