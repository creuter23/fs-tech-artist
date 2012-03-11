'''
Panel Creation
mecModelEditor_test.py

import mecModelEditor_test
reload(mecModelEditor_test)
'''
# panel
# paneLayout
# modelPanel
# modelEditor
# Checking for scripted panel.

# modelPanelBarShadingCallback("LightBtn", "modelPanel4", "MayaWindow|mayaMainWindowForm|formLayout3|viewPanes|modelPanel4|modelPanel4|modelEditorIconBar"); restoreLastPanelWithFocus();

import maya.cmds as cmds

class BuddyWindow(object):
	def __init__(self, camera, setting=1, width=0, height=0):
		self.editor = cmds.modelEditor()
		self.camera = camera
		self.width = width
		self.heigth = height
		self.setting = { 1: "silMode()" }
		
		if( width and height ):	
			cmds.modelEditor( self.editor, edit=True, w=width )
			cmds.modelEditor( self.editor, edit=True, h=height )
		
		cmds.modelEditor( self.editor, edit=True, camera=self.camera )
		
		# eval( self.setting[setting] )
		
	def silMode(self):
		'''
		Turns silhouette mode on
		'''
		cmds.modelEditor( self.editor, edit=True, displayLights="selected" )
		cmds.modelEditor( self.editor, edit=True,grid=False )
		cmds.modelEditor( self.editor, edit=True,selectionHiliteDisplay=False )
		cmds.modelEditor( self.editor, edit=True, displayAppearance='smoothShaded')
		cmds.modelEditor( self.editor, edit=True, manipulators=False)
		cmds.modelEditor( self.editor, edit=True, headsUpDisplay=False)
		self.hideAll()
		cmds.camera(self.camera, e=True, displayResolution=True  )
		
	def hideAll(self, nurbsCrv=0):
		cmds.modelEditor( self.editor, edit=True,allObjects=False )	
		cmds.modelEditor( self.editor, edit=True,polymeshes=True )
		cmds.modelEditor( self.editor, edit=True,nurbsSurfaces=True )
		cmds.modelEditor( self.editor, edit=True,nurbsCurves=nurbsCrv ) 		
		
	def normal(self):
		cmds.modelEditor( self.editor, edit=True, displayLights="default" )
		cmds.modelEditor( self.editor, edit=True,allObjects=True )
		cmds.modelEditor( self.editor, edit=True, manipulators=False)
		cmds.modelEditor( self.editor, edit=True, headsUpDisplay=False)
		cmds.modelEditor( self.editor, edit=True,selectionHiliteDisplay=False )
		cmds.modelEditor( self.editor, edit=True, displayAppearance='smoothShaded')

		
def gui():
	window = cmds.window()
	tabsGUI()
	'''
	cmds.paneLayout( configuration='single' )
	global bw
	bw = BuddyWindow('camera1')
	bw.silMode()
	'''
	cmds.showWindow( window )

def tabsGUI():
	# global tabs
	tabs = cmds.tabLayout(w=500, h=500)
	
	siloLayout = cmds.paneLayout(w=500, h=500, configuration='single' )
	global bw
	bw = BuddyWindow('camera1')
	bw.silMode()
	cmds.setParent(tabs)
	
	cmds.columnLayout(w=500, h=500)
	cmds.text("Another Layout")
	cmds.button(label="Test")
	cmds.button(label="Test2")
	cmds.button(label="Test3")
	cmds.setParent(tabs)
	
	# cmds.tabLayout( tabs, tl=[[siloLayout,"Silh Cam"]] )
	

"""	
Test Code
import mecModelEditor_test as mod
reload(mod)
mod.gui()

mod.bw.silMode()
mod.bw.normal()
mod.bw.hideAll(1)



window = cmds.window()
# form = cmds.formLayout()
cmds.paneLayout( configuration='single' )
editor = cmds.modelEditor()
# column = cmds.columnLayout('true')


cmds.modelEditor( editor, edit=True, camera="camera1" )
cmds.modelEditor( editor, edit=True, displayLights="selected" )
cmds.modelEditor( editor, edit=True,allObjects=False )
cmds.modelEditor( editor, edit=True,polymeshes=True )
cmds.modelEditor( editor, edit=True,nurbsSurfaces=True )
# cmds.modelEditor( editor, edit=True,nurbsCurves=True ) 
cmds.modelEditor( editor, edit=True,grid=False )
cmds.modelEditor( editor, edit=True,selectionHiliteDisplay=False )

'''
selected = cmds.ls(sl=True)
cmds.select( "group1", r=True )
cmds.modelEditor( editor, edit=True,addObjects="group1" )
cmds.modelEditor( editor, edit=True,viewSelected =True )
'''

cmds.modelEditor(editor, edit=True, displayAppearance='smoothShaded')
cmds.modelEditor(editor, edit=True, manipulators=False)
cmds.modelEditor(editor, edit=True, headsUpDisplay=False)


cmds.camera("camera1", e=True, displayResolution=True  )

if( selected):
	cmds.select( selected, r=True)
else:
	cmds.select( cl=True )
# cmds.formLayout( form, edit=True, attachForm=[(column, 'top', 0), (column, 'left', 0), (editor, 'top', 0), (editor, 'bottom', 0), (editor, 'right', 0)], attachNone=[(column, 'bottom'), (column, 'right')], attachControl=(editor, 'left', 0, column))
cmds.showWindow( window )
"""


