'''
Set Driven Keyframe (SDK)
sdk.py

Description:
	This script covers how to create set driven keyframes through code.
	
How to Run:


'''

import maya.cmds as cmds

print( "Set Driven Keyframes" )

'''
SDK
'''
# Driver (1)

# Driven (at least 1)

cmds.setDrivenKeyframe()

'''
Flags

# Driver"
currentDriver (cd) -->  "object.attr"
driverValue (dv)

# Driven
value (v)

'''
cmds.setDrivenKeyframe( "driven.attr", value=0,
	currentDriver="driver.attr", driverValue=0 )


'''
Example
Setting up a blend shape
'''
# Starting Point
cmds.setDrivenKeyframe( "blendShape1.smile", value=0,
	currentDriver="sliderIcon.tx", driverValue=0 )
# Ending Point
cmds.setDrivenKeyframe( "blendShape1.smile", value=1,
	currentDriver="sliderIcon.tx", driverValue=10 )



