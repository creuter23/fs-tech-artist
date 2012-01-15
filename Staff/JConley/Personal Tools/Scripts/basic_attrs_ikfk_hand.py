"""Basic IkFk Hand Attribute Adder"""

"""
Author: Jennifer Conley
Date Modified: 8/22/11

Description: Addes several basic attributes which I normally add to the IkFk
Hand Switch control.

How to run:
import basic_attrs_ikfk_hand
reload (basic_attrs_ikfk_hand)

"""

import maya.cmds as cmds

"""
Creates a list to cycle through. IkFk Hand attributes will be added to 
everything within the list.
"""

my_sel = cmds.ls(sl=True)

for each in my_sel:
	"""Creates IkFk switch attribute"""
	cmds.addAttr(each, ln='Ik_Fk_Switch', at='double', min=0, max=10,
		dv=0, k=True)
	
	"""Creates visibility switch for individual fk controls"""
	cmds.addAttr(each, ln='Indiv_Ctrls', at='bool', k=True)
	
	"""Creates the finger Fk attributes"""
	cmds.addAttr(each, ln='Finger_SDKs', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.Finger_SDKs', cb=True)
	
	cmds.addAttr(each, ln='All_Curl', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='All_Spread', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='All_Flat', at='double', min=-360, max=360,
		dv=0, k=True)
	
	"""Thumb curl attributes"""
	cmds.addAttr(each, ln='Thumb_Curl', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.Thumb_Curl', cb=True)
	cmds.addAttr(each, ln='Thumb_Drop', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Thumb_Root', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Thumb_Mid', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Thumb_End', at='double', min=-360, max=360,
		dv=0, k=True)

	"""Index finger curl attributes"""
	cmds.addAttr(each, ln='Index_Curl', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.Index_Curl', cb=True)
	cmds.addAttr(each, ln='Index_Root', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Index_Mid', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Index_End', at='double', min=-360, max=360,
		dv=0, k=True)

	"""Mid finger curl attributes"""
	cmds.addAttr(each, ln='Mid_Curl', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.Mid_Curl', cb=True)
	cmds.addAttr(each, ln='Mid_Root', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Mid_Mid', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Mid_End', at='double', min=-360, max=360,
		dv=0, k=True)

	"""Ring finger curl attributes"""
	cmds.addAttr(each, ln='Ring_Curl', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.Ring_Curl', cb=True)
	cmds.addAttr(each, ln='Ring_Root', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Ring_Mid', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Ring_End', at='double', min=-360, max=360,
		dv=0, k=True)
	
	"""Pinky finger curl attributes"""
	cmds.addAttr(each, ln='Pinky_Curl', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.Pinky_Curl', cb=True)
	cmds.addAttr(each, ln='Pinky_Root', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Pinky_Mid', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Pinky_End', at='double', min=-360, max=360,
		dv=0, k=True)
	
	"""Creates the finger spread attributes"""
	cmds.addAttr(each, ln='Spreads', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.Spreads', cb=True)
	cmds.addAttr(each, ln='Thumb_Spread', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Index_Spread', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Mid_Spread', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Ring_Spread', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Pinky_Spread', at='double', min=-360, max=360,
		dv=0, k=True)	
	
	
	
	
	
	
	
	
	
