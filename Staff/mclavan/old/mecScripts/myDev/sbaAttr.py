'''
This script will create an attribute for multiple selected objects.

Advanced
Integrate a textScrollList to be able add multiple attributes to single or
  multiple objects.
'''

import maya.cmds as cmds

win = "sbaAttrWin"
scriptName = __name__

def gui():
	'''
	Create a gui to add attributes to the selected objects.
	'''
	

	
	
	'''
	<---- Create an if statement to check to see if the window exists and if
		it does delete it.
	
	'''


	'''
	<---- You may have noticed that you window sizes aren't allways the correct
	    size when you generate your window.  This is because the windows
	    keep their preferences.
	    
	    -  Check to see if the window has preferences and if it does remove them.
	    	(Hint: removing is a flag)
	    -  Research command windowPref
		 
	'''

	cmds.window(win, t="Create Attr", w=200, h=160)
	
	cmds.columnLayout()
	
	cmds.text(l="1. Selected objects for new attrs.", w=200, al="center")
	
	cmds.textFieldGrp("sbaAttrAName", l="Attr Name: ", w=200, cw2=[75, 125])
	
	'''
	<---- How many radio buttons does the command have?  What are they going to
	     be used for?
	'''
	
	cmds.radioButtonGrp("sbaAttrRType", l="Data Type:", labelArray2=["float", "int"], 
		nrb=2, cw3=[75, 50, 40], sl=1)
	
	cmds.rowLayout(nc=4, cw4=[45, 55, 45, 50])
	
	'''
	<---- Explain what are the flags onc and ofc doing for these checkBox commands?
	     What function are the gui components below going to be used for?
	'''
	cmds.checkBox("sbaAttrCBMin", l="Min", w=45,
		onc='sbaAttr.cmds.floatField("sbaAttrMin", e=True, en=True)',
		ofc='sbaAttr.cmds.floatField("sbaAttrMin", e=True, en=False)')
	cmds.floatField("sbaAttrMin", w=50, en=False)
	cmds.checkBox("sbaAttrCBMax", l="Max", w=45,
		onc='sbaAttr.cmds.floatField("sbaAttrMax", e=True, en=True)',
		ofc='sbaAttr.cmds.floatField("sbaAttrMax", e=True, en=False)')
	cmds.floatField("sbaAttrMax", w=50, en=False)
	cmds.setParent("..")
	
	cmds.button(l="Create Attr", w=200,
		c="sbaAttr.sbaMultiAttrs()")
	
	cmds.showWindow(win)


def sbaMultiAttrs():
	'''
	This function will create the attributes on the selected objects.
	'''	
	#Getting Name, Min, Max, Data Type.

	
	
	'''
	<---- Retrieve information from the GUI.  The above varables are the
		names of the gui components we will need to retrieve.  Use them in
		the retreving process below.  
	'''





	'''
	<---- From the radio buttons on the gui.  The first radio button is ment
		to equal data type double, the second "long".
	      - Declare a variable called (dataType) first.
	      - Then create a if statement to assign the variable dataType ether
	      	"double" or "long" depending on which radioButton the user selected.
	'''
	



	# Now looping though multiple attributes.
	
	'''
	<----  Use the ls command to grab the selected object in the scene and
	    catch the contents into a variable called (objs).
	    	
	'''

	
	
	
	for obj in objs:
		
		'''
		<---- Create an attribute using the information obtained from the
		      gui.
		      
		      Research these flags and fill them with the information 
		      obtained from the gui.
		      (Flags) 
		      ln
		      at
		      k=True
		      r=True
		      s=True
		      w=True
		      
		      
		'''


		
		'''
		<---- Explain what is going on with these two if statements.
		'''
		if(chBoxMin):
			cmds.addAttr((obj+"."+attrName), e=True, min=fieldMin)
		if(chBoxMax):
			cmds.addAttr((obj+"."+attrName), e=True, max=fieldMax)
		


