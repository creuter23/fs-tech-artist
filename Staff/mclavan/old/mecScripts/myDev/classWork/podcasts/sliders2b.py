'''
Blend Shapes
sliders2b.py

Description:
	- This script show some advanced topics to add more complexity to the slider function.
	- Features such as:
		- pythons string concatination

	
	
How to Run:

'''

import maya.cmds as cmds

print("Slider Functions 2")


'''
Part 2a
Slider Function
Python's String Concatination
'''

scriptName = __name__

def sliderBld_old(attrLabel, attr, curParent, minVal=0, maxVal=1, reset=0):
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
	
	
# Typical in most Languages.	
command=scriptName + ".key( '" + attr + "')"

# Python's Methods
# %s stand-in

line = "I'd like to place a value here: ?? I'll have to break the string up"
# Standard way
value = 33
line = "I'd like to place a value here: " + value + " I'll have to break the string up"
# type casting error, Can't add strings and integer together
line = "I'd like to place a value here: " + str(value) + " I'll have to break the string up"


# Python's Method
# % key - The precent is a standing marker followd by what type of values is going to be placed in.
# %s - string 
line = "I'd like to place a value here: %s I'll have to break the string up" %value
# No typecasting and easy.

# Multiple usage
line = "I'd like to place a value here: ?? and my name is ??."
line = "I'd like to place a value here: %s and my name is %s." %(value, "Michael")


# attribute needs to be sent to the function.
btn1 = cmds.button(label="Key", 
	# command=scriptName + ".key( '" + attr + "')")
	command="%s.key( '%s' )" %(scriptName, attr))

# attribute and reset value need to sent to the function.
btn2 = cmds.button(label="Reset",
	# command=scriptName + ".reset( '" + attr + "', " + str(reset) + ")")
	command="%s.reset( '%s', %s )" %(scriptName, attr, reset))



def sliderBld(attrLabel, attr, curParent, minVal=0, maxVal=1, reset=0):
	frm = cmds.formLayout(parent=curParent)
	
	text = cmds.text( label=attrLabel, w=60 )
	field = cmds.floatField( w=60, min=minVal, max=maxVal)
	slider = cmds.floatSlider( w=100, min=minVal, max=maxVal )
	
	# attribute needs to be sent to the function.
	btn1 = cmds.button(label="Key", 
		# command=scriptName + ".key( '" + attr + "')")
		command="%s.key( '%s' )" %(scriptName, attr))

	# attribute and reset value need to sent to the function.
	btn2 = cmds.button(label="Reset",
		# command=scriptName + ".reset( '" + attr + "', " + str(reset) + ")")
		command="%s.reset( '%s', %s )" %(scriptName, attr, reset))

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
