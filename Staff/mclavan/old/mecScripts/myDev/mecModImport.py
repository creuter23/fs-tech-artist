

# Load the information from a director into a gui as 


import glob
import os, os.path
import maya.cmds as cmds

winWidth = 300
# path, list files or directories, type
# type = 0 (tabs), 1 (frames), 2(iconTextButton)

win = "mecModIWin"

def gui():
	
	global mainCol
	if( cmds.window(win, q=True, ex=True)):
		cmds.deleteUI(win)
	
	cmds.window(win, w=winWidth, h=400, t="Model Import")
	
	mainCol = cmds.columnLayout()
	
	cmds.showWindow(win)
	
def dynFrmGUI(filePath, items, parent, dirType=0 )
	'''
	filePath(string) is the filePath that each file will be at.
	items(string list) will be files or directories
	parent(string) which gui component will the the newly created gui components will be connected to.	
	dirType(int) 0 means tabs are going to be created, where 1 will create frames
	'''
	# items will be formatted correctly so only what is needed is included.
	# keeping track of all the gui components created.
	guiCom = []
	
	# Mainlayout for the gui.
	
	cmds.setParent(parent)
	
	allPaths = os.walk(filePath)
	
	
	"""
	for item in items:
		
		
		if(dirType):
			'''
			Create frames
			'''
			layoutTemp = cmds.frameLayout(label=item)
			newPath = os.path.join( filePath,item )
			files = glob.glob( os.path.join(newPath,"*.mb") )
			
			
			guiImages = dynGUI( newPath, files, layoutTemp )	
			return [layoutTemp, guiImages]
		else:
			'''
			Create tabs.
			'''
			print("Create tabs")
			layoutTemp = cmds.tabLayout()
			
			newPath = os.path.join( filePath,item )
			# List all the files and isolate the directories.
			dynFrmGUI(newPath, items, parent, dirType=0 )
	"""	
	
def dynGUI( filePath, items, parent ):
	'''
	
	filePath(string) is the filePath that each file will be at.
	items(string list) will be files or directories
	parent(string) which gui component will the the newly created gui components will be connected to.
	'''
	
	# items will be formatted correctly so only what is needed is included.
	# keeping track of all the gui components created.
	guiCom = []
	
	# Mainlayout for the gui.
	
	cmds.setParent(parent)
	mainRow = cmds.rowColumnLayout( nc=2, cw=[[1,winWidth/2],[2, winWidth/2]] )
	
	for item in items:
	
		
		
		# Need to check to see if there is an image version like it.
		# Extra the file name
		fileParts = os.path.splitext(item)
		
		# Check to see if the image exists?
		'''
		iconBtn = cmds.button( w=winWidth/2, h=30, label=fileParts[0], parent=mainRow,
			c="print('Load file: %s')" %(item))
		'''
		iconBtn = cmds.iconTextButton( label=fileParts[0],  style="iconAndTextHorizontal",
			 marginWidth=10,   marginHeight=5, labelOffset=5,
			w=winWidth/2, h=50 , parent=mainRow,
			c="print('Load file: %s')" %(item))
	
		
		if( os.path.exists(os.path.join(filePath,fileParts[0]+".xpm")) ):
			cmds.iconTextButton(iconBtn, edit=True, image=os.path.join(filePath,fileParts[0]+".xpm") )
		elif( os.path.exists(os.path.join(filePath,fileParts[0]+".bmp")) ):
			cmds.iconTextButton(iconBtn, edit=True, image=os.path.join(filePath,fileParts[0]+".bmp") )
		else:
			print("Didn't find a match. %s  != %s" %(os.path.join(filePath,fileParts[0]+".xmp"), item))
		''''''
		print("Icon Button:%s %s" %(item, iconBtn))
		guiCom.append(iconBtn)
	
		
	return guiCom
