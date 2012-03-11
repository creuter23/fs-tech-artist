"""Rename Tool"""

"""
Author: Jennifer Conley
Date Modified: 8/23/11

Description: A rename tool to help quickly rename objects created inside of Maya.

How to run:
import rename_tool_v3
reload (rename_tool_v3)
rename_tool_v3.gui()

"""

import maya.cmds as cmds
win = 'rename_win'
scriptname = __name__
width = 400


"""
Creates the window for the rename tool
"""
def gui():
	if (cmds.window(win, q=True, ex=True)):
		cmds.deleteUI(win)
		
	global prefix, name, inc, suffix
		
	cmds.window(win, t='Rename Tool', w=width, h=300)
	main_layout = cmds.columnLayout(nch=2)
	cmds.rowColumnLayout(w=width, nc=4)
	
	cmds.text(w=(width/4), l='Prefix')
	cmds.text(w=(width/4), l='Name')
	cmds.text(w=(width/4), l='Instance')
	cmds.text(w=(width/4), l='Suffix')
	
	prefix = cmds.textField(w=(width/4), tx='')
	name = cmds.textField(w=(width/4), tx='')
	inc = cmds.intField(w=(width/4), v=0)
	suffix = cmds.textField(w=(width/4), tx='')

	cmds.setParent(main_layout)
	
	cmds.columnLayout(w=width, adj=True)
	cmds.button(l='Run Rename', c=scriptname + '.rn()')
	
	cmds.showWindow()
	
	
def rn():
	"""
	Creates the fuction to replace the old name with the 
	new name for selection
	"""
	my_sel = cmds.ls(sl=True)
	
	rn_prefix = cmds.textField(prefix, q=True, tx=True)
	rn_name = cmds.textField(name, q=True, tx=True)
	rn_inc = cmds.intField(inc, q=True, v=True)
	rn_suffix = cmds.textField(suffix, q=True, tx=True)


	for each in my_sel:
		if rn_prefix != '':
			new_pre = rn_prefix + '_'
		else:
			new_pre = ''
			
			
		if rn_inc > 0:
			new_inc = '_' + str(rn_inc)
			rn_inc += 1
		else:
			new_inc = ''	
			
		
		if rn_suffix != '':
			new_suf = '_' + rn_suffix
		else:
			new_suf = ''
			

		
		
		new_name = new_pre + rn_name + new_inc + new_suf	
		cmds.rename(each, new_name)
		
	
	
	
