"""Basic Ik Hand Attribute Adder"""

"""
Author: Jennifer Conley
Date Modified: 8/22/11

Description: Addes several basic attributes which I normally add to the Ik
Hand control.

How to run:
import basic_attrs_ik_hand
reload (basic_attrs_ik_hand)

"""

import maya.cmds as cmds

"""
Creates a list to cycle through. Ik Hand attributes will be added to 
everything within the list.
"""

my_sel = cmds.ls(sl=True)

for each in my_sel:
	"""Creates space switching attributes"""
	cmds.addAttr(each, ln='Space_Switching', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.Space_Switching', cb=True)
	cmds.addAttr(each, ln='Head', at='double', min=0, max=10,
		dv=0, k=True)
	cmds.addAttr(each, ln='Back', at='double', min=0, max=10,
		dv=0, k=True)
	cmds.addAttr(each, ln='Hips', at='double', min=0, max=10,
		dv=0, k=True)
	cmds.addAttr(each, ln='Locator', at='double', min=0, max=10,
		dv=0, k=True)
