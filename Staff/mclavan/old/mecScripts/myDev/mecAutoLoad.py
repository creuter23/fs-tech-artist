'''
Michael Clavan
mecAutoLoad.py

Description:

How to Run:

import mecAutoLoad
reload( mecAutoLoad )
mecAutoLoad.gui()

'''
import maya.cmds as cmds

win = "mecMenuWin"
width = 300
height = 300

def gui():


	
	if( cmds.window( win, q=True, ex=True )):
		cmds.deleteUI(win)
	
	cmds.window(win, title="Menu Layout", w=width, h=height )
	frm = cmds.formLayout( )
	gui1 = menuOutlineGUI( frm )
	# gui1 = cmds.psdChannelOutliner(h=175, w=150, psdParent="mecMenu")

	# gui1 = cmds.button( label="psdChannelBox", h=175, w=150 )
	# gui2 = cmds.button( label="Setting info" , h=250, w=250 )
	
	gui2 = settingsGUI(frm)
	
	cmds.formLayout( frm, e=1, af=[[gui1, "top", 5],[gui1, "left", 5]])
	cmds.formLayout( frm, e=1, af=[gui2, "top", 5],
		ac=[gui2, "left", 5, gui1])
	
	
	cmds.showWindow()

# def psdButtonsGUI(curParent):
	
def settingsGUI2(curParent):
	
	frm = cmds.formLayout( parent=curParent )
	txtGUI = cmds.text( label="----Settings----", w=400 )
	global rbSettings
	rbSettings = cmds.radioButtonGrp( nrb=2, labelArray2=["Python", "MEL"], sl=1,
		label="Language Type:", cw=[[1,100],[2,75],[3,50]], w=250)
	
	global scrollGui
	scrollGui = cmds.cmdScrollFieldExecuter(width=450, height=200, sourceType="python")
		
	cmds.formLayout( frm, e=1, af=[[txtGUI, "top", 5],[txtGUI, "left", 50]] )	
	cmds.formLayout( frm, e=1, af=[rbSettings, "left", 50], ac=[rbSettings, "top", 5, txtGUI] )	
	cmds.formLayout( frm, e=1, af=[scrollGui, "left", 0], ac=[scrollGui, "top", 0, rbSettings])	

	cmds.setParent(curParent)
	return frm
	
def settingsGUI(curParent):
	frame = cmds.frameLayout( label="Menu Settings", w=450, la="center", parent=curParent )	
	frm = cmds.formLayout( )

	global rbSettings
	rbSettings = cmds.radioButtonGrp( nrb=2, labelArray2=["Python", "MEL"], sl=1,
		label="Language Type:", cw=[[1,100],[2,75],[3,50]], w=250)
	
	global scrollGui
	scrollGui = cmds.cmdScrollFieldExecuter(width=450, height=200, sourceType="python")
	
	btnExeAll = cmds.button(label="Execute All", w=190,
		command=(lambda x: cmds.cmdScrollFieldExecuter( scrollGui, e=1, executeAll=1)))
	btnExeSel = cmds.button(label="Execute Selected", w=190,
		command=(lambda x: cmds.cmdScrollFieldExecuter( scrollGui, e=1, execute=1)))
	
	cmds.formLayout( frm, e=1, af=[[rbSettings, "left", 50],[rbSettings, "top", 0]] )	
	cmds.formLayout( frm, e=1, af=[[scrollGui, "left", 3],[scrollGui, "right", 3]], ac=[scrollGui, "top", 0, rbSettings])	
	cmds.formLayout( frm, e=1, af=[btnExeAll, "left", 50], ac=[btnExeAll, "top", 5,scrollGui])
	cmds.formLayout( frm, e=1, ac=[[btnExeSel, "top", 5,scrollGui], [btnExeSel, "left", 10,btnExeAll]])

	
	cmds.setParent(curParent)
	return frame


	
	
def settingsGUI3(curParent):
	frame = cmds.frameLayout( label="Settings", w=450, la="center", parent=curParent )
	frm = cmds.formLayout( )
	btn = cmds.button(label="Code", w=450, h=200)
	
	cmds.formLayout( frm, e=1, af=[[btn, "top", 3],[btn, "left", 3], [btn,"right", 3]])
	cmds.setParent(curParent)
	return frame

	
def menuOutlineGUI(curParent):
	frame = cmds.frameLayout( parent=curParent, w=180, la="center", label="Menu Outline")
	frm = cmds.formLayout()
	global chanOutline
	chanOutline = cmds.psdChannelOutliner(h=175, w=180, psdParent="mecMenu")
	
	btns = menuOutBtns(frm)
	
	cmds.formLayout( frm, e=1, af=[[chanOutline, "top", 0],[chanOutline, "left", 0]])
	cmds.formLayout( frm, e=1, af=[btns, "left", 3], ac=[btns, "top", 0, chanOutline]) 
	cmds.psdChannelOutliner( chanOutline, e=True, psdParent="mecMenu", addChild=["MyScripts",""] )
	cmds.psdChannelOutliner( chanOutline, e=True, psdParent="mecMenu", addChild=["Rigging",""] )
	cmds.psdChannelOutliner( chanOutline, e=True, psdParent="mecMenu", addChild=["Modeling",""] )
	
	cmds.psdChannelOutliner( chanOutline, e=True, psdParent="Rigging", addChild=["Script1",""] )
	cmds.psdChannelOutliner( chanOutline, e=True, psdParent="Rigging", addChild=["Script2",""] )
	cmds.psdChannelOutliner( chanOutline, e=True, psdParent="Rigging", addChild=["Script3",""] )
	
	cmds.psdChannelOutliner( chanOutline, e=True, psdParent="MyScripts", addChild=["Script1",""] )
	cmds.psdChannelOutliner( chanOutline, e=True, psdParent="MyScripts", addChild=["Script2",""] )
	cmds.psdChannelOutliner( chanOutline, e=True, psdParent="MyScripts", addChild=["Script3",""] )	
	cmds.setParent( curParent )
	
	
	return frame
	
def menuOutBtns(curParent):
	frm = cmds.formLayout( parent=curParent)
	global opMenu
	opMenu = cmds.optionMenu( w=135 )
	cmds.menuItem( label='mecMenu' )
	cmds.menuItem( label='mecMenu.Modeling' )
	cmds.menuItem( label='mecMenu.Rigging' )
		
	xBtn = cmds.button( label="-", w=25, h=20)
	addBtn = cmds.button( label="+", w=25, h=20 )
	global addField
	addField = cmds.textField( w=135 )
	
	# Positioning Elements
	cmds.formLayout( frm, e=1, af=[[opMenu, "top", 3],[opMenu, "left", 3]])
	cmds.formLayout( frm, e=1, ac=[xBtn, "left", 5, opMenu],af=[xBtn, "top", 3] )
	cmds.formLayout( frm, e=1, af=[addBtn, "left", 5], ac=[addBtn, "top", 3, opMenu])
	cmds.formLayout( frm, e=1, ac=[[addField, "left", 5, addBtn],[addField, "top", 3, opMenu]])
	
	cmds.setParent(curParent)
	return frm
"""
# Create an xml here for the tree structure
import xml.etree.ElementTree as ET

# One of these will have to read in from xml
class ChannelOutliner(object):
	'''
	Controls entries into the psdChannelOutliner.
	'''
	def __init__(self, rootName, width, height):
		self.gui = cmds.psdChannelOutliner( w=width, h=height, parent=rootName )
		self.root = ET.Eleement( rootName )
		
		self.tree = {rootName:self.root}
		
		# self.items = {self.root:[None]}

	def addChild(self, posName, name):
		if( not self.tree.hasKey( name ) ):
			if( self.tree.hasKey(posName):
				pos = self.tree(posName)
				self.tree[name] = ET.Element(pos, name)
			else:
				print("Parent element %s doesn't exists" %posName)
		else:
			print( "%s : Currently exists: Choose a different menuName" %name )
		
	def subElement(self, posName, name):
		if( not self.tree.hasKey( name ) ):
			if( self.tree.hasKey( posName ) ):
				pos = self.tree(posName)
				self.tree[name] = Et.SubElement(pos, name)
			else:
				print("Parent element %s doesn't exists" %posName)
		else:
			print( "%s : Currently exists: Choose a different menuName" %name )
			
	def loadXML(self):
		mayaFolder = cmds.internalVar( uad=True )
		path = cmds.fileDialog( m=0, directoryMask=mayaFolder )
		
		if( path ):
			
			tree = ET.parse( path )
			elem = tree.getroot()

			
		
	def writeXML(self):
		mayaFolder = cmds.internalVar( uad=True )
		cmds.fileDialog( m=1, directoryMask=mayaFolder )
		'''
		if( path ):
			myFile = open( path, 'w' )
			
			myFile.close()
		'''	
"""		
"""
import xml.etree.ElementTree as ET

root = ET.Element("html")
head = ET.SubElement(root, "head")
head.text = "Header Info"
help(root)
root.tag

title = ET.SubElement(head, "title")
title.text = "Page Title"
tree = ET.ElementTree(root)



root = ET.Element("mecMenu")
sub1 = ET.SubElement( root, "myScripts" )
sub2 = ET.SubElement( root, "Rigging" )
sub3 = ET.SubElement( root, "Modeling" )
ET.SubElement( sub1, "Script1")
ET.SubElement( sub1, "Script2")
ET.SubElement( sub1, "Script3")



root = ET.Element("mainMenu")
root.text = "mecMenu"
sub1 = ET.SubElement( root, "subMenu")
sub1.text = "myScripts"
sub2 = ET.SubElement( root, "subMenu")
sub2.text = "Rigging"
sub3 = ET.SubElement( root, "subMenu")
sub3.text = "Modeling"

menu1 = ET.SubElement( sub1, "menuItem")
menu1.text = "Script1"
menu1 = ET.SubElement( sub2, "subMenu")
menu1.text = "MyRiggingScripts"
leaf1 = ET.SubElement( menu1, "menuItem")
leaf1.text = "mecConvert"
leaf1 = ET.SubElement( menu1, "menuItem")
leaf1.text = "mecImport"
menu1 = ET.SubElement( sub1, "menuItem")
menu1.text = "Script3"


# Searching for an element
grabItem = "Script1"

root.findtext( "Script1" )
root.findall( "Script1" )
root.findtext( "Script1" )
root.getiterator("menuItem")[0].text

checkItem = "Script3"
for item in root.getiterator("menuItem"):
	print("<%s> %s </%s>" %(item.tag, item.text, item.tag) )
	if( item.text == "Script1"):
		print(item.text)
		print("import maya.cmds as cmds")
	elif( item.text == "Script3" ):
		print("cmds.sphere()")
		global tempItem
		tempItem = ET.SubElement( item, "python" )
		tempItem.text = "import maya.cmds as cmds\ncmds.sphere()"

parent = [root]  # Option menu can get this list
# The first Item 
cmds.psdChannelOutliner( psdName, e=True, parent=parent[-1].text )
for item in root.getiterator():
	if( item.tag == "subMenu" ):
		print("I'm a sub menu: Setting as parent: %s" %item.text)
		cmds.psdChannelOutliner( psdName, e=True, parent=parent[-1].text )
		parent.append(item)

	elif( item.tag == "menuItem" ):
		print("I'm a leaf, my parent is %s" %parent[-1].text )
	print( "<%s> %s " %( item.tag, item.text) )

# Option menu can get this list
for curParent in parent:
	print(curParent.text)


ET.tostring(root)
"""
"""
# Its close to working, the parent isn't working.
# Everything else, even down to the ordering is working great

class MenuNode(object):
	def __init__(self, xmlTag ):
		self.parent = None
		self.name = xmlTag.text
		self.type = xmlTag.tag
		self.xmlNode = xmlTag
		if( self.type == "menuItem" ):
			self.lang = self.xmlNode[0].tag
			self.code = self.xmlNode[0].text

orderList = []
def recusion( xmlTag ):
	if( xmlTag.tag == "menuItem" ):
		nodeItem = MenuNode(xmlTag)
		orderList.append( nodeItem  )
		return  nodeItem
	# add element
	# subItem = MenuNode( xmlTag )
	# What is its current parent?

	orderList.append( newMenu )
	
	for curItem in xmlTag.getchildren():
		recTag = recusion( curItem )

		# Setting parent variable
		# 
		
		
		if(recTag):
			print("Tag: %s Name: %s" %(recTag.type, recTag.name))
			recTag.parent = xmlTag.text
		'''
		else:
			orderedList[-1].parent = xmlTag.text
			print("No Parent: Tag: %s Name: %s" %(curItem.tag, curItem.text))
		'''

'''
	parent = None
	if( orderList ):
		# newMenu.parent = orderList[-2].name
		parent = orderList[-1].name

	newMenu = MenuNode(xmlTag)
	newMenu.parent = parent
	# orderList[-1].name = xmlTag.text
'''
recusion(root)
for item in orderList:
	print(item.name, item.__dict__)
len(orderList)
import xml.etree.ElementTree as ET

root = ET.Element("mainMenu")
root.text = "mecMenu"
sub1 = ET.SubElement( root, "subMenu")
sub1.text = "myScripts"
sub2 = ET.SubElement( root, "subMenu")
sub2.text = "Rigging"
sub3 = ET.SubElement( root, "subMenu")
sub3.text = "Modeling"

menu1 = ET.SubElement( sub1, "menuItem")
menu1.text = "Script1"
menu1 = ET.SubElement( sub2, "subMenu")
menu1.text = "MyRiggingScripts"
leaf1 = ET.SubElement( menu1, "menuItem")
leaf1.text = "mecConvert"
leaf1 = ET.SubElement( menu1, "menuItem")
leaf1.text = "mecImport"
menu1 = ET.SubElement( sub1, "menuItem")
menu1.text = "Script3"
"""

"""
# This one works

class MenuNode(object):
	def __init__(self, xmlTag ):
		self.parent = None
		self.name = xmlTag.text
		self.type = xmlTag.tag
		self.xmlNode = xmlTag
		self.children = None
		'''
		if( self.type == "menuItem" ):
			self.lang = self.xmlNode[0].tag
			self.code = self.xmlNode[0].text
		'''

orderKey = []
def menuBuild( xmlTag ):
	if( xmlTag.tag == "menuItem" ):
		print("menuItem reached: ", xmlTag.tag, xmlTag.text)
		nodeItem = MenuNode(xmlTag)
		orderKey.append( nodeItem )
		return  nodeItem		
	elif( xmlTag.tag == "subMenu" ):
		print("subMenu reached: ", xmlTag.tag, xmlTag.text)
		nodeItem = MenuNode(xmlTag)
		orderKey.append(nodeItem)
		for child in xmlTag.getchildren():
			recTag = menuBuild( child )
			recTag.parent = xmlTag.text
		return nodeItem

	root = MenuNode(xmlTag)
	orderKey.append( root )
	for curItem in xmlTag.getchildren():
		recTag = menuBuild( curItem )
		recTag.parent = xmlTag.text

	
	

menuBuild(root)
# order key is above
len(orderKey )
for item in orderKey:
	print(item.name, item.parent)
	item.__dict__


# print out results
# for item in orderKey:
	# print(item.name, item.parent)
#   current   parent
# ('mecMenu', None)
# ('myScripts', 'mecMenu')
# ('Script1', 'myScripts')
# ('Script3', 'myScripts')
# ('Rigging', 'mecMenu')
# ('MyRiggingScripts', 'Rigging')
# ('mecConvert', 'MyRiggingScripts')
# ('mecImport', 'MyRiggingScripts')
# ('Modeling', 'mecMenu')

import xml.etree.ElementTree as ET

root = ET.Element("mainMenu")
root.text = "mecMenu"
sub1 = ET.SubElement( root, "subMenu")
sub1.text = "myScripts"
sub2 = ET.SubElement( root, "subMenu")
sub2.text = "Rigging"
sub3 = ET.SubElement( root, "subMenu")
sub3.text = "Modeling"

menu1 = ET.SubElement( sub1, "menuItem")
menu1.text = "Script1"
menu1 = ET.SubElement( sub2, "subMenu")
menu1.text = "MyRiggingScripts"
leaf1 = ET.SubElement( menu1, "menuItem")
leaf1.text = "mecConvert"
leaf1 = ET.SubElement( menu1, "menuItem")
leaf1.text = "mecImport"
menu1 = ET.SubElement( sub1, "menuItem")
menu1.text = "Script3"
"""

