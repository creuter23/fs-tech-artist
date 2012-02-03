'''
BlendShade Helper
blendHelp.py

Description:

How to Run:

import blendHelp
blendHelp.gui()

'''

'''
Part 1
Frames, Tabs, & Slider Function
'''
import maya.cmds as cmds

scriptName = __name__

def sliderBld(labelName, attr, currParent, minVal=0, maxVal=1, resetVal=0, cw1=60):
	frm = cmds.formLayout(parent=currParent)
	'''
	slider = cmds.floatSliderGrp( label=labelName, field=True, min=minVal, max=maxVal,
		cw=[[1,cw1],[2,60], [3,70]], co3=[0, 0, 10], cat=[3,"left",0])
	'''
	text = cmds.text( width=cw1, label=labelName, align="center" )
	field = cmds.floatField( min=minVal, max=maxVal, w=60 )
	slider = cmds.floatSlider( min=minVal, max=maxVal, w=100 )
	cmds.connectControl(field, attr)
	cmds.connectControl(slider, attr)
	btn1 = cmds.button( label="Key",
		command=scriptName + ".key('" + attr + "')")
	btn2 = cmds.button( label="Reset",
		command=scriptName + ".reset('" + attr + "', " + str(resetVal) +")" )

	# text position
	cmds.formLayout( frm, e=1, attachForm=[[text, "left", 0],[text, "top", 0]])
	# field position
	cmds.formLayout( frm, e=1, attachForm=[field, "top", 0], attachControl=[field, "left", 0, text])
	# slider position
	cmds.formLayout( frm, e=1, attachForm=[slider, "top", 0], attachControl=[slider, "left", 0, field])
	# buttons position
	cmds.formLayout( frm, e=1, attachForm=[btn1, "top", 0], attachControl=[btn1, "left", 0, slider])
	cmds.formLayout( frm, e=1, attachForm=[btn2, "top", 0], attachControl=[btn2, "left", 0, btn1])
	cmds.setParent( currParent )
	return frm
	
def key(obj):
	cmds.setKeyframe(obj)

	
def reset(attr, val):
	cmds.setAttr( attr, val )

'''
def gui():
	cmds.window()
	cmds.columnLayout()
	slider1 = sliderBld( 
	cmds.showWindow()
'''
	

