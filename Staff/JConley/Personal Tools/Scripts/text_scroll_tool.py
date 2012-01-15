"""Text Scroll List"""

"""
Author: Jennifer Conley
Date modified: 9/9/11

Description: A tool to allow for the easy creation of commenly used utility
nodes as well as the display of them in a list which can be sorted based on
name, and type.

How to run:
import text_scroll_tool
reload (text_scroll_tool)
text_scroll_tool.gui()

"""

import maya.cmds as cmds


win = 'text_scroll_win'
scriptname = __name__
width=100

test_list = ['one','two','three','four','five','six','seven','eight','nine']

"""
Creates the window for the tool
"""
def gui():
	global txt_list
	
	if (cmds.window(win, q=True, ex=True)):
		cmds.deleteUI(win)
		
	cmds.window(win, w=170)
	main_layout= cmds.columnLayout(adj=True)
	
	cmds.paneLayout(cn='vertical2', w=width)
	txt_list = cmds.textScrollList(w=width, a=test_list)
	
	cmds.columnLayout(adj=True, w=width/2)
	cmds.button(l='Move Up', w=width/1.5, c=scriptname + '.move_up()')
	cmds.button(l='Move Down', w=width/1.5, c=scriptname + '.move_down()')
	cmds.button(l='Delete', w=width/1.5, c=scriptname + '.remove_item()')
	
	cmds.text(l='Sort')
	cmds.button(l='ABC', w=width/1.5, c=scriptname + '.sort_abc()')
	cmds.button(l='Type', w=width/1.5)
	cmds.button(l='Default', w=width/1.5, c=scriptname + '.sort_default()')
	cmds.setParent(main_layout)
	
	cmds.separator(w=width, h=5)
	cmds.text(l='Create')
	
	cmds.rowColumnLayout(nc=2)
	cmds.button(l='pmAvg', w=width/4)
	cmds.button(l='multDiv', w=width/4)
	
	cmds.showWindow(win)
	

def move_up():
	"""
	Moves the selected item up inside of the text list
	"""
		
	new_list = cmds.textScrollList(txt_list, q=True, ai=True)
	index_num = cmds.textScrollList(txt_list, q=True, sii=True)

	num = index_num[0]-1
	name = new_list[num]
	remove_num = index_num[0]+1

	cmds.textScrollList(txt_list, e=True, ap=(num, name))

	cmds.textScrollList(txt_list, e=True, rii=remove_num)
	cmds.textScrollList(txt_list, e=True, sii=num)
	print 'Selected item has been moved up inside of the list.'
	
def move_down():
	"""
	Move the selected item down inside of the text list
	"""
	
	new_list = cmds.textScrollList(txt_list, q=True, ai=True)
	index_num = cmds.textScrollList(txt_list, q=True, sii=True)
	
	num = index_num[0]
	name = new_list[num]
	remove_num = num + 2

	cmds.textScrollList(txt_list, e=True, ap=(num, name))
	
	cmds.textScrollList(txt_list, e=True, rii=remove_num)
	print 'Selected item has been moved down inside of the list.'
	
def remove_item():
	"""
	Removes selected item from the list
	"""
	item = cmds.textScrollList(txt_list, q=True, sii=True)
	cmds.textScrollList(txt_list, e=True, rii=item)
	
def sort_abc():
	new_list = cmds.textScrollList(txt_list, q=True, ai=True)
	new_list.sort()
	
	cmds.textScrollList(txt_list, e=True, ra=True)
	cmds.textScrollList(txt_list, e=True, a=new_list)
	
	print new_list
	
def sort_default():
	new_list = cmds.textScrollList(txt_list, q=True, ai=True)
	cmds.textScrollList(txt_list, e=True, ra=True)
	cmds.textScrollList(txt_list, e=True, a=test_list)	
	
	
	




	

	
	

	
	
	
	
	
	
	
	
	
