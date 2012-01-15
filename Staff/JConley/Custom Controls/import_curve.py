"""Curve Import"""

"""
Author: Jennifer Conley
Date Modified: 9/10/11

Description: A script used to demestrate the ability to import custom curve 
icons into maya through Illistrator paths.

How to run:
import import_curve
reload (import_curve)


"""
import maya.cmds as cmds
import maya.mel as mel

cmds.file('Autodesk/maya/2011-x64/prefs/icons/icon.ai',
	i=True, type='Adobe(R) Illustrator(R)', ra=True, ns='icon', gr=True,
	gn='icon_pad', pr=True, lrd='all')
print 'Illustrator Path has been imported'

cmds.select('icon_pad')
cmds.ungroup()
cmds.ungroup()
curves = cmds.ls(sl=True)
shapes = cmds.pickWalk(d='down')
print 'Curves have been selected and ungrouped'


cmds.select(shapes[1], curves[0])
cmds.parent(r=True, s=True)
print 'Curves have been combined to a single object'

final = curves[0]
curves.pop(0)
cmds.delete(curves)
cmds.select(final)
mel.eval('CenterPivot')
print 'Unused groups have been deleted'







