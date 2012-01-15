"""Key Attributes Tool"""

"""
Author: Jennifer Conley
Date Modified: 10/09/11

Description: A GUI used to easily key the min and max values for SDKs simultaneously

How to run:
import key_attr_tool
reload (key_attr_tool)
key_attr_tool.gui()

"""


import maya.cmds as cmds

win = 'key_attr_tool'
width=200


def gui():
    global attr_field, attr_min, attr_max, button_grp
    
    if(cmds.window(win, q=True, ex=True)):
        cmds.deleteUI(win)
        
    cmds.window(win, w=width)
    
    main = cmds.columnLayout(w=width)
    
    cmds.separator(w=width, h=5)
    cmds.text(l='Select the joint to be keyed.', w=width)
    cmds.text(l='Select the control with the driver.', w=width)
    cmds.separator(w=width, h=5)

    
    cmds.rowColumnLayout(nc=2, w=width)
    cmds.text(l='Attribute',w=50)
    attr_field = cmds.textField(w=150)
    
    cmds.text(l='Axis', w=50)
    button_grp = cmds.radioButtonGrp(la3=('X', 'Y', 'Z'), nrb=3, cw3=(30, 30, 30))
    cmds.setParent(main)
    
    cmds.separator(w=width, h=5)
    
    cmds.rowColumnLayout(nc=4, w=width)
    cmds.text(l='Min', w=50)
    attr_min = cmds.intField(v=-360, w=50)
    cmds.text(l='Max', w=50)
    attr_max = cmds.intField(v=360, w=50)
    cmds.setParent(main)
    
    cmds.separator(w=width, h=5)
    cmds.button(l='Run', w=width, c=key_attr)
    

    
    cmds.showWindow(win)


def key_attr(*args):
    selection = cmds.ls(sl=True)
    attr_name = cmds.textField(attr_field, q=True, tx=True)
    key_min = cmds.intField(attr_min, q=True, v=True)
    key_max = cmds.intField(attr_max, q=True, v=True)
    axis = cmds.radioButtonGrp(button_grp, q=True, sl=True)
    
    if selection != 2:
    	    print 'Your selection is incorrect.'
    
    if axis == 1:
        axis = 'x'
    elif axis == 2:
        axis = 'y'
    elif axis == 3:
        axis = 'z'
    else:
    	print 'Must have an asix selected.'
    
    key_min = -key_min
    key_max = -key_max
    
    driver = selection[1] + '.' + attr_name
    driven = selection[0] + '.r' + axis
    print driver
    print driven
    
    cmds.setAttr(driver, 0)
    cmds.setAttr(driven, 0)
    cmds.setDrivenKeyframe(driven, cd=driver)  
    
    cmds.setAttr(driver, key_min)
    cmds.setAttr(driven, key_min)
    cmds.setDrivenKeyframe(driven, cd=driver)
    
    cmds.setAttr(driver, key_max)
    cmds.setAttr(driven, key_max)
    cmds.setDrivenKeyframe(driven, cd=driver)
    
    cmds.setAttr(driver, 0)
    
    