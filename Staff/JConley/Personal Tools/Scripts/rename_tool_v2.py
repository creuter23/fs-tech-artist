"""Rename Tool"""

"""
Author: Jennifer Conley
Date Modified: 8/23/11

Description: A rename tool to help quickly rename objects created inside of Maya.

How to run:
import rename_tool_v2
reload (rename_tool_v2)
rename_tool_v2.gui()

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
		
	global prefix, name, suffix
		
	cmds.window(win, t='Rename Tool', w=500, h=300)
	main_layout = cmds.columnLayout(nch=2)
	cmds.rowColumnLayout(nc=3)
	
	cmds.text(l='Prefix')
	cmds.text(l='Name')
	cmds.text(l='Suffix')
	
	prefix = cmds.textField(tx='')
	name = cmds.textField(tx='')
	suffix = cmds.textField(tx='')

	cmds.text(l='')
	cmds.button(l='Run Rename', c=scriptname + '.rn()')
	
	cmds.showWindow()

def rn():
	"""
	Creates the fuction to replace the old name with the new name for selection
	"""
	my_sel = cmds.ls(sl=True)
	
	rn_prefix = cmds.textField(prefix, q=True, tx=True)
	rn_name = cmds.textField(name, q=True, tx=True)
	rn_suffix = cmds.textField(suffix, q=True, tx=True)


	for each in my_sel:
		if rn_prefix != '':
			new_pre = rn_prefix + '_'
		else:
			new_pre = ''
			
			
		if rn_suffix != '':
			new_suf = '_' + rn_suffix
		else:
			new_suf = ''
		
		new_name = new_pre + rn_name + new_suf	
		cmds.rename(each, new_name)
	



