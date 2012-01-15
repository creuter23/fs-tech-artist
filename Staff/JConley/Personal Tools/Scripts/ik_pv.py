"""Ik Pv Plane Creation"""

"""
Author: Jennifer Conley
Date Modified: 9/10/11

Description: A script used to quickly create a plane for the correct placement
of ik pv icons from a joint chain selection.


How to run:
import ik_pv
reload (ik_pv)


"""
import maya.cmds as cmds

cmds.select(hierarchy=True)

sel = cmds.ls(sl=True)
position_list = []

for each in sel:
	space = cmds.xform(each, q=True, t=True, ws=True)
	position_list.append(space)
	
	
print position_list
cmds.polyCreateFacet(ch=True, tx=1, s=1, p=position_list)

