"""Basic Ik Foot Attribute Adder"""

"""
Author: Jennifer Conley
Date Modified: 8/22/11

Description: Addes several basic attributes which I normally add to the Ik
Foot control.

How to run:
import basic_attrs_ik_foot
reload (basic_attrs_ik_foot)

"""

import maya.cmds as cmds

"""
Creates a list to cycle through. Ik Foot attributes will be added to 
everything within the list.
"""

my_sel = cmds.ls(sl=True)

for each in my_sel:
	
	
	"""Creates reverse foot Attribute"""
	cmds.addAttr(each, ln='Foot_SDKs', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.Foot_SDKs', cb=True)
	
	cmds.addAttr(each, ln='Foot_Roll', at='double', min=-10, max=10,
		dv=0, k=True)
	cmds.addAttr(each, ln='Bank', at='double', min=-360, max=360,
		dv=0, k=True)	
	
	"""Creates foot raise attributes"""
	cmds.addAttr(each, ln='Raises', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.Raises', cb=True)
	cmds.addAttr(each, ln='Toe_Raise', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Ball_Raise', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Heel_Raise', at='double', min=-360, max=360,
		dv=0, k=True)


	"""Creates foot grind attributes"""
	cmds.addAttr(each, ln='Grinds', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.Grinds', cb=True)
	cmds.addAttr(each, ln='Toe_Grind', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Ball_Grind', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Heel_Grind', at='double', min=-360, max=360,
		dv=0, k=True)
	
	
	"""Creates no-flip-leg attributes"""
	cmds.addAttr(each, ln='Knee_PV', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.Knee_PV', cb=True)
	cmds.addAttr(each, ln='Knee', at='double', min=-360, max=360,
		dv=0, k=True)
	cmds.addAttr(each, ln='Offset', at='double', min=-360, max=360,
		dv=0, k=True)
	
	
	"""Creates space switching attributes"""
	cmds.addAttr(each, ln='Space_Switching', at='enum', en='----------:Blue')
	cmds.setAttr(each + '.Space_Switching', cb=True)
	cmds.addAttr(each, ln='Cog', at='double', min=0, max=10,
		dv=0, k=True)
	cmds.addAttr(each, ln='Locator', at='double', min=0, max=10,
		dv=0, k=True)

