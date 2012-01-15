"""Basic COG Attribute Adder"""

"""
Author: Jennifer Conley
Date Modified: 8/22/11

Description: Addes several basic attributes which I normally add to the COG
icon control.

How to run:
import basic_attrs_cog
reload (basic_attrs_cog)

"""

import maya.cmds as cmds

"""
Creates a list to cycle through. Cog attributes will be added to everything 
within the list.
"""

my_sel = cmds.ls(sl=True)

for each in my_sel:
	cmds.addAttr(each, ln='Adv_Back', at='enum', en='----------:Blue:')
	cmds.setAttr(each + '.Adv_Back', cb=True)
	cmds.addAttr(each, ln='Back_Ctrls', at='enum', en='Fk_Ctrls:Ik_Ctrls:Both:None', k=True)
	
	cmds.addAttr(each, ln='Other', at='enum', en='----------:Blue:')
	cmds.setAttr(each + '.Other', cb=True)
	cmds.addAttr(each, ln='Res', at='enum', en='Low:Proxy:High', k=True)
	cmds.addAttr(each, ln='Auto_Hips', at='bool', k=True)

