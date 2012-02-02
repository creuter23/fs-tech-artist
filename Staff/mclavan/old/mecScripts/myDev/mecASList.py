'''
Active Selected List
mecASList.py

Description:
	- This script shows you what is currently selected in your scene.
	- Options include:
		- Live Monitoring or Refresh
		- Change order of selection queue
		- Remove elements from the selection queue.
	- Etras:
		- Saving selection queues.
		- Drag and drop positioning.
'''

print( "Action Selection List script loaded." )

import maya.cmds as cmds


win = "mecASLWin"
winWidth = 300
winHeight = 300

def gui():
	'''
	Generates the interface for the script.
	'''
	
	if( cmds.window(win, q=True, ex=True) ):
		cmds.deleteUI(win)
		
	cmds.window(win, title="Active Selection List", w=winWidth, h=winHeight )
	mainCol = cmds.columnLayout()
	
	global tsl
	tsl = cmds.textScrollList( w=winWidth-5, h=200, ams=True, append=cmds.ls(sl=True))
	
	cmds.button( label="Live", w=75,
		c="")
	cmds.buton
	cmds.showWindow(win)
	
