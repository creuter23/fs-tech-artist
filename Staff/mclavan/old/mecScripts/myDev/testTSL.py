'''
Michael Clavan
testTSL.py

Description:
	Testing the TextScrollList Class
	
How to Run:
	
import testTSL
testTSL.gui()

'''

# import mecTest.guiTest as gui
# from mecTest.guiTest import TextScrollList
import textScrollList as tsl
import maya.cmds as cmds
from mecMaya.callback import Callback
print( "Testing my tsl class" )

scriptName = __name__

def gui():
	cmds.window()
	cmds.columnLayout()
	global myTsl
	myTsl = tsl.TextScrollList(150, 200, items=cmds.ls(sl=True))
	cmds.button( label="Remove All",
		c=scriptName + ".myTsl.remAllItems()")
	cmds.button( label="Remove Sel",
		c=scriptName + ".myTsl.remSelItems()")
	cmds.button( label="Add Sel",
		c=Callback(addSel) )
	cmds.showWindow()

def addSel(imArg1, imArg2, v=0, *args):
	myTsl.append( cmds.ls(sl=True) )

	
	
	
