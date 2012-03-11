"""Basic Eye Attribute Adder"""

"""
Author: Jennifer Conley
Date Modified: 8/22/11

Description: A script I use to set up the basic attributes associated with the 
main eye control icon.

How to run:
import basic_attrs_eyes
reload (basic_attrs_eyes)

"""

import maya.cmds as cmds

"""
Creates a list to cycle through. Eye attributes will be added to everything 
within the list.
"""

my_sel = cmds.ls(sl=True)

for each in my_sel:
	cmds.addAttr(each, ln='CtrlVis', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.CtrlVis', cb=True)
	cmds.addAttr(each, ln='IndivCtrls', at='bool', k=True)

