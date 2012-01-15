""" Group Orginization Script v2.0"""

""" 
Author: Jennifer Conley
Updated: 08/22/11

Description: This script is designed to help in the initial set up for creating 
a rig by automatically constructing most of the groups in the outliner. This
script should only be run once per program file.

How to run:
import groupScript
reload (groupScript)

"""

import maya.cmds as cmds

"""Creates Groups"""
cmds.group(em = True, w = True, n='Character')
cmds.group(em = True, w = True, n='Rig')
cmds.group(em = True, w = True, n='Controls')
cmds.group(em = True, w = True, n='Geometry')
cmds.group(em = True, w = True, n='Blend_Shapes')
cmds.group(em = True, w = True, n='DO_NOT_TOUCH')
cmds.group(em = True, w = True, n='Curves')
cmds.group(em = True, w = True, n='Clusters')


"""Selects all of the group nods"""
groups = cmds.ls('Character', 'Rig', 'Controls', 'Geometry', 'Blend_Shapes',
	'DO_NOT_TOUCH', 'Curves', 'Clusters')


"""Lock and Hide Unused Channels"""
for each in groups:
		cmds.setAttr(each + '.tx', l=True, k=False, cb=False)
		cmds.setAttr(each + '.ty', l=True, k=False, cb=False)
		cmds.setAttr(each + '.tz', l=True, k=False, cb=False)
		cmds.setAttr(each + '.rx', l=True, k=False, cb=False)
		cmds.setAttr(each + '.ry', l=True, k=False, cb=False)
		cmds.setAttr(each + '.rz', l=True, k=False, cb=False)
		cmds.setAttr(each + '.sx', l=True, k=False, cb=False)
		cmds.setAttr(each + '.sy', l=True, k=False, cb=False)
		cmds.setAttr(each + '.sz', l=True, k=False, cb=False)

"""Creating the Parenting"""
cmds.parent('Curves', 'Clusters', 'Blend_Shapes', 'DO_NOT_TOUCH')
cmds.parent('Rig', 'Controls', 'Geometry', 'DO_NOT_TOUCH', 'Character')


"""Clear Selection"""
cmds.select(cl=True)

