"""Basic Head Attribute Adder"""

"""
Author: Jennifer Conley
Date Modified: 8/22/11

Description: Addes several basic attributes which I normally add to the 
Head control.

How to run:
import basic_attrs_head
reload (basic_attrs_head)

"""

import maya.cmds as cmds

"""
Creates a list to cycle through. Head attributes will be added to everything
within the list.
"""

my_sel = cmds.ls(sl=True)

for each in my_sel:
	"""Creates control visiblity attributes"""
	cmds.addAttr(each, ln='Ctrl_Visibility', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.Ctrl_Visibility', cb=True)
	cmds.addAttr(each, ln='Face_Gui', at='bool', k=True)
	cmds.addAttr(each, ln='Eye_Ctrls', at='bool', k=True)
