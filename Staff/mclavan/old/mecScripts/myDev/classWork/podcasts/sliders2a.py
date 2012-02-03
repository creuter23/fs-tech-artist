'''
Blend Shapes
sliders2a.py

Description:
	- This script show some advanced topics to add more complexity to the slider function.
	- Features such as:
		- formLayout
		- pythons string concatination
		- lambda functions
	
	
How to Run:

'''

import maya.cmds as cmds

print("Slider Functions 2")


'''
Part 2a
Slider Function
formLayout
'''

scriptName = __name__

def sliderBld_old(attrLabel, attr, curParent, minVal=0, maxVal=1, reset=0):
	row = cmds.rowColumnLayout(nc=3, cw=[[1,280],[2,50],[3,50]],
		parent=curParent)
	slider = cmds.floatSliderGrp( label=attrLabel, field=True, min=minVal, max=maxVal,
		cw=[[1,60], [2,60], [3,100]])
	
	# attribute needs to be sent to the function.
	cmds.button(label="Key", 
		command=scriptName + ".key( '" + attr + "')")
	'''
	# Python's string concatination (adding strings)
	cmds.button(label="Key", 
		command=scriptName + ".key('%s')" %attr)  
		# The %s means its a stand in for a string.  
		# %attr is the value being placed inside the string.
		# %(attr, ??? ) for multiple strings.
	'''
	# attribute and reset value need to sent to the function.
	cmds.button(label="Reset",
		command=scriptName + ".reset( '" + attr + "', " + str(reset) + ")")
	'''
	cmds.button(label="Reset",
		command=scriptName + ".reset('%s', %s)" %(attr, reset))
	# Multiple strings can be inputted
	# %( attr, reset ) places values by order.
	'''
	cmds.connectControl( slider, attr )
	
	cmds.setParent(curParent)
	return row
	

'''
Part 1
formLayout
'''
	
	slider = cmds.floatSliderGrp( label=attrLabel, field=True, min=minVal, max=maxVal,
		cw=[[1,60], [2,60], [3,100]])
	cmds.button(label="Key", 
		command=scriptName + ".key( '" + attr + "')")
	cmds.button(label="Reset",
		command=scriptName + ".reset( '" + attr + "', " + str(reset) + ")")
	

	text = cmds.text( label=attrLabel, w=60 )
	field = cmds.floatField( w=60, min=minVal, max=maxVal)
	slider = cmds.floatSlider( w=100, min=minVal, max=maxVal )
	
	
'''
3 Steps to working with formLayout
1) Declair a formLayout.
2) Create GUI controls. (Must be named)
3) Position.

'''

# 1)
frm = cmds.formLayout()

# 2)
text = cmds.text( label=attrLabel, w=60 )
field = cmds.floatField( w=60, min=minVal, max=maxVal)
slider = cmds.floatSlider( w=100, min=minVal, max=maxVal )
	
# 3)
# 4 Slides "top", "left", "right", & "bottom"
# Normaly set 2.
# 3 Main Flags
# attachForm 
# attachControl
# attachPostion
# [control, side, offset]  or [control, side, offset, otherControl]

# attach Form (text control)
cmds.formLayot( frm, edit=True, attachForm=[[text, "left", 0], [text, "top", 0]] )
# attachForm and attachControl
cmds.formLayout( frm, edit=True, attachForm=[field, "top", 0], attachControl=[field, "left", 0, text] )
cmds.formLayout( frm, edit=True, attachForm=[slider, "top", 0], attachControl=[slider, "left", 0, field] )


def sliderBld(attrLabel, attr, curParent, minVal=0, maxVal=1, reset=0):
	frm = cmds.formLayout(parent=curParent)
	
	text = cmds.text( label=attrLabel, w=60 )
	field = cmds.floatField( w=60, min=minVal, max=maxVal)
	slider = cmds.floatSlider( w=100, min=minVal, max=maxVal )
	
	# attribute needs to be sent to the function.
	btn1 = cmds.button(label="Key", 
		command=scriptName + ".key( '" + attr + "')")

	# attribute and reset value need to sent to the function.
	btn2 = cmds.button(label="Reset",
		command=scriptName + ".reset( '" + attr + "', " + str(reset) + ")")

	# attach Form (text control)
	cmds.formLayot( frm, edit=True, attachForm=[[text, "left", 0], [text, "top", 0]] )
	# attachForm and attachControl
	cmds.formLayout( frm, edit=True, attachForm=[field, "top", 0], attachControl=[field, "left", 0, text] )
	cmds.formLayout( frm, edit=True, attachForm=[slider, "top", 0], attachControl=[slider, "left", 0, field] )
	cmds.formLayout( frm, edit=True, attachForm=[btn1, "top", 0], attachControl=[btn1, "left", 0, slider] )
	cmds.formLayout( frm, edit=True, attachForm=[btn2, "top", 0], attachControl=[btn2, "left", 0, btn1] )


	cmds.connectControl( slider, attr )
	cmds.connectControl( field, attr )
	
	cmds.setParent(curParent)
	return row
	
	
def key(attr):
	cmds.setKeyframe(attr)
	
def reset(attr, value):
	cmds.setAttr( attr, value )
