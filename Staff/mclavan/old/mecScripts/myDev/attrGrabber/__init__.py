"""
Attribute Grabber Script
The purpose of this script is to create a gui container that will allow the 
user to get easy access to attribute in one location.

Each attribute that is requested will have the ability to keyframe, reset to default, create and reset to an offset.

The script is broken down a bunch of smaller classes so it can be used in different situations.

How To Run:

import attrGrabber.attr as attr

"""
"""
import attrGrabber.attr as attr2
reload(attr2)

import attrGrabber as attr
reload(attr)
attr.gui()

"""



from attr import *
import maya.cmds as cmds
from callback import Callback

def gui():
	win = "mecAttrGWin"
	if( cmds.window( win, ex=True)):
		cmds.deleteUI(win)
	if( cmds.windowPref(win, ex=True)):
		cmds.windowPref(win, remove=True)
		
	cmds.window( win, title="Attribute Grabber", width=450, h=400, menuBar=True )

	
	tab = TabGroup(win)	

	cmds.menu(label="Attributes")
	cmds.menuItem(label="Add Tab",
				  command=Callback(tab.addTabPrompt))
	cmds.menuItem(label="Add Tab (file)",
		command=Callback(tab._loadTab))
	cmds.menuItem(label="Save Tab",
		command=Callback(tab._saveTab))
	cmds.menuItem(label="Remove Tab",
		command=Callback(tab._removeTab))
	cmds.menuItem(divider=True)
	
	cmds.menuItem(label="Add Frame",
	   command=Callback(tab.addFramePrompt))
	cmds.menuItem(label="Add Frame (file)")
	cmds.menuItem(label="Save Frame")
	cmds.menuItem(label="Remove Frame")
		
	
	cmds.menuItem(divider=True)
	
	
	cmds.menu(label="About")
		
	
	cmds.showWindow()



"""
# Test Code
import maya.cmds as cmds
from attrGrabber import attr
reload(attr)


win = cmds.window()
mainCol = cmds.columnLayout()
attrGUI = attr.AttrGroup(mainCol)
cmds.showWindow(win)

help(attrGUI)
attrGUI.addAttrGUI()
"""










































