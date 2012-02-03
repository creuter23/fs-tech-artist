
import maya.cmds as cmds
		
class Window(object):
	def __init__(self, title="Test Window", width=300, height=300):

		self.win = cmds.window( t=title, w=width, h=height)
		
	def show(self):
		cmds.showWindow( self.win )
	
	def getWidth(self):
		return cmds.window(self.win, q=True, w=True)
		
	def getHeight(self):
		return cmds.window(self.win, q=True, h=True)
		
	def getSize(self):
		return cmds.window(self.win, q=True, widthHeight=True)
		
	def setWidth(self, newWidth):
		cmds.window(self.win, e=True, w=newWidth)
		
	def setHeight(self, newHeight):
		cmds.window(self.win, e=True, h=newHeight)
		
	def setSize(self, newSize):
		cmds.window(self.win, e=True, widthHeight=newSize)
	
	def setSizeOffset(self, offset=(0,0)):
		cmds.window(self.win, e=True, 
			widthHeight=( self.getWidth() + offset[0], self.getHeight() + offset[1]))
			
	def getTitle(self):
		'''
		Returns the title of the window.
		'''
		return cmds.window(self.win, q=True, title=True)
		
	def setTitle(self, newTitle):
		'''
		Sets the title of the window
		'''
		cmds.window(self.win, e=True, title=newTitle)
		
	def getPos(self):
		'''
		Get the current position of the window.
		'''
		return cmds.window(self.win, q=True, topLeftCorner=True)
	
	def getPosX(self):
		'''
		Gets the left edge position.
		'''
		return cmds.window(self.win, q=True, leftEdge=True)
		
	def getPosY(self):
		'''
		Gets the top edge position.
		'''
		return cmds.window(self.win, q=True, topEdge=True)
	
	def setPos(self, pos):
		'''
		Sets the Positions of the window
		'''
		cmds.window(self.win, e=True, topLeftCorner=pos)
		
	def setPosX(self, pos):
		'''
		Sets the left edge positions of the window
		'''
		cmds.window(self.win, e=True, leftEdge=pos)
		
	def setPosY(self, pos):
		'''
		Sets the top edge positions of the window
		'''
		cmds.window(self.win, e=True, topEdge=pos)
	
	def setPosOffset(self, pos=(0,0)):
		'''
		Moves the window relative to its current position.
		'''
		self.setPosX(self.getPosX() + pos[0] )
		self.setPosY(self.getPosY() + pos[1] )
		
		
		
	def setPosXOffset(self, pos):
		cmds.window(self.win, e=True, leftEdge=self.getPosX() + pos)
		
	def setPosYOffset(self, pos):
		cmds.window(self.win, e=True, topEdge=self.getPosY() + pos)
		
class WinName(Window):
	def __init__(self, winName, title="Test Window", width=300, height=300):
		if( cmds.window(winName, q=True, ex=True) ):
			cmds.deleteUI(winName)
		self.win = cmds.window(winName, t=title, w=width, h=height)		
'''
Good features
- Getting all the children layouts
	- They can be stored in a list.
	- Maybe the heirarchy as well.
	
'''
	
	
