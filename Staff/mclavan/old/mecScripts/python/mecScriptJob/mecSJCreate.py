'''
Script Job Monitoring Station

Disc:
This script shows all the scriptJobs currently running in the scene.
Options for refreshing the list along will killing normal and protected 
	script jobs is offered through a menu.

How to use:
Two scripts and a xml file is required to use this script.
	mecScriptJob (This is the scriptJob monitoring script.")
	mecSJCreate (This script for creating scriptJobs.")
	scriptJob.xml (This xml has the different types of script jobs and their descriptions.)
		The scriptJob.xml file should be placed in your maya folder (The folder before your scripts folder).
		
import mecSJCreate
mecSJCreate.gui()

'''

import maya.cmds as cmds
import maya.mel as mel
import xml.etree.ElementTree as ET
import os, os.path
from callback import Callback

import mecScriptJob

winWidth = 385
winHeight = 525

winWidth2 = winWidth + 20
win = "mecSJCWin"



# Once parse global sjXML will exists

# Read xml data into script

# Practice global variables

def parseXML():
	'''
	This function will read all the xml data into a global variable.
	'''
	global sjXML
	
	mayaFolder = os.path.split(__file__)[0]
	fullPath = os.path.join( mayaFolder, "scriptJob.xml")
	
	# Need to check to see if the xml file is present.
	xmlFile = open( fullPath, "r" )
	sjXML = ET.parse(xmlFile)
	'''
	elem = tree.getroot()
	for items in elem:
		print("Event: %s" %(items.text))
		print("Desc: %s" %(items[0].text))
	'''
	xmlFile.close()		
	
def getAllEventData():
	elem = sjXML.getroot()
	for item in elem:
		print("Event: %s" %(item.text))
		print("Desc: %s" %(item[0].text))
	
def searchDisc():
	'''
	This function will return the description of the given event.
	'''	
	print("This function works.")

def loadTSL():
	'''
	Upon choosing a different radioButton the textScrollList will be updated along with the default scrollField message.
	'''
	# Get RadioButton	
	selectedRC = cmds.radioCollection(radioCol, q=True, sl=True)	
	xmlDict = { "mecSJEvent":"Events", "mecSJAttr":"attributes", "mecSJCond":"Conditions", 
		"mecSJNode":"nodeNameChanged", "mecSJConn":"connectionChange", "mecSJUI":"uiDeleted", 
		"mecSJTime":"timeChange"}	
	
	# Access proper tag from xml file
	elem = sjXML.getroot()
	sjType = xmlDict[selectedRC]
	curSel = elem.find(sjType)
	
	# Lets print out the tag and the content.
	'''
	print("TSL Enabled: %s" %(curSel.get('en')))
	print("TSL Enabled: %s" %(curSel.get('type')))	
	for items in curSel:
		print("Event: %s" %(items.text))
		print("Event: %s" %(items[0].text))	
	'''
	# Some radioButton option will clear and disable the textScrollList
	if(not int(curSel.get('en')) ):
		# print("Disable textScroll List")
		
		cmds.textScrollList(tsl, e=True, ra=True)
		cmds.textScrollList(tsl, e=True, append=curSel.get('type'))
		cmds.textScrollList(tsl, e=True, en=False)
		cmds.scrollField(sfDisc, e=True, text=curSel[0][0].text)
	else:
		# Load the textScrollList will information
		# print("Enable textScroll List")
		cmds.textScrollList(tsl, e=True, ra=True)
		cmds.textScrollList(tsl, e=True, en=True)
		cmds.scrollField(sfDisc, e=True, text='Select event for discription.')
		for item in curSel:
			cmds.textScrollList(tsl, edit=True, append=item.text)		
	sjModeSwitch()

		
def loadDisc():
	'''
	When a type of script job is selected in the textScrollList the discription of that 
		event will be posted in the adjacent scrollField.	
	'''
	# Get RadioButton	
	selectedRC = cmds.radioCollection(radioCol, q=True, sl=True)	
	xmlDict = { "mecSJEvent":"Events", "mecSJAttr":"attributes", "mecSJCond":"Conditions", 
		"mecSJNode":"nodeNameChanged", "mecSJConn":"connectionChange", "mecSJUI":"uiDeleted", 
		"mecSJTime":"timeChange"}	
	
	# get selected element from the textScrollList
	# Get which event was selected. Only the first item will be addressed.
	selectedTSL = cmds.textScrollList(tsl, q=True, si=True)[0]	
	
	# Access proper tag from xml file
	elem = sjXML.getroot()
	sjType = xmlDict[selectedRC]
	curSel = elem.find(sjType)	
	
	# find which type is selected.

	disc = ""
	for item in curSel:
		if( item.text == selectedTSL ):
			disc = item[0].text
		
	# apply disc name to the scrollField
	cmds.scrollField( sfDisc, edit=True, text=disc)
	sjModeSwitch()


def sjModeSwitch():
	'''
	Will adjust the interface for the different modes that are available.
	'''
	# Get Radio Button info
	rc = cmds.radioCollection(radioCol, q=True, sl=True)
	# Label is the same name as the scriptJob type 
	sjType = cmds.radioButton(rc, q=True, label=True)
	
	# Get selected items from the textScrollList
	try:
		selectedTSL = cmds.textScrollList(tsl, q=True, si=True)[0]
	except TypeError:
		selectedTSL = ""
	cmds.textFieldGrp("mecSJConLabel", edit=True, en=True)	
	cmds.textFieldGrp("mecSJConLabel", edit=True, text="")	
	if( sjType == "event"):
		cmds.textFieldGrp("mecSJConLabel", edit=True, text=selectedTSL)
		cmds.textFieldGrp("mecSJConLabel", edit=True, label="Event Type")
	elif( sjType == "attributes" or sjType == "connectionChange"):
		cmds.textFieldGrp("mecSJConLabel", edit=True, label="Attribute")
	elif( sjType == "condition"):
		cmds.textFieldGrp("mecSJConLabel", edit=True, text=selectedTSL)
		cmds.textFieldGrp("mecSJConLabel", edit=True, label="Condition Type")
	elif( sjType == "nodeNameChanged"):
		cmds.textFieldGrp("mecSJConLabel", edit=True, label="Node Name")
	elif( sjType == "uiDeleted"):
		cmds.textFieldGrp("mecSJConLabel", edit=True, label="uiName")
	elif(sjType == "timeChange"):
		cmds.textFieldGrp("mecSJConLabel", edit=True, label="")
		cmds.textFieldGrp("mecSJConLabel", edit=True, en=False)
	
	
def sjCreateSJ():
	'''
	Create script job from what the user chooses.
	'''

	# Grab the mode
	rc = cmds.radioCollection(radioCol, q=True, sl=True)
	# Label is the same name as the scriptJob type 
	sjType = cmds.radioButton(rc, q=True, label=True)
	
	optionLine = ""
	# Gather gui components
	proc = cmds.checkBox("mecSJPro", q=True, value=True)
	if(proc):
		optionLine += " -protected"
		
	prem = cmds.checkBox("mecSJPer", q=True, value=True)
	if( prem ):
		optionLine += " -permanent"
		
	cUndo = cmds.checkBox("mecSJCU", q=True, value=True)
	if(cUndo):
		optionLine += " -compressUndo true"
		
	# -runOnce true
	runOnce = cmds.checkBox("mecSJRo", q=True, value=True)
	if(runOnce):
		optionLine += " -runOnce true"
		
	killSc = cmds.checkBox("mecSJKws", q=True, value=True)
	if(killSc):
		optionLine += " -killWithScene"
		
	# Parent area DO LAST.
	parentCB = cmds.checkBox("mecSJParent", q=True, value=True)
	parentText = cmds.textField("mecSJParentText", q=True, text=True)
	replacePrev = cmds.checkBox("mecSJReplace", q=True, value=True)
	
	sjMode = ""
	if( sjType == "condition" ):
		if( cmds.menuItem("mecCondTrue", q=True, rb=True) ):
			sjMode = "-" + cmds.menuItem("mecCondTrue", q=True, label=True)	
		elif( cmds.menuItem("mecCondFalse", q=True, rb=True) ):
			sjMode = "-" + cmds.menuItem("mecCondFalse", q=True, label=True)	
		else:
			sjMode = "-" + cmds.menuItem("mecCondChange", q=True, label=True)
	elif( sjType == "attributes" ):
		if( cmds.menuItem("mecAttrCh", q=True, rb=True) ):
			sjMode = "-" + cmds.menuItem("mecAttrCh", q=True, label=True)	
		elif( cmds.menuItem("mecAttrDel", q=True, rb=True) ):
			sjMode = "-" + cmds.menuItem("mecAttrDel", q=True, label=True)	
		else:
			sjMode = "-" + cmds.menuItem("mecAttrAdd", q=True, label=True)
	else:
		sjMode = "-" + sjType
	"""
	elif( sjType == "event" ):
		sjMode = "-" + sjType
	elif( sjType == "timeChange"):
		sjMode = "-" + sjType
	elif( sjType == "uiDeleted"):
		sjMode = "-" + sjType
	elif( sjType == "connectionChange"):
		sjMode = "-" + sjType
	elif( sjType == 
	"""
	arg1 = cmds.textFieldGrp("mecSJConLabel", q=True, text=True)
	arg2 = cmds.textFieldGrp("mecSJProcLabel", q=True, text=True)
		
	parentFlag = cmds.checkBox("mecSJParent",  q=True, value=True )
	uiName = cmds.textField("mecSJParentText", q=True, text=True)
	replaceChk = cmds.checkBox("mecSJReplace", q=1, v=1)		
	
	sjParent = ""
	if( parentFlag ):
		sjParent += ' -p "%s"' %uiName
		if( replaceChk ):
			sjParent += " -rp" 	
	
	sjModeArgs = ""
	if( sjType != "timeChange" ):
		sjModeArgs = '"%s" "%s"' %(arg1, arg2)
	else:
		sjModeArgs = '"%s"' %arg2
	
	fullLine = "scriptJob %s %s%s%s;" %(sjMode, sjModeArgs, optionLine, sjParent)
	print(fullLine)
	cmds.textField("mecSJPreview", edit=True, text=fullLine)


def exeScriptJ():
	'''
	Execute Script Job (MEL Side)
	'''
	sjLine = cmds.textField("mecSJPreview", q=True, text=True)
	mel.eval(sjLine)
	
def gui():
	'''
	GUI for creating scriptJobs
	'''
	# Get XML Data
	parseXML()
	global mainCol, tsl, sfDisc, tslText, radioCol

	if( cmds.window(win, q=True, ex=True ) ):
		cmds.deleteUI(win)
	if( cmds.windowPref( win, ex=True)):
		cmds.windowPref(win, r=True)
		
	cmds.window(win, title="Script Job Creator", mb=True, w=winWidth2, h=winHeight )
	cmds.menu(label="System")
	cmds.menuItem(label="Script Job Monitor",
		c=Callback(mecScriptJob.gui))
	mainCol = cmds.columnLayout(rs=4, co=["both", 5])
	cmds.rowColumnLayout( nc=2, cw=[[1,winWidth*.4],[2,winWidth*.6]])
	tslText = cmds.text(label="Event Types", w=200, al="center")
	cmds.text(label="Type Desciption", w=300, al="center")
	tsl = cmds.textScrollList( w=200, h=150, append="Select Mode",  en=False,
		sc=Callback(loadDisc))
	sfDisc = cmds.scrollField( w=300, h=150,
		editable=False, wordWrap=True, text='Select event for discription.' )
	cmds.setParent( mainCol )
	
	# Create a radioButton collection
	cmds.frameLayout(label="Script Job Type", labelAlign="center", w=winWidth,
		labelIndent=winWidth/2-50)
	frmType = cmds.formLayout(w=winWidth, h=25)
	
	# cmds.text( l="Choose Script Job Type", w=winWidth, al="center")
	rlType = cmds.rowColumnLayout(nc=4, w=500, cw=[[1,winWidth*.25-15],[2,winWidth*.25],[3,winWidth*.25-10],[4,winWidth*.25]],
								  co=[1,"left", 5])
	radioCol = cmds.radioCollection()
	cmds.radioButton("mecSJEvent", label='event', cl=radioCol, sl=True,
		onCommand=Callback(loadTSL))
	cmds.radioButton("mecSJAttr", label='attributes', cl=radioCol,
		onCommand=Callback(loadTSL) )
	cmds.radioMenuItemCollection("mecSJAttrCol")
	cmds.popupMenu()
	cmds.menuItem("mecAttrCh", label="attributeChange", cl="mecSJAttrCol", rb=True)
	cmds.menuItem("mecAttrDel", label="attributeDeleted", rb=False, cl="mecSJAttrCol")
	cmds.menuItem("mecAttrAdd", label="attributeAdded", rb=False, cl="mecSJAttrCol")
	cmds.setParent("..", m=True)
	
	cmds.radioButton("mecSJCond", label='condition', cl=radioCol,
		onCommand=Callback(loadTSL) )
	cmds.radioMenuItemCollection("mecSJConCol")
	cmds.popupMenu()
	cmds.menuItem("mecCondTrue", label="conditionTrue", rb=True, cl="mecSJConCol")
	cmds.menuItem("mecCondFalse", label="conditionFalse", rb=False, cl="mecSJConCol")
	cmds.menuItem("mecCondChange", label="conditionChange", rb=False, cl="mecSJConCol")
	cmds.setParent("..", m=True)
	
	cmds.radioButton("mecSJNode", label='nodeNameChanged', cl=radioCol,
		onCommand=Callback(loadTSL) )
	
	cmds.setParent(frmType)
	rlType2 = cmds.rowColumnLayout(nc=3, w=500, cw=[[1,winWidth/3],[2,winWidth/3-20],[3,winWidth/3]],
									  co=[1,"right", 10])

	cmds.radioButton("mecSJConn", label='connectionChange', cl=radioCol,
		onCommand=Callback(loadTSL) )
	cmds.radioButton("mecSJUI", label='uiDeleted', cl=radioCol,
		onCommand=Callback(loadTSL) )
	cmds.radioButton("mecSJTime", label='timeChange', cl=radioCol,
		onCommand=Callback(loadTSL) )	
		
	cmds.setParent(frmType)
	
	
	row1 = cmds.rowColumnLayout(nc=2, cw=[[1,winWidth/2+10],[2,winWidth/2-20]])
	# This text and ann will change depending when type of script job is chosen.
	# In the case time this text and field will not be used.
	# Certain scriptJob types will automaticly change the content of this field
	cmds.textFieldGrp("mecSJConLabel", label='Attribute', text='', w=winWidth/2,
		cw=[[1,90], [2,200]],
		ann="")

		
	# This field will recieve which procedure will be exectued when the scriptJob is triggered.
	cmds.textFieldGrp("mecSJProcLabel", label='Procedure: ', text='', w=winWidth/2,
		cw=[1,75],
		ann="What function will the scriptJob call?")
	cmds.formLayout(frmType, edit=True, attachForm=[[rlType, "left", 0], 
		[rlType2, "left", 40], [row1, "left", 0], [rlType, "top", 5]], 
		attachControl=[[rlType2,"top",5,rlType], [row1,"top",5,rlType2]])  
	cmds.formLayout( frmType, e=1, af=[row1, "bottom", 5])
	cmds.setParent(mainCol)
	
	
	frmMid = cmds.formLayout()
	jsLayout = jobSecurity( frmMid )
	jLayout = jobLifeSpan( frmMid )
	
	cmds.formLayout(frmMid, e=1, af=[[jsLayout, "top", 5],[jLayout, "top", 5]],
				    ac=[jLayout, "left", 10, jsLayout])
	
	cmds.setParent( mainCol )


	
	# Script Job UI Connection
	cmds.frameLayout(label="Script Job UI Connection", labelAlign="center", w=winWidth,
		labelIndent=winWidth/2-60)
	frm3 = cmds.formLayout(w=winWidth, h=25)
	row3 = cmds.rowColumnLayout(nc=3, cw=[[1,60], [2,150],[3,100]])
	cmds.checkBox("mecSJParent", label="parent", w=100, v=0,
		ann="Attaches this job to a piece of maya UI. When the UI is destroyed, the job will be killed along with it.")
	cmds.textField("mecSJParentText", text="UINameHere", w=100)
	cmds.checkBox("mecSJReplace", label="replacePrevious", v=0,
		ann="This flag can only be used with the -parent flag. Before the new scriptJob is created, any existing scriptJobs that have the same parent are first deleted.")
	cmds.setParent("..")
	cmds.formLayout(frm3, edit=True, attachForm=[[row3, "left", winWidth/2-140],
		[row3, "top", 5]])  
	cmds.setParent(mainCol)		
	
	# Create the Script Job
	cmds.button(label="Generate Script Job", w=winWidth,
		c=Callback(sjCreateSJ))
	cmds.textField("mecSJPreview", w=winWidth, text="Preview Area",  editable=False)
	cmds.button(label="Execute Script Job! Warning this will activate the scriptJob!", w=winWidth,
		c=Callback(exeScriptJ))
	# Preview Area (Extra)
	# This area will show what the script job is looking like.
	
	# Get radioButton event setup first
	# Attr
	# Condition
	
	# Add elements into textScrollList
	#appendElements( tsl )
	loadTSL()
	cmds.showWindow(win)
	
def jobSecurity(curParent):
	# Script Job Security	
	frameWidth = 195
	frame = cmds.frameLayout(label="Script Job Security", labelAlign="center", w=frameWidth, parent=curParent, 
		labelIndent=frameWidth/2-50)
	frm2 = cmds.formLayout(w=winWidth, h=25)
	cb3 = cmds.checkBox("mecSJPro", label="Protect", w=100, v=0,
		ann="Makes the job harder to kill. Protected jobs must be killed or replaced intentionally by using the -force flag. The -killWithScene flag does apply to protected jobs")
	cb4 = cmds.checkBox("mecSJPer", label="Permanent", w=100, v=0,
		ann="Makes the job un-killable. Permanent jobs exist for the life of the application, or for the life of their parent object. The -killWithScene flag does apply to permanent jobs. ")
	cb5 = cmds.checkBox("mecSJCU", label="compressUndo", w=100, v=0,
		ann="If this is set to true, and the scriptJob is undoable, then its action will be bundled with the last user action for undo purposes. For example; if the scriptJob was triggered by a selection change, then pressing undo will undo both the scriptJob and the selection change at the same time.")
	'''
	cmds.formLayout(frm2, edit=True, attachForm=[[cb3, "left", winWidth/4], 
		[cb3, "top", 5],[cb4, "top", 5],[cb5, "top", 5]], 
		attachControl=[[cb4,"left",0,cb3], [cb5,"left",0,cb4]])  
	'''
	cmds.formLayout( frm2, e=1, af=[[cb3, "left", 5], [cb3, "top", 5], [cb4, "left", 5],[cb5, "left", 5]],
					  ac=[[cb4, "top", 0, cb3],[cb5, "top", 0, cb4]])
	cmds.formLayout( frm2, e=1, af=[cb5, "bottom", 5])	 

	cmds.setParent(curParent)
	
	return frame
			 
def jobLifeSpan( curParent ):

	# Script Job Lifespan
	frameWidth = 180
	frame = cmds.frameLayout(label="Script Job Life Span", labelAlign="center", w=frameWidth, parent=curParent,
		labelIndent=(frameWidth/2 - 60))

	frm1 = cmds.formLayout(w=winWidth, h=25)	
	cb1 = cmds.checkBox("mecSJRo", label="runOnce", w=100, v=0, parent=frm1,
		ann="If this is set to true, the script will only be run a single time. If false (the default) the script will run every time the triggering condition/event occurs. If the -uid flag is used, runOnce is turned on automatically.")
	cb2 = cmds.checkBox("mecSJKws", label="killWithScene", w=100, v=0, parent=frm1,
		ann="Attaches the job to the current scene, and when the scene is emptied. The current scene is emptied by opening a new or existing scene.")
	'''
	cmds.formLayout(frm1, edit=True, attachForm=[[cb1, "left", winWidth/3],
		[cb1, "top", 5],[cb2, "top", 5]], 
		attachControl=[[cb2,"left",0,cb1]]) 
	'''
	cmds.formLayout( frm1, e=1, af=[[cb1, "top", 5],[cb1, "left", 5],[cb2, "left", 5]],
					 ac=[cb2, "top", 0, cb1])
	cmds.formLayout( frm1, e=1, af=[cb2, "bottom", 20])	 
	cmds.setParent(curParent)
	return frame


def appendElements( tsl ):
	'''
	Add event names to the textScrollList provided.
	'''	
	# Get event names from the xml file.
	# Get the root
	elem = sjXML.getroot()
	for item in elem:
		cmds.textScrollList(tsl, edit=True, append=item.text)

#parseXML()
