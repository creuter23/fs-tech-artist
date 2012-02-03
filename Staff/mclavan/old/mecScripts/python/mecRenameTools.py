
import maya.cmds as cmds
# from Callback import Callback
from mecMaya.callback import Callback

# from gui import Window()
def seqRename( objects, ori, nodeName, seq, nodeType, end=""):
	
	for i, obj in enumerate(objects):
		line = ori+ "_" + nodeName + "_"
		if(i == 0):
			line += seq[i] + "_" + nodeType
		elif(obj == objects[-1]):
			line += seq[-1] + "_"
			if(end == ""):
				line += nodeType
			else:
				line += end
		elif( i < len(seq)-1):
			line += seq[i] + "_" + nodeType
		else:			
			line += str(i) + "_" + nodeType
		print(line)	
		cmds.rename(obj, line)		

def remAllTSL(tsl):
	cmds.textScrollList(tsl, e=True, ra=True)
	
def remSelTSL(tsl):
	selectedTSL = cmds.textScrollList(tsl, q=True, si=True)
	for selTSL in selectedTSL:
		cmds.textScrollList(tsl, e=True, ri=selTSL)
	
def addTSL(tsl):
	# Get textField information
	addEle = cmds.textField( "mecRenSeqName", q=True, text=True)
	tslItems = cmds.textScrollList(tsl, q=True, ai=True)
		
	try:
		if( addEle not in tslItems ):
			cmds.textScrollList( tsl, e=True, append=addEle )
			print( "Item: %s already exists." %addEle) 
	except TypeError:
		cmds.textScrollList( tsl, e=True, append=addEle )

def prefix():
	preName = cmds.textField("mecRenPre", q=True, text=True)
	selected = cmds.ls(sl=True)

	for sel in selected:
		if(cmds.ls(sel)):
			print("Warning %s already exists in the scene." %sel)
		cmds.rename(sel, preName+sel )	
	
def suffix():
	sufName = cmds.textField("mecRenSuf", q=True, text=True)
	selected = cmds.ls(sl=True)
	
	for sel in selected:
		if(cmds.ls(sel)):
			print("Warning %s already exists in the scene." %sel)
		cmds.rename(sel, sel+sufName )	
	
	
def renameNoSeq(objs, prefix, nodeType, counter, suffix ):
	
	for obj in objs:
		newName = "_".join([prefix, nodeType, str(counter), suffix])
		if( newName in cmds.ls(obj)):
			print("Warning %s already exists in the scene." %obj)
		cmds.rename( obj, newName )
		counter += 1
		
def fullRename():
	preName = cmds.textField("mecRenPre", q=True, text=True)
	name = cmds.textField( "mecRenName", q=True, text=True)
	counter = cmds.intField( "mecRenCount", q=True, value=True)
	sufName = cmds.textField("mecRenSuf", q=True, text=True)
	selected = cmds.ls(sl=True)
	
	if( cmds.checkBox( "mecRenSeqCB", q=True, value=True )):
		# run sequence version
		selTSL = cmds.textScrollList( "mecRenSeqTSL", q=True, ai=True)
		'''	
		seqRename(cmds.ls(sl=True, dag=True), "lt", "MiddleFig", 
			["Root", "End"], "Bind")
		'''
		seqRename( selected, preName, name, selTSL, sufName)
		
	else:
		# run non sequece version
		renameNoSeq(selected, preName, name, counter, sufName )
	
def renameGui(parent):
	renCol = cmds.columnLayout()
	colWidth = winWidth/4
	cmds.rowColumnLayout(nc=4, cw=[[1,colWidth],[2,colWidth+40],[3,colWidth-40],[4,colWidth]],
		co=[[1,"both",3],[2,"both",3],[3,"both", 3],[4,"both",3]])
	cmds.text( label="Prefix", al="center" )
	cmds.text( label="Name", al="center" )
	cmds.text( label="###", al="center" )
	cmds.text( label="Suffix", al="center" )	
	
	cmds.textField( "mecRenPre" )
	cmds.textField( "mecRenName" )
	cmds.intField( "mecRenCount" )
	cmds.textField( "mecRenSuf" )
	cmds.setParent(renCol)
	
	cmds.rowColumnLayout( nc=3, cw=[[1,winWidth/3-20],[2,winWidth/3+40],[3,winWidth/3-20]],
		co=[[1,"both",3],[3,"both",3]])
	cmds.button(label="Prefix",
		c=Callback(prefix))
	cmds.button(label="Full Rename",
		c=Callback(fullRename))
	cmds.button(label="Suffix",
		c=Callback(suffix))
	cmds.setParent( parent )	
	
def enGUI(guiType, guiName, state):
	exec( "cmds.%s('%s', e=True, en=%s )" %(guiType, guiName, state))	
	
def seqGUI(parent):
	frm = cmds.frameLayout( label="Sequence", cll=True, w=winWidth-5,
		collapseCommand=Callback(winExpand, -70),
		expandCommand=Callback(winExpand, 70))
	frmCol = cmds.columnLayout(rs=3)
	cmds.checkBox( "mecRenSeqCB", label="On\Off", v=1)
	rowCol = cmds.rowColumnLayout("mecRenSeqRC", nc=2, cw=[[1,winWidth/2],[2,winWidth/2]],
		co=[[1,"right",5]])
	'''
	Older version.  Used Callback instead with a function that will enable or disable any gui component.	
	cmds.checkBox( "mecRenSeqCB", e=True, onc='%s.cmds.rowColumnLayout("mecRenSeqRC", e=True, en=True)' %scriptName)
	cmds.checkBox( "mecRenSeqCB", e=True, ofc='%s.cmds.rowColumnLayout("mecRenSeqRC", e=True, en=False)' %scriptName)
	'''
	cmds.checkBox( "mecRenSeqCB", e=True, onc=Callback(enGUI,"rowColumnLayout", "mecRenSeqRC", 1 ) )
	cmds.checkBox( "mecRenSeqCB", e=True, ofc=Callback(enGUI,"rowColumnLayout", "mecRenSeqRC", 0 ))
	
	cmds.textScrollList( "mecRenSeqTSL", h=40, ams=True )
	cmds.setParent(rowCol)
	subCol = cmds.columnLayout()
	rowWidth = winWidth/2
	cmds.rowColumnLayout(nc=2, w=rowWidth,
		cw=[[1,(rowWidth-70)], [2,60]])
	cmds.textField("mecRenSeqName", w=rowWidth-70 )
	cmds.button(label="Add",
		c=Callback(addTSL, "mecRenSeqTSL"))
	cmds.setParent(subCol)
	cmds.rowColumnLayout(nc=2, w=rowWidth,
		cw=[[1,rowWidth/2],[2,rowWidth/2-10]])
	cmds.button(label="Rem All",
		c=Callback(remAllTSL, "mecRenSeqTSL"))
	cmds.button(label="Rem Sel",
		c=Callback(remSelTSL, "mecRenSeqTSL"))
	cmds.setParent(parent)

def remElement(pos):
	selected = cmds.ls(sl=True)
	for sel in selected:
		items = sel.split("_")
		items.remove(items[pos])
		cmds.rename(sel, "_".join(items))

def remReplace():
	selected = cmds.ls(sl=True)
	oldEle = cmds.textField("mecRenRepOld" , q=True, text=True)
	newEle = cmds.textField("mecRenRepNew" , q=True, text=True)
	
	for sel in selected:
		newName = sel.replace(oldEle, newEle)
		cmds.rename(sel, newName)
		
		
def replaceGui(parent):
	cmds.frameLayout( label="Replace", cll=True,
		collapseCommand=Callback(winExpand, -70),
		expandCommand=Callback(winExpand, 70))
	replaceCol = cmds.columnLayout(rs=3)	
	cmds.rowColumnLayout(nc=2, cw=[[1,winWidth/2],[2,winWidth/2]],
		co=[[1,"both",3],[2,"both",3]])
	cmds.button(label="Prefix",	
		c=Callback(remElement, 0))
	cmds.button(label="Suffix",
		c=Callback(remElement, -1))
	cmds.setParent(replaceCol)
	
	cmds.rowColumnLayout(nc=3, cw=[[1,winWidth/2-50],[2,winWidth/2-50],[3,100]],
		co=[[1,"both",5],[2,"both",5],[3,"both",5]])
	cmds.text(label="old", al="center")
	cmds.text(label="new", al="center")
	cmds.text(label="")
	cmds.textField("mecRenRepOld")
	cmds.textField("mecRenRepNew")
	cmds.button(label="Relace",
		c=Callback(remReplace))
	cmds.setParent(parent)

def winExpand(size):
	# Current height
	curHeight = cmds.window(win, q=True, h=True)
	cmds.window(win, e=True, h=curHeight + size)
	
	
win = "mecRenWin"
winWidth=300
winHeight=300

def gui():
	
	if( cmds.window( win, q=True, ex=True)):
		cmds.deleteUI(win)
		
	cmds.window(win, title="Rename Tool", w=winWidth, h=winHeight)
	mainCol = cmds.columnLayout(rs=3)
	renameGui(mainCol)
	seqGUI(mainCol)
	replaceGui(mainCol)
	
	cmds.showWindow(win)
	
'''	
seqRename(cmds.ls(sl=True, dag=True), "lt", "MiddleFig", 
	["Root", "End"], "Bind")
'''
