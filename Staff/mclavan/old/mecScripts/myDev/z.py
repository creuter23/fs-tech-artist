
import os, os.path
import maya.cmds as cmds
print("Hello Script: A")

print(__file__)

# Get extension

filePath = os.path.split(__file__)
iconDir = os.path.join( filePath[0], "icons" )

print(iconDir)




class modTools:
	'''
	Creates a window.
	
	def __init__(self):
		self.win = cmds.window(title="Class Test", w=300, h=300)
		self.winParts()
		cmds.showWindow(self.win)
	'''
	def win(self):
		'''
		if( cmds.window(self.win, q=True, ex=True) ):
			cmds.deleteUI(self.win)
		'''
		self.win = cmds.window(title="Class Test", w=300, h=300)
		self.winParts()
		cmds.showWindow(self.win)		
	'''	
	def show(self):
		cmds.showWindow(self.win)
	'''
	def delHist(self, *args):
		cmds.delete(ch=1)
	'''
	def delHist2(self,*args):
		cmds.delete(ch=1)
	def delHist3(*args):
		cmds.delete(ch=1)
	'''

	#lambda function

	def myLattice(self,dx=4, dy=4, dz=4):
		print("Lattice Created: %s" %dx )
		print("Lattice Created: %s" %dy )
		print("Lattice Created: %s" %dz )
		
		
	def mySmooth(self):
		smtVal = cmds.intField( self.divX, q=True, value=True)
		print("Smooth Poly: %s" %smtVal)
	
	def winParts(self):
		self.mainCol = cmds.columnLayout()
		cmds.button( label="Press Me" )
		cmds.button( label="Del Hist", c=self.delHist)
		self.divX = cmds.intField( w=40, value=4, min=2, max=10)
		cmds.button( label="Lattice", c=(lambda *args: self.myLattice(2,4,6)))
		# cmds.button( label="Lattice2", c=self.myLattice )
		cmds.button( label="Smooth", c=(lambda *args: self.mySmooth()))
		print(os.path.join(iconDir,"3dsetup.xmp"))

		cmds.picture( image=os.path.join(iconDir,"3dsetup.xpm") )
		cmds.button(label="hello")

