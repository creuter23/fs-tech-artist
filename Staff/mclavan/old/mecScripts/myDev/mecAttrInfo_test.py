'''
Finding information on attributes different ways.
mecAttrInfo_test.py

This script provides information on gathering information about attributes.

New name for all information scripts.
info_attrs.py
info_errors.py
info_panel.py
info_formLayout.py

import mecAttrInfo_test
reload(mecAttrInfo_test)

Main commands used here are:
	listAttr
	attributeQuery
	attributeInfo (this command only works on types of nodes, not on individually created ones)
I need to be able to get all the attribute of a given nodes.
- I need to have it return only specific nodes that pop up in the channelbox.


- Check attribute query
'''


# This is giving me some weird results.

import maya.cmds as cmds

keyAttrs = cmds.listAttr( 'ball', k=True )

# Returns which in the channel box is locked. ( can't set l=False and return those that are not locked.)
# Also k=True WILL return locked attributes.
keyAttrs = cmds.listAttr('ball', k=True, l=True)
print(keyAttrs)

# Getting the keyable attributes (what's in the channelbox) of a selected object.
selected = cmds.ls(sl=True)
cmds.listAttr( selected[0] , k=True ) # First item selected.

# Get the blend shape attributes
# [u'envelope', u'a', u'b', u'c', u'd']
# envelope
blendAttrs = cmds.listAttr('ball', multi=True, k=True )
blendAttrs.remove('envelope')
print(blendAttrs)

# Create sliders based on the blend shape nodes

# Reset blendshapes

# Create 
