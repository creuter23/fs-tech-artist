'''
textScrollList.py

'''

# from mecMaya.gui import Window
import maya.cmds as cmds

class TextScrollList(object):
	def __init__(self, tslWidth=100, tslHeight=100, items=[], multSel=1):
		'''
		Creates a textScrollList.
		'''
		self.tsl = cmds.textScrollList( w=tslWidth, h=tslHeight, ams=multSel,
			append=items)
	'''
	def __str__(self):
		# print the name of the textScrollList and all of its content.
		line = "-"*15 + " textScrollList " + "-"*15 +'\n'
		line += "tslName: %s\n" %self.tsl 
		line += "tslContents:\n"
		try:
			line += "\n".join(self.tsl.getAllItems()) 
		except AttributeError:
			line += "Nothing in the textScrollList\n"
		line += "-"*48 + '\n'
		
		return line
	'''
	def getWidth(self):
		return cmds.textScrollList( self.tsl, q=True, w=True )
		
	def setWidth(self, value):
		cmds.textScrollList( self.tsl, e=True, w=value )
		print( "%s width changed to %s." %(self.tsl, value) )
	def getHeight(self):
		return cmds.textScrollList( self.tsl, q=True, h=True )
	def setHeight(self, value):
		cmds.textScrollList( self.tsl, e=True, h=value )
		print( "%s height changed to %s." %(self.tsl, value) )
		
	width = property(getWidth,setWidth)
	w = property(getWidth,setWidth)
	height = property(getHeight, setHeight)	
	h = property(getHeight,setHeight)

	
	'''
	def __setAttr__( self, attr, value ):
		if( attr == "width" ):
			self.tsl.setWidth(value)
			print("hello")
			
	def __getAttr__(self, attr ):
		if(attr == "width"):
			return self.tsl.getWidth()
	'''		
	def getAllItems(self):
		'''
		Returns all the items in the textScrollList
		'''
		allItems = cmds.textScrollList( self.tsl, q=True, ai=True)
		if(allItems):
			return allItems
		else:
			return []
		
	def getSelItems(self):
		'''
		Returns the selected items from the textScrollList
		'''
		selItem = cmds.textScrollList( self.tsl, q=True, si=True)
		if( selItem ):
			return selItem
		else:
			return []
		
	def remSelItems(self):
		'''
		Remove selected Items from the textScrollList
		'''
		selItems = self.getSelItems()
		for item in selItems:
			cmds.textScrollList( self.tsl, edit=True, ri=item )
		
	def remAllItems(self):
		'''
		Remove all items from the textScrollList
		'''
		cmds.textScrollList( self.tsl, edit=True, ra=True)
			
	
	def appendAll(self, items):
		'''
		Adds the items into the textScrollList even if a duplicate name
		exists.
		'''
		cmds.textScrollList( self.tsl, edit=True, append=items)
		
	def append(self, items, output=1):
		'''
		Adds only unique elements to the textScrollList. 
		'''
		for item in items:
			if( item not in self.getAllItems() ):
				self.appendAll(item)
				if(output):
					print("Adding: %s" %item)
			else:
				print("Item: %s is already in the list." %item)
	'''
	def __add__(self, tslObj):
		newItems = tslObj.getAllItems()
		curItems = self.tsl.getAllItems()
				    
		return curItems.extend(newItems)
	
	def __eq__(self, tslObj):
		newItems = tslObj.getAllItems()
		curItems = self.tsl.getAllItems()
		
		
	
	I need to create a generic class for the elements that always exist.
	enable and disable
	size get and set
	'''

"""
myTsl = TextScrollList(items=cmds.ls(sl=True))
myTsl2 = TextScrollList(items=cmds.ls("*_bind", sl=True))

if( myTsl1 == myTsl2 ):

from gui import TextScrollList	
from callback import Callback


cmds.window()
cmds.columnLayout()
tsl = TextScrollList()
cmds.button( label="Remove All", c=Callback( tsl.remAllItems ) )
cmds.button( label="Remove Sel", c=Callback( tsl.remSelItems ) )
cmds.showWindow()

global tsl
scriptName = __name__
cmds.window()
cmds.columnLayout()
tsl = TextScrollList()
cmds.button( label="Remove All", c=scriptName + ".tsl.remAllItems('%s', '%s')" %(value1, value2) )
cmds.button( label="Remove Sel", c=scritpName + ".tsl.remSelItems()" )
cmds.showWindow()



import textScrollList
reload(textScrollList)


from textScrollList import TextScrollList	
from mecMaya.callback import Callback
import maya.cmds as cmds


cmds.window()
cmds.columnLayout()
tsl = TextScrollList()
tsl2 = TextScrollList( items=cmds.ls(sl=True) )
cmds.button( label="Remove All", c=Callback( tsl.remAllItems ) )
cmds.button( label="Remove Sel", c=Callback( tsl.remSelItems ) )
cmds.showWindow()

tsl.h = 150
tsl.w = 150
"""



