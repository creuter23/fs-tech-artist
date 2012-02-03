'''
Icon File Browser
'''
import glob
import maya.cmds as cmds

cmds.fileBrowserDialog( m=4, fc=iconViewer, an='View Images', om='Import' )

def iconViewer(fileName, fileType):

	# print(fileName, fileType)
	iconPath = lambda type, path="" : os.path.join( fileName, path, "*.%s" %type )

	iconType = "xpm"

	paths = glob.glob(iconPath( iconType ))

	print(iconPath(iconType), fileName, paths )

	cmds.window( title="Icon Viewer", w=300, h=300 )
	cmds.scrollLayout()
	cmds.rowColumnLayout( nc=10 )
	for path in paths:
		pathPieces = os.path.split(path)
		cmds.symbolButton( i=path, c=(lambda x: punched(path, pathPieces[1])))
	
	cmds.showWindow()

def punched(path, icon):
	print("IconName: %s\nIconPath: %s" %(icon, path))

