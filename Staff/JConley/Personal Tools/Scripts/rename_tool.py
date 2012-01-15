"""Rename Tool"""

"""
Author: Jennifer Conley
Date Modified: 8/23/11

Description: A rename tool to help quickly rename objects created 
	inside of Maya.

How to run:
import rename_tool
reload (rename_tool)
rename_tool.gui()

"""

import maya.cmds as cmds
import maya.mel as mel
win = 'rename_win'
scriptname = __name__
width = 200


"""
Creates the window for the rename tool
"""
def gui():
	if (cmds.window(win, q=True, ex=True)):
		cmds.deleteUI(win)
		
	global prefix, name, start_num, pad_num, division, search, replace, sel_hier
		
	cmds.window(win, t='Rename Tool', w=width, h=300)
	main_layout = cmds.columnLayout(w=width, nch=2)
	cmds.rowColumnLayout(w=width, nc=2)
	
	cmds.text(w=(width/2), l='Prefix:')
	prefix = cmds.textField(w=(width/2), tx='Prefix')
	
	cmds.text(w=(width/2), l='New Name:')
	name = cmds.textField(w=(width/2), tx='New Name')
	
	cmds.text(w=(width/2), l='Start Number:')
	start_num = cmds.intField(w=(width/2), min=0, max=999, v=1, s=1)
	
	cmds.text(w=(width/2), l='Padding:')
	pad_num = cmds.intField(w=(width/2), min=0, max=5, v=2, s=1)
	
	cmds.text(w=75, l='Divider:')
	division = cmds.radioButtonGrp(nrb=2, cw=[(1,40), (2,40)],
		labelArray2=('_', 'None'), sl=1)
	cmds.setParent(main_layout)
	
	
	cmds.columnLayout(w=width, adj=True)
	cmds.button(l='Rename', c=scriptname + '.run_rename()')
	cmds.setParent(main_layout)
	
	
	cmds.rowColumnLayout(w=width, nc=2)
	cmds.text(w=(width/2), l='Search:')
	search = cmds.textField(w=(width/2), tx='joint')
	
	cmds.text(w=(width/2), l='Replace:')
	replace = cmds.textField(w=(width/2), tx='Replace')
	cmds.setParent(main_layout)
	
	
	cmds.columnLayout(w=width, adj=True)
	sel_hier = cmds.radioButtonGrp(nrb=2, cw=[(1,(width/2)), (2,(width/2))], 
		labelArray2=('Selected', 'Hierarchy'), sl=1)
	cmds.button(w=75, l='Replace', c=scriptname + '.searchReplace()')

		
	cmds.showWindow()

def run_rename():
	"""
	Creates the fuction to rename an object based on user input.
	"""
	my_sel = cmds.ls(sl=True)
	count = len(my_sel)
	i = 0
	
	rn_pre = cmds.textField(prefix, q=True, tx=True)
	rn_name = cmds.textField(name, q=True, tx=True)	
	rn_start = cmds.intField(start_num, q=True, v=True)
	rn_pad = cmds.intField(pad_num, q=True, v=True)
	div_state = cmds.radioButtonGrp(division, q=True, sl=True)
	
	
	
	if (div_state == 1):
		divider = '_'
	else:
		divider = ''
	
	
	for each in my_sel:
		add_pad = ''
		number=0
		if (rn_start < count):
			number = i + rn_start
			i += 1
			j = 1
		
			if (j==1) or (j < rn_pad):
				j += j
		
				if (number < pow(10, j)):
					add_pad += '0'
		
					new_name = (rn_pre + divider + rn_name + divider
						+ add_pad + str(number))
					cmds.rename(each, new_name)


def searchReplace():
	"""
	Creates the fuction to search and replace text based on user input.
	"""
	search_type = cmds.radioButtonGrp(sel_hier, q=True, sl=True)
	search_txt = cmds.textField(search, q=True, tx=True)
	replace_txt = cmds.textField(replace, q=True, tx=True)
	
	if search_type == 1:
		mel.eval('searchReplaceNames search_txt replace_txt "selected"')
	else:
		mel.eval('searchReplaceNames search_txt replace_txt "hierarchy"')
	
	
