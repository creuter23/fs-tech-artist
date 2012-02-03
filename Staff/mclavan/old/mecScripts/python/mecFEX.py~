'''
Face Extract Script
Michael Clavan
'''
import maya.cmds as cmds
import maya.mel as mel

win = "mecFEXWin"
mCol = "mecFEXMainC"
winWidth = 300
winHeight = 310
def gui():
	'''
	Function that generates the gui for the script.
	'''

	if( cmds.window(win, q=True, ex=True)):
		cmds.deleteUI(win)
	if( cmds.windowPref(win, q=True, ex=True)):
		cmds.windowPref(win, r=True)
		
	cmds.window(win, title="Face Extract", w=winWidth, h=winHeight)
	cmds.columnLayout(mCol)
	
	# Grab faces area
	cmds.button(label="Grab Selected Faces", w=winWidth-10,
		c="mecFEX.grabFaces()")
	
	# Selected faces area.
	cmds.frameLayout(label="Selected Faces", w=winWidth-10, cll=True, cl=True)
	cmds.columnLayout()
	cmds.textScrollList("mecFEXTSL", w=winWidth-15, h=150, ams=True,
		selectCommand="mecFEX.selectObjs()")
	cmds.rowColumnLayout( nc=2, cw=[[1,winWidth/2-7], [2,winWidth/2-7]])
	cmds.button(label="Remove All",
		c="mecFEX.removeAllTSL()")
	cmds.button(label="Remove Selected",
		c="mecFEX.removeSelTSL()")
	cmds.setParent(mCol)
	
	#Moving the extracted geometry.
	cmds.text(label="Extracted Move", width=winWidth-5)	
	cmds.rowColumnLayout( nc=6, 
		cw=[[1,winWidth/6-10],[2,winWidth/6],[3,winWidth/6-10],
		[4,winWidth/6], [5,winWidth/6-10], [6,winWidth/6]])
	cmds.text(label="X", al="center")
	cmds.floatField("mecFEXTX", v=0, pre=2 )
	cmds.text(label="Y", al="center")
	cmds.floatField("mecFEXTY", v=1.5, pre=2 )
	cmds.text(label="Z", al="center")
	cmds.floatField("mecFEXTZ", v=0, pre=2 )
	cmds.setParent(mCol)
	cmds.button(label="Apply Extract", w=winWidth-10,
		c="mecFEX.loopExtract()")
		
	cmds.frameLayout(label="Extra Tools", w=winWidth-10, cll=True, cl=True)
	cmds.columnLayout()
	cmds.rowColumnLayout(nc=2, cw=[[1,winWidth/2-7],[2,winWidth/2-7]])
	cmds.button(label="Extract Suffix", c="mecFEX.extSuffix()")
	cmds.button(label="Rename Child to Parent", c="mecFEX.renameSwap()")
	cmds.showWindow(win)

def extSuffix():
	'''
	Extract the end part the object name.
	'''
	objSelected = cmds.ls(sl=True)
	for obj in objSelected:
		temp = obj.split("_")[:-1]
		newName = ""
		for t in temp:
			newName = newName + t + "_"
		newName = newName[:-1]
		print(newName)
		cmds.rename(obj, newName)	

def renameSwap():
	'''
	------------------- Rename child parent's name ------------
	'''
	# list relative
	objSelected = cmds.ls(sl=True)
	for obj in objSelected:
		childObj = cmds.listRelatives(obj, c=True)
		cmds.parent(childObj[-1], w=True)
		cmds.delete(obj)
		cmds.rename(childObj[-1], obj)
		
def loopExtract():
	'''
	Loop through all the selected objects and runt he extractGeo function.
	'''
	curSel = cmds.ls(sl=True)
	for cur in curSel:
		cmds.select(cl=True)
		cmds.select(cur, r=True)
		extractGeo(cur)
	mel.eval('changeSelectMode -obj')
	
def extractGeo(obj):
	'''
	Extract the selected faces.
	'''
	# Grab elements from the textScrollList.
	orgSelected = cmds.textScrollList("mecFEXTSL", q=True, ai=True)
	curSel = obj
	faces = []
	for sel in orgSelected:
		temp = sel.split(".")
		#print( curSel[0] + "." + temp[-1] )
		faces.append( curSel + "." + temp[-1] )
	
	cmds.select(faces, r=True)
	mel.eval('doMenuComponentSelection("%s", "facet")' %curSel)
	
	cmds.ExtractFace()
	extSel = cmds.ls(sl=True)
	cmds.delete(extSel[0])
	cmds.delete(ch=1)
	
	# Grab transform values from the interface.
	tx = cmds.floatField("mecFEXTX", q=True, v=True)
	ty = cmds.floatField("mecFEXTY", q=True, v=True)
	tz = cmds.floatField("mecFEXTZ", q=True, v=True)
	
	# Center Pivot and move the geometry
	cmds.xform(extSel[1], cp=True)
	cmds.xform(extSel[1], t=[tx,ty,tz])
	
	# object mode
	# changeSelectMode -obj
	
def removeAllTSL():
	'''
	Remove all the elements from the textScrollList
	'''
	cmds.textScrollList("mecFEXTSL", e=True, ra=True)

def removeSelTSL():
	'''
	Remove selected objects from the textScrollList.
	'''
	# Grab TSL Selected elements.
	tslSel = cmds.textScrollList("mecFEXTSL", q=True, si=True)
	# Loop through and remove them.
	for sel in tslSel:
		cmds.textScrollList("mecFEXTSL", e=True, ri=sel)
	
def grabFaces():
	'''
	Grab faces from the scene and return it the textScrollList.
	'''	
	orgSelected = cmds.ls(sl=True)
	
	#Remove all the elements from the textScrollList
	cmds.textScrollList("mecFEXTSL", e=True, ra=True)
	#Add current selected faces to the textScrollList
	cmds.textScrollList("mecFEXTSL", e=True, append=orgSelected)
	
def selectObjs():
	'''
	Select all the object selected in the textScrollList
	'''
	tslSelected = cmds.textScrollList("mecFEXTSL", q=True, si=True)
	cmds.select(tslSelected, r=True)
