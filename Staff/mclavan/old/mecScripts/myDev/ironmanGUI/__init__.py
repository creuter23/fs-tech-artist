'''
Ironman Character GUI
'''
import maya.cmds as cmds
import os, os.path
import mecCharGUIGen as charGUI


imgPath = __path__

# iconPath = os.path.join(imgPath, "icons")
iconCharPath = os.path.join(imgPath[0], "icons", "char_icons")
iconPath = os.path.join(imgPath[0], "icons", "other_icons")

def guiSetup():
	charGUI.CharSelect_Input( iconCharPath )
	
def basicGUI():
	win = cmds.window( title="Test Window")
	cmds.frameLayout( label="Ironman Character Selection", cll=True )
	basicSel = charGUI.CharSelect_Base( iconCharPath, win )
	cmds.showWindow()
	
def gui():
	charGUI.gui()

'''	
'''

