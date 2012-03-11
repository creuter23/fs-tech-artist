"""Rename Tool"""

"""
Author: Jennifer Conley
Date Modified: 8/23/11

Description: A rename tool to help quickly rename objects created inside of Maya.

How to run:
import rename_tool_v1
reload (rename_tool_v1)
rename_tool_v1.gui()

"""

import maya.cmds as cmds
win = 'rename_win'
scriptname = __name__


"""
Creates the window for the rename tool
"""
def gui():
	if (cmds.window(win, q=True, ex=True)):
		cmds.deleteUI(win)
		
	global name
		
	cmds.window(win, t='Rename Tool', w=500, h=300)
	
	
	main_layout = cmds.columnLayout(nch=2)
	cmds.rowColumnLayout(nc=2)
		
	cmds.text(l='New Name')
	name = cmds.textField(tx='Name')
	
	cmds.button(l='Run Rename', c=scriptname + '.rn()')
	
	cmds.showWindow()
	
def rn():
	"""
	Creates the fuction to replace the old name with the new name for selection
	"""
	my_sel = cmds.ls(sl=True)
	
	for each in my_sel:
		rn_name = cmds.textField(name, q=True, tx=True)
		cmds.rename(each, rn_name)
