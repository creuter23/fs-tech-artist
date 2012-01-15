""" Three Point Light Setup v2"""

"""

Author: Jennifer Conley
Update: 8/22/11

Description: This is a simple script to quickly set up a basic light setup. 
Three lights will be created and parented to a locator and their values for
shadow rays and other attributes will be set to defaults that I typically use.

How to run:
import three_point_lights
reload(three_point_lights)

"""

import maya.cmds as cmds

"""Creates a locator to parent the lights to"""

cmds.spaceLocator()
cmds.rename('locator1', 'lightLoc')

cmds.circle(nr=(0,1,0), c=(0, 0, 0))
cmds.select('nurbsCircleShape1', 'lightLoc', add = True)
cmds.parent(r = True, s = True)

cmds.select('nurbsCircle1')
cmds.delete()


"""Creates the key light and sets light attributes"""

cmds.spotLight(n='keyLight', d=2, i=400, rs=True)

cmds.move(-10,5,0)
cmds.rotate(0,-90,0)
cmds.setAttr('keyLightShape.shadowRays', 16)
cmds.parent('keyLight', 'lightLoc')


"""Creates the fill light and sets light attributes"""

cmds.spotLight(n='fillLight', d=2, i=300, rs=True)

cmds.move(10,0,0)
cmds.rotate(25,90,0)
cmds.setAttr('fillLightShape.shadowRays', 16)
cmds.parent('fillLight', 'lightLoc')


"""Creates the back light and sets light attributes"""

cmds.spotLight(n='backLight', d=2, i=300, rs=True)

cmds.move(0,8,-10)
cmds.rotate(-35,180,0)
cmds.setAttr('backLightShape.shadowRays', 16)
cmds.parent('backLight', 'lightLoc')






