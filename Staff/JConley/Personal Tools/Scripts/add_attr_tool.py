"""Add Attributes Tool"""

"""
Author: Jennifer Conley
Date Modified: 8/22/11

Description: A GUI used to add attributes to various icons of a standard
biped rig.

How to run:
import add_attr_tool
reload (add_attr_tool)
add_attr_tool.gui()

"""

import maya.cmds as cmds
win = 'adder_win'
scriptname = __name__

"""
Creates a gui with buttons to easily add custom attributes to rig icons.
"""

def gui():
	if (cmds.window(win, q=True, ex=True)):
		cmds.deleteUI(win)		
		
	cmds.window(win, t="Attribute Adder", w=500, h=300)
	cmds.rowColumnLayout(nc=2, cw=[(1,75),(2,75)])
	
	cmds.button(label='Cog', command=scriptname + ".Cog()")
	cmds.button(label='Head', command=scriptname + ".Head()")
	cmds.button(label='Ik_Foot', command=scriptname + ".Ik_Foot()")
	cmds.button(label='Ik_Hand', command=scriptname + ".Ik_Hand()")
	cmds.button(label='Foot_Switch', command=scriptname + ".Foot_Switch()")
	cmds.button(label='Hand_Switch', command=scriptname + ".Hand_Switch()")
	cmds.button(label='Eyes', command=scriptname + ".Eyes()")	
	
	cmds.showWindow()
	
	
"""
Creates the fuctions for the buttons
	
"""

def Cog():
	import basic_attrs_cog
	reload (basic_attrs_cog)
	
def Head():
	import basic_attrs_head
	reload (basic_attrs_head)
	
def Ik_Foot():	
	import basic_attrs_ik_foot
	reload (basic_attrs_ik_foot)
	
def Ik_Hand():	
	import basic_attrs_ik_hand
	reload (basic_attrs_ik_hand)
	
	
def Foot_Switch():
	import basic_attrs_ikfk_foot
	reload (basic_attrs_ikfk_foot)

def Hand_Switch():
	import basic_attrs_ikfk_hand
	reload (basic_attrs_ikfk_hand)
	
def Eyes():
	import basic_attrs_eyes
	reload (basic_attrs_eyes)

