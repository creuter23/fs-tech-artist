"""Basic Attribute IkFk Foot Swithc"""

"""
Author: Jennifer Conley
Date Modified: 8/22/11

Descritpion: Addes several basic attributes which I normally add to the IkFk
Foot icon control.

How to run:
import basic_attrs_ikfk_foot
reload (basic_attrs_ikfk_foot)

"""

import maya.cmds as cmds

"""
Creates a list to cycle through. IkFk Foot Switch attributes will be added to
everything within the list.
"""

my_sel = cmds.ls(sl=True)

for each in my_sel:
	"""Creates IkFk switch attribute"""
	cmds.addAttr(each, ln='Ik_Fk_Switch', at='double', min=0, max=10,
		dv=0, k=True)
	
	"""Creates visibility switch for individual fk controls"""
	cmds.addAttr(each, ln='Indiv_Ctrls', at='bool', k=True)
	
	
	"""Creates the toe Fk attributes"""
	cmds.addAttr(each, ln='ToeSDKs', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.ToeSDKs', cb=True)
	
	cmds.addAttr(each, ln='All_Curl', at='double', min=-360, max=360,
		dv=0, k=True)
	
	"""Big toe curl Attributes"""
	cmds.addAttr(each, ln='Big_Curl', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.Big_Curl', cb=True)
	cmds.addAttr(each, ln='Big_Root', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Big_Mid', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Big_End', at='double', min=-360, max=360,
		dv=0, k=True)

	"""Index toe curl Attributes"""
	cmds.addAttr(each, ln='Index_Curl', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.Index_Curl', cb=True)
	cmds.addAttr(each, ln='Index_Root', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Index_Mid', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Index_End', at='double', min=-360, max=360,
		dv=0, k=True)

	"""Mid toe curl Attributes"""
	cmds.addAttr(each, ln='Mid_Curl', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.Mid_Curl', cb=True)
	cmds.addAttr(each, ln='Mid_Root', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Mid_Mid', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Mid_End', at='double', min=-360, max=360,
		dv=0, k=True)

	"""Fourth toe curl Attributes"""
	cmds.addAttr(each, ln='Fourth_Curl', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.Fourth_Curl', cb=True)
	cmds.addAttr(each, ln='Fourth_Root', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Fourth_Mid', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Fourth_End', at='double', min=-360, max=360,
		dv=0, k=True)
	
	"""Pinky toe curl Attributes"""
	cmds.addAttr(each, ln='Pinky_Curl', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.Pinky_Curl', cb=True)
	cmds.addAttr(each, ln='Pinky_Root', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Pinky_Mid', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Pinky_End', at='double', min=-360, max=360,
		dv=0, k=True)
	
	"""Creates the toe spread attributes"""
	cmds.addAttr(each, ln='Spreads', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.Spreads', cb=True)
	cmds.addAttr(each, ln='Big_Spread', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Index_Spread', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Mid_Spread', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Fourth_Spread', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Pinky_Spread', at='double', min=-360, max=360,
		dv=0, k=True)	
	
	
	

