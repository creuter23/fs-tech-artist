"""
colorPopup.py
Michael Clavan

Hey Mike check out the code below.  I'll introduce you to Classes on Monday, but below it a ColorButton class.
Mainly I created it to over write the button command so it would give you a pop up to change the button color.
Below is a test gui code.  

btn = ColorButton(btnLabel="Check", btnCommand=delHist, btnWidth=100, btnHeight=25,)

I decided to use the color editor instead, but I left you window code in as well.  So, you could see an alternatives.

You can ether import this into the other script or copy the class info straight into the toolset.
Give it a try and see if you can get it working.  Give me a call if your having any difficulty.
"""

import maya.cmds as cmds
class ColorButton:
	
	def __init__(self, btnLabel, btnCommand, btnWidth=None, btnHeight=None, btnParent=None):
		self.btnCommand=btnCommand

		if( btnParent ):
			self.btnName = cmds.button( label=btnLabel, w=btnWidth, h=btnHeight, parent=btnParent,
				command=btnCommand)			
		else:
			self.btnName = cmds.button( label=btnLabel, w=btnWidth, h=btnHeight, 
				command=btnCommand)
		self.menu = cmds.popupMenu(parent=self.btnName)
		cmds.menuItem(parent=self.menu, l="Change Color", c=self.applyColor2)
	"""	
	def colorWin(self, *args):
		self.colorWindow = cmds.window( t="Color Picker", w=420, h=80, tlb=1)
		cmds.windowPref(self.colorWindow, e=1, remove=True)
		cmds.windowPref(self.colorWindow, e=1, h=80)
		cmds.windowPref(self.colorWindow, e=1, w=420)

		cmds.columnLayout()
		cmds.text(h=5)
		self.sliderGrp = cmds.colorSliderButtonGrp("clrButton",  label="Button Color", buttonLabel="Apply", 
			bc=self.applyColor, rgb=(1, 0, 0), columnWidth=[[1,100],[5, 40]])
		
		cmds.showWindow(self.colorWindow)

	def applyColor(self, *args):
		self.currentColor = cmds.colorSliderButtonGrp(self.sliderGrp, q=True, rgb=True)
		cmds.button(self.btnName, edit=True, bgc=self.currentColor)
		cmds.deleteUI(self.colorWindow)
	"""
	def applyColor2(self, *args):
		tempVal = cmds.colorEditor(rgb=[1,0,0])
		tempColors = [float(x) for x in tempVal.split()]
		self.colorVal = tempColors[0:3]
		if( tempColors[-1] ):
			cmds.button(self.btnName, edit=True, bgc=self.colorVal)

"""
cmds.window()
mainCol = cmds.columnLayout()
btn = ColorButton(btnLabel="Check", btnCommand=delHist, btnWidth=100, btnHeight=25,)
btn2 = ColorButton(btnLabel="Check", btnCommand=delHist, btnWidth=100, btnHeight=25, btnParent=mainCol)
cmds.showWindow()	

def delHist(*args):
	print("This function has been executed.")	
"""
