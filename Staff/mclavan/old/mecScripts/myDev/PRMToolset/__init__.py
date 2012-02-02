'''
Production Modeling Toolset
creator: Michael Corinella
contact: www.MCorinella@Fullsail.com
date Started: 06/23/2010



	

Script Idea:
	A whole List of commonly used modeling tools in one convienient location
	
Main Objectives:
	For the user to be able to easily locate and use common modeling tools
	
Extra Objectives:
	Right-Click functionality, to be able to change button colors.
	
How the script works:
	Use these tools all for polygon modeling.
	
*Acknowledgments:
	The Production Modeling Toolset (A.K.A) The Money Brick was originally 
	scripted by Dan Neufeldt (nerfsafetysquid.com).	
	Callback function created by Nathan Horn inspired by pymel (Luma Studio)
	EdgeLoop function created by Michael Clavan.

How to Run:
import PRMToolset
PRMToolset.gui()

'''

import prm2009.proModTool as prm2009
import prm2010.proModTool as prm2010
import prm2011.proModTool as prm2011

import maya.cmds as cmds

def gui():
	mayaVer = cmds.about( version=True )
	if(mayaVer == "2009"):
		print("Launching PRMToolset for Maya 2009.")
		prm2009.gui()
	elif(mayaVer == "2010"):
		print("Launching PRMToolset for Maya 2010.")
		prm2010.gui()
	elif(mayaVer == "2011"):
		# print("Launching PRMToolset for Maya 2011.")
		# prm2011.gui()
		print("Maya 2011 isn't complete.")
	else:
		print("Launching PRMToolset for Maya 2009.")
		prm2009.gui()
	
	#proModTool.gui()



