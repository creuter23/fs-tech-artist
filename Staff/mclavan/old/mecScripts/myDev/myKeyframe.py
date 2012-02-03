'''
Keyframe option

'''

import maya.cmds as cmds


def createKeyAttr():
	'''
	
	'''
	
	# if the attribute doesn't exists
	# attribute query
	# cmds.attributeQuery( 
	# dt(dataType) == used for strings
	cmds.addAttr( ln="attr_all", dt="string" )
# Create attributes on the objects that have the attribute to keyframe.


# Loop to loop through the selected objects and selected channel box
# 	to add an attribute with the selected names.


# Code to add attribute

# Code to grab selected channelbox and selected objects.

def addAttrs(attr="attr_all"):
	selected = cmds.ls(sl=True)
	cbSelected = cmds.channelBox("mainChannelBox", q=True, selectedMainAttributes=True)
	
	
	for sel in selected:
		if(cbSelected):
			attrs = addSeq(cbSelected, sel+"."+attr)
			attrs = cmds.getAttr(sel + "." + attr) + attrs
			cmds.setAttr( sel+"."+attr, attrs, type="string")
		else:
			keyAttrs=cmds.listAttr(sel, sn=True, k=True)
			attrs = addSeq(keyAttrs, sel+"."+attr)
			attrs = cmds.getAttr(sel + "." + attr) + attrs
			cmds.setAttr( sel+"."+attr, attrs, type="string")
	
def addSeq(attrs, dest):
	'''
		attrs(string[]) == ['tx', 'ty', 'tz']
		dest(string) == "object.attr"
	'''

	destAttrs = cmds.getAttr(dest)
	addAttrs = ""

	if( destAttrs ):
		for sAttr in attrs:
			if( sAttr not in destAttrs ):
				addAttrs += " " + sAttr
				print(addAttrs)
	else:
		addAttrs = " ".join(attrs)
		
	return addAttrs

def keyframe(attr="attr_all"):
	selected = cmds.ls(sl=True)
	for sel in selected:
		attrs = cmds.getAttr(sel+"."+attr).split()
		for at in attrs:
			cmds.setKeyframe(sel+"."+at)
		
# addSeq(cmds.listAttr( sn=True, k=True),  'pSphere1.attr_all')
	
	
	

