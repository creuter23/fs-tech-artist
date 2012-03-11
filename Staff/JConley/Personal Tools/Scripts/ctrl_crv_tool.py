"""Ctrl Curves Tool"""

"""
Author: Jennifer Conley
Date Modified: 8/31/11

Description: A tool to easily create controls curves for rigging.

How to run:
import ctrl_crv_tool
reload (ctrl_crv_tool)
ctrl_crv_tool.gui()

"""

import maya.cmds as cmds
import maya.mel as mel

win = 'ctrl_crv_win'
scriptname = __name__
width = 50
height=50


"""
Creates the window for the tool
"""
def gui():
	if (cmds.window(win, q=True, ex=True)):
		cmds.deleteUI(win)
		
	cmds.window(win, t='Ctrl Curve Tool', w=300)
	main_layout= cmds.columnLayout()
	
	tabs = cmds.tabLayout(w=300, imw=5, imh=5)

	child1 = cmds.columnLayout()
	
	cmds.frameLayout(l='Shapes', cll=True)
	cmds.rowColumnLayout(w=300, nc=4)
	cmds.button(l='Circle', c=scriptname + '.ctrl_circle()')
	cmds.button(l='Square', c=scriptname + '.ctrl_square()')
	cmds.button(l='Frame', c=scriptname + '.ctrl_frame()')
	cmds.button(l='Triangle', c=scriptname + '.ctrl_tri()')
	
	cmds.button(l='+', c=scriptname + '.ctrl_plus()')
	cmds.button(l='Swirl', c=scriptname + '.ctrl_swirl()')
	cmds.setParent('..')
	
	cmds.frameLayout(l='Arrows', cll=True)
	cmds.rowColumnLayout(w=300, nc=4)	
	cmds.button(l='Single', c=scriptname + '.ctrl_single()')
	cmds.button(l='Double', c=scriptname + '.ctrl_double()')
	cmds.button(l='Triple', c=scriptname + '.ctrl_triple()')
	cmds.button(l='Single Curve', c=scriptname + '.ctrl_sCurve()')
	
	cmds.button(l='Double Curve', c=scriptname + '.ctrl_dCurve()')
	cmds.button(l='180 Line', c=scriptname + '.ctrl_180()')
	cmds.button(l='270 Line', c=scriptname + '.ctrl_270()')
	cmds.setParent('..')
	
	cmds.frameLayout(l='Cogs / M_A', cll=True)
	cmds.rowColumnLayout(w=300, nc=4)	
	cmds.button(l='Move All', c=scriptname + '.ctrl_move_all()')	
	cmds.button(l='Sun', c=scriptname + '.ctrl_sun()')
	cmds.button(l='Quad', c=scriptname + '.ctrl_quad()')
	cmds.button(l='Oct', c=scriptname + '.ctrl_oct()')
	
	cmds.setParent(tabs)

	
	child2 = cmds.columnLayout()
	cmds.frameLayout(l='Shapes', cll=True)
	cmds.rowColumnLayout(w=300, nc=4)
	cmds.button(l='Box', c=scriptname + '.ctrl_box()')
	cmds.button(l='Diamond', c=scriptname + '.ctrl_dia()')
	cmds.button(l='Ring', c=scriptname + '.ctrl_ring()')
	cmds.button(l='Cone', c=scriptname + '.ctrl_cone()')
	
	cmds.button(l='Orb', c=scriptname + '.ctrl_orb()')
	cmds.button(l='Lever', c=scriptname + '.ctrl_lever()')
	cmds.button(l='Jack', c=scriptname + '.ctrl_jake()')
	cmds.button(l='Pointer', c=scriptname + '.ctrl_pointer()')
	cmds.setParent(tabs)

	child3 = cmds.columnLayout()
	cmds.frameLayout(l='Letters', cll=True)
	cmds.rowColumnLayout(w=300, nc=4)
	cmds.button(l='C', c=scriptname + '.ctrl_letter("C")')
	cmds.button(l='E', c=scriptname + '.ctrl_letter("E")')
	cmds.button(l='H', c=scriptname + '.ctrl_letter("H")')
	cmds.button(l='K', c=scriptname + '.ctrl_letter("K")')
	
	cmds.button(l='L', c=scriptname + '.ctrl_letter("L")')
	cmds.button(l='R', c=scriptname + '.ctrl_text("R")')
	cmds.button(l='S', c=scriptname + 'ctrl_letter("S")')
	cmds.setParent('..')
	
	cmds.frameLayout(l='Text', cll=True)
	cmds.rowColumnLayout(w=300, nc=4)
	cmds.button(l='Rt', c=scriptname + '.ctrl_text("Rt")')
	cmds.button(l='Lf', c=scriptname + '.ctrl_text("Lf")')
	cmds.button(l='Ik / Fk', c=scriptname + '.ctrl_text("Ik / FK")')
	cmds.button(l='Gui', c=scriptname + '.ctrl_text("Gui")')
	
	cmds.button(l='Blend Shapes', c=scriptname + '.ctrl_text("Blend Shapes")')
	cmds.setParent(tabs)

	cmds.tabLayout(tabs, e=True, tl=([child1, '2D'], [child2, '3D'], [child3, 'Text']))
	
	cmds.showWindow()
	
	
"""
Creates the functions for the text tab control curves.
"""

def ctrl_letter(var):
	"""
	Creates letters made from single curves.
	"""
	cmds.textCurves(ch=0, f='Times New Roman', t=var)
	cmds.ungroup()
	cmds.ungroup()
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot as been centered.'


def ctrl_text(var):
	"""
	Creates letters and text made from multipe curves.
	"""
	cmds.textCurves(ch=0, f='Times New Roman', t=var)
	cmds.ungroup()
	cmds.ungroup()
	print 'Curves have been ungrouped.'
	
	curves = cmds.ls(sl=True)
	cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
	print 'Freezing transforms on curves.'
	
	cmds.pickWalk(d='Down')
	shapes = cmds.ls(sl=True)
	print 'Creating a list of curve shape nodes.'
	
	
	parent_shapes = shapes[1:]
	delete_curves = curves[1:]
	print 'Slicing lists for parenting and deleting purposes.'
	
	cmds.select(parent_shapes, r=True)
	cmds.select(curves[0], add=True)
	cmds.parent(r=True, s=True)
	print 'Curve list has been parented into single curve.'
	
	cmds.select(delete_curves, r=True)
	mel.eval('doDelete')
	print 'Unused groups have been deleted.'
	
	cmds.select(curves[0])
	mel.eval('CenterPivot')
	print ('End result curve have been selected and its pivot has been centered.')


"""
Creates the functions for the 2D tab control curves.
"""
def ctrl_circle():
	cmds.circle(c=[0, 0, 0], nr=[0, 1, 0], sw=360, r=1,
		d=3, ut=0, tol=.01, s=8, ch=1)
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'
	
def ctrl_square():
	mel.eval('curve -d 1 -p -1 -1 0 -p -1 1 0 -p 1 1 0 -p 1 -1 0 -p -1 -1 0 -k 0 -k 1 -k 2 -k 3 -k 4')
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'


def ctrl_frame():
	mel.eval('curve -d 1 -p -5 5 0 -p 5 5 0 -p 5 -5 0 -p -5 -5 0 -p -5 5 0 -p -4 4 0 -p 4 4 0 -p 5 5 0 -p 4 4 0 -p 4 -4 0 -p 5 -5 0 -p 4 -4 0 -p -4 -4 0 -p -5 -5 0 -p -4 -4 0 -p -4 4 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15')
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'


def ctrl_tri():
	mel.eval('curve -d 1 -p -4 0 4 -p 4 0 4 -p 0 0 -3 -p -4 0 4 -k 0 -k 1 -k 2 -k 3')
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'


def ctrl_plus():
	mel.eval('curve -d 1 -p 0.4 0 -0.4 -p 0.4 0 -2 -p -0.4 0 -2 -p -0.4 0 -0.4 -p -2 0 -0.4 -p -2 0 0.4 -p -0.4 0 0.4 -p -0.4 0 2 -p 0.4 0 2 -p 0.4 0 0.4 -p 2 0 0.4 -p 2 0 -0.4 -p 0.4 0 -0.4 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12')
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'


def ctrl_swirl():
	mel.eval('curve -d 3 -p 0.474561 0 -1.241626 -p 0.171579 0 -1.214307 -p -0.434384 0 -1.159672 -p -1.124061 0 -0.419971 -p -1.169741 0 0.305922 -p -0.792507 0 1.018176 -p -0.0412486 0 1.262687 -p 0.915809 0 1.006098 -p 1.258635 0 0.364883 -p 1.032378 0 -0.461231 -p 0.352527 0 -0.810017 -p -0.451954 0 -0.43765 -p -0.634527 0 0.208919 -p -0.0751226 0 0.696326 -p 0.292338 0 0.414161 -p 0.476068 0 0.273078 -k 0 -k 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 13 -k 13')
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'


def ctrl_single():
	mel.eval('curve -d 1 -p -1 0 0 -p 1 0 0 -p 1 1 0 -p 1 2 0 -p 1 3 0 -p 2 3 0 -p 0 5 0 -p -2 3 0 -p -1 3 0 -p -1 2 0 -p -1 1 0 -p -1 0 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11')
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'


def ctrl_double():
	mel.eval('curve -d 1 -p 0 1 0 -p 1 1 0 -p 2 1 0 -p 3 1 0 -p 3 2 0 -p 4 1 0 -p 5 0 0 -p 4 -1 0 -p 3 -2 0 -p 3 -1 0 -p 2 -1 0 -p 1 -1 0 -p 0 -1 0 -p -1 -1 0 -p -2 -1 0 -p -3 -1 0 -p -3 -2 0 -p -4 -1 0 -p -5 0 0 -p -4 1 0 -p -3 2 0 -p -3 1 0 -p -2 1 0 -p -1 1 0 -p 0 1 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24')
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'
	
	
def ctrl_triple():
	mel.eval('curve -d 1 -p -1 1 0 -p -3 1 0 -p -3 2 0 -p -5 0 0 -p -3 -2 0 -p -3 -1 0 -p -1 -1 0 -p 1 -1 0 -p 3 -1 0 -p 3 -2 0 -p 5 0 0 -p 3 2 0 -p 3 1 0 -p 1 1 0 -p 1 3 0 -p 2 3 0 -p 0 5 0 -p -2 3 0 -p -1 3 0 -p -1 1 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19')
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'
	

def ctrl_quad():
	mel.eval('curve -d 1 -p 1 0 1 -p 3 0 1 -p 3 0 2 -p 5 0 0 -p 3 0 -2 -p 3 0 -1 -p 1 0 -1 -p 1 0 -3 -p 2 0 -3 -p 0 0 -5 -p -2 0 -3 -p -1 0 -3 -p -1 0 -1 -p -3 0 -1 -p -3 0 -2 -p -5 0 0 -p -3 0 2 -p -3 0 1 -p -1 0 1 -p -1 0 3 -p -2 0 3 -p 0 0 5 -p 2 0 3 -p 1 0 3 -p 1 0 1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24')
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'


def ctrl_oct():
	mel.eval('curve -d 1 -p -1.8975 0 0 -p -1.4025 0 0.37125 -p -1.4025 0 0.12375 -p -0.380966 0 0.157801 -p -1.079222 0 0.904213 -p -1.254231 0 0.729204 -p -1.341735 0 1.341735 -p -0.729204 0 1.254231 -p -0.904213 0 1.079222 -p -0.157801 0 0.380966 -p -0.12375 0 1.4025 -p -0.37125 0 1.4025 -p 0 0 1.8975 -p 0.37125 0 1.4025 -p 0.12375 0 1.4025 -p 0.157801 0 0.380966 -p 0.904213 0 1.079222 -p 0.729204 0 1.254231 -p 1.341735 0 1.341735 -p 1.254231 0 0.729204 -p 1.079222 0 0.904213 -p 0.380966 0 0.157801 -p 1.4025 0 0.12375 -p 1.4025 0 0.37125 -p 1.8975 0 0 -p 1.4025 0 -0.37125 -p 1.4025 0 -0.12375 -p 0.380966 0 -0.157801 -p 1.079222 0 -0.904213 -p 1.254231 0 -0.729204 -p 1.341735 0 -1.341735 -p 0.729204 0 -1.254231 -p 0.904213 0 -1.079222 -p 0.157801 0 -0.380966 -p 0.12375 0 -1.4025 -p 0.37125 0 -1.4025 -p 0 0 -1.8975 -p -0.37125 0 -1.4025 -p -0.12375 0 -1.4025 -p -0.157801 0 -0.380966 -p -0.904213 0 -1.079222 -p -0.729204 0 -1.254231 -p -1.341735 0 -1.341735 -p -1.254231 0 -0.729204 -p -1.079222 0 -0.904213 -p -0.380966 0 -0.157801 -p -1.4025 0 -0.12375 -p -1.4025 0 -0.37125 -p -1.8975 0 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -k 38 -k 39 -k 40 -k 41 -k 42 -k 43 -k 44 -k 45 -k 46 -k 47 -k 48')
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'


def ctrl_sCurve():
	mel.eval('curve -d 1 -p -0.251045 0 1.015808 -p -0.761834 0 0.979696 -p -0.486547 0 0.930468 -p -0.570736 0 0.886448 -p -0.72786 0 0.774834 -p -0.909301 0 0.550655 -p -1.023899 0 0.285854 -p -1.063053 0 9.80765e-009 -p -0.961797 0 8.87346e-009 -p -0.926399 0 0.258619 -p -0.822676 0 0.498232 -p -0.658578 0 0.701014 -p -0.516355 0 0.802034 -p -0.440202 0 0.841857 -p -0.498915 0 0.567734 -p -0.251045 0 1.015808 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15')
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'
	
	
def ctrl_dCurve():
	mel.eval('curve -d 1 -p -0.251045 0 -1.015808 -p -0.761834 0 -0.979696 -p -0.486547 0 -0.930468 -p -0.570736 0 -0.886448 -p -0.72786 0 -0.774834 -p -0.909301 0 -0.550655 -p -1.023899 0 -0.285854 -p -1.063053 0 9.80765e-009 -p -1.023899 0 0.285854 -p -0.909301 0 0.550655 -p -0.72786 0 0.774834 -p -0.570736 0 0.886448 -p -0.486547 0 0.930468 -p -0.761834 0 0.979696 -p -0.251045 0 1.015808 -p -0.498915 0 0.567734 -p -0.440202 0 0.841857 -p -0.516355 0 0.802034 -p -0.658578 0 0.701014 -p -0.822676 0 0.498232 -p -0.926399 0 0.258619 -p -0.961797 0 8.87346e-009 -p -0.926399 0 -0.258619 -p -0.822676 0 -0.498232 -p -0.658578 0 -0.701014 -p -0.516355 0 -0.802034 -p -0.440202 0 -0.841857 -p -0.498915 0 -0.567734 -p -0.251045 0 -1.015808 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28')	
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'	
	
	
def ctrl_180():
	mel.eval('circle -c 0 0 0 -nr 0 1 0 -sw -180 -r 1 -d 3 -ut 0 -tol 0.01 -s 8 -ch 0')	
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'


def ctrl_270():
	mel.eval('curve -d 3 -p -0.707107 0 -0.707107 -p -0.570265 0 -0.843948 -p -0.205819 0 -1.040044 -p 0.405223 0 -0.978634 -p 0.881027 0 -0.588697 -p 1.059487 0 0 -p 0.881027 0 0.588697 -p 0.405223 0 0.978634 -p -0.205819 0 1.040044 -p -0.570265 0 0.843948 -p -0.707107 0 0.707107 -k 0 -k 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 8 -k 8')	
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'
	
def ctrl_sun():
	ctrl = mel.eval('curve -d 3 -p 7.06316e-009 0 -1 -p 0.104714 0 -0.990425 -p 0.314142 0 -0.971274 -p 0.597534 0 -0.821244 -p 0.822435 0 -0.597853 -p 0.96683 0 -0.314057 -p 1.016585 0 -2.28604e-005 -p 0.96683 0 0.314148 -p 0.822435 0 0.597532 -p 0.597534 0 0.822435 -p 0.314142 0 0.96683 -p 1.22886e-008 0 1.016585 -p -0.314142 0 0.96683 -p -0.597534 0 0.822435 -p -0.822435 0 0.597532 -p -0.96683 0 0.314148 -p -1.016585 0 -2.29279e-005 -p -0.96683 0 -0.314057 -p -0.822435 0 -0.597853 -p -0.597534 0 -0.821244 -p -0.314142 0 -0.971274 -p -0.104714 0 -0.990425 -p 7.06316e-009 0 -1 -k 0 -k 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 20 -k 20')
	cmds.select((ctrl + '.ep[1]'), (ctrl + '.ep[3]'), (ctrl + '.ep[5]'), (ctrl + '.ep[7]'), (ctrl + '.ep[9]'), (ctrl + '.ep[11]'), (ctrl + '.ep[13]'), (ctrl + '.ep[15]'), (ctrl + '.ep[17]'), (ctrl + '.ep[19]'), r=True)
	cmds.scale(0.732056, 0.732056, 0.732056, p=[0, 0, 0], r=True)
	cmds.select(ctrl)
	cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'
	
	
	
def ctrl_move_all():
	base_circle = mel.eval('circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1.5 -d 3 -ut 0 -tol 0.01 -s 8 -ch 0')
	arrow_list = []
	arrow1 = mel.eval('curve -d 1 -p 1.75625 0 0.115973 -p 1.75625 0 -0.170979 -p 2.114939 0 -0.170979 -p 2.114939 0 -0.314454 -p 2.473628 0 -0.0275029 -p 2.114939 0 0.259448 -p 2.114939 0 0.115973 -p 1.75625 0 0.115973 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7')
	arrow2 = mel.eval('curve -d 1 -p 0.143476 0 -1.783753 -p 0.143476 0 -2.142442 -p 0.286951 0 -2.142442 -p 0 0 -2.501131 -p -0.286951 0 -2.142442 -p -0.143476 0 -2.142442 -p -0.143476 0 -1.783753 -p 0.143476 0 -1.783753 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7')
	arrow3 = mel.eval('curve -d 1 -p -1.75625 0 -0.170979 -p -2.114939 0 -0.170979 -p -2.114939 0 -0.314454 -p -2.473628 0 -0.0275029 -p -2.114939 0 0.259448 -p -2.114939 0 0.115973 -p -1.75625 0 0.115973 -p -1.75625 0 -0.170979 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7')
	arrow4 = mel.eval('curve -d 1 -p -0.143476 0 1.728747 -p -0.143476 0 2.087436 -p -0.286951 0 2.087436 -p 0 0 2.446125 -p 0.286951 0 2.087436 -p 0.143476 0 2.087436 -p 0.143476 0 1.728747 -p -0.143476 0 1.728747 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7')
	arrow_list.append(arrow1)
	arrow_list.append(arrow2)
	arrow_list.append(arrow3)
	arrow_list.append(arrow4)
	print 'Curves have been created and positioned.'
	
	cmds.select(arrow_list)
	cmds.pickWalk(d='Down')
	cmds.select(base_circle, add=True)
	cmds.parent(r=True, s=True)
	print 'Curve list has been parented into single curve.'
	
	cmds.select(arrow_list, r=True)
	mel.eval('doDelete')
	print 'Unused groups have been deleted.'
	
	cmds.select(base_circle)
	mel.eval('CenterPivot')
	print ('End result curve have been selected and its pivot has been centered.')	
	
	
"""	
Creates the fuctions for the 3D tab control curves.
"""
def ctrl_box():
	mel.eval('curve -d 1 -p 0.5 0.5 0.5 -p 0.5 0.5 -0.5 -p 0.5 -0.5 -0.5 -p 0.5 -0.5 0.5 -p 0.5 0.5 0.5 -p -0.5 0.5 0.5 -p -0.5 -0.5 0.5 -p 0.5 -0.5 0.5 -p -0.5 -0.5 0.5 -p -0.5 -0.5 -0.5 -p -0.5 0.5 -0.5 -p -0.5 0.5 0.5 -p -0.5 0.5 -0.5 -p 0.5 0.5 -0.5 -p 0.5 -0.5 -0.5 -p -0.5 -0.5 -0.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15')
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'
	
	
def ctrl_dia():
	mel.eval('curve -d 1 -p 0 0.699773 0 -p 0.707107 -0.00175397 0 -p 9.27258e-08 -0.00733389 -0.707107 -p 0 0.699773 0 -p 9.27258e-08 -0.00733389 -0.707107 -p -0.707107 -0.00175397 6.18172e-08 -p 0 0.699773 0 -p -0.707107 -0.00733389 -6.18172e-08 -p -3.09086e-08 -0.00733389 0.707107 -p 0 0.699773 0 -p -3.09086e-08 -0.00733389 0.707107 -p 0.707107 -0.00175397 0 -p 0 -0.708861 0 -p -3.09086e-08 -0.00733389 0.707107 -p 0 -0.708861 0 -p -0.707107 -0.00733389 -6.18172e-08 -p 0 -0.708861 0 -p 9.27258e-08 -0.00733389 -0.707107 -p 0 -0.708861 0 -p 0.707107 -0.00733389 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19')
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'


def ctrl_ring():
	mel.eval('curve -d 1 -p -1 0.0916408 0 -p -0.707107 0.0916408 0.707107 -p 0 0.0916408 1 -p 0.707107 0.0916408 0.707107 -p 1 0.0916408 0 -p 0.707107 0.0916408 -0.707107 -p 0 0.0916408 -1 -p -0.707107 0.0916408 -0.707107 -p -1 0.0916408 0 -p -1 -0.0916408 0 -p -0.707107 -0.0916408 -0.707107 -p -0.707107 0.0916408 -0.707107 -p -0.707107 -0.0916408 -0.707107 -p 0 -0.0916408 -1 -p 0 0.0916408 -1 -p 0 -0.0916408 -1 -p 0.707107 -0.0916408 -0.707107 -p 0.707107 0.0916408 -0.707107 -p 0.707107 -0.0916408 -0.707107 -p 1 -0.0916408 0 -p 1 0.0916408 0 -p 1 -0.0916408 0 -p 0.707107 -0.0916408 0.707107 -p 0.707107 0.0916408 0.707107 -p 0.707107 -0.0916408 0.707107 -p 0 -0.0916408 1 -p 0 0.0916408 1 -p 0 -0.0916408 1 -p -0.707107 -0.0916408 0.707107 -p -0.707107 0.0916408 0.707107 -p -0.707107 -0.0916408 0.707107 -p -1 -0.0916408 0 -p -1 0.0916408 0 -p -1 -0.0916408 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33')
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'


def ctrl_cone():
	mel.eval('curve -d 1 -p 0.5 -1 0.866025 -p -0.5 -1 0.866025 -p 0 1 0 -p 0.5 -1 0.866025 -p 1 -1 0 -p 0 1 0 -p 0.5 -1 -0.866025 -p 1 -1 0 -p 0 1 0 -p -0.5 -1 -0.866026 -p 0.5 -1 -0.866025 -p 0 1 0 -p -1 -1 -1.5885e-007 -p -0.5 -1 -0.866026 -p 0 1 0 -p -0.5 -1 0.866025 -p -1 -1 -1.5885e-007 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16')
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'

	
def ctrl_orb():
	mel.eval('circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 0.01 -s 8 -ch 1')
	base_circle = cmds.ls(sl=True)
	
	cmds.duplicate(rr=True)
	dup1 = cmds.ls(sl=True)
	cmds.setAttr(dup1[0] + '.rotateX', 90)
	
	cmds.duplicate(rr=True)
	dup2 = cmds.ls(sl=True)
	cmds.setAttr(dup2[0] + '.rotateY', 90)

	cmds.duplicate(rr=True)
	dup3 = cmds.ls(sl=True)
	cmds.setAttr(dup3[0] + '.rotateY', 45)
	print 'Curves have been created and positioned.'
	
	cmds.select(base_circle, dup1, dup2, dup3)
	cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
	print 'Freezing transforms on curves.'

	cmds.select(dup1, dup2, dup3, r=True)
	curves = cmds.ls(sl=True)
	cmds.pickWalk(d='Down')
	cmds.select(base_circle, add=True)
	cmds.parent(r=True, s=True)
	print 'Curve list has been parented into single curve.'
	
	cmds.select(curves, r=True)
	mel.eval('doDelete')
	print 'Unused groups have been deleted.'
	
	cmds.select(base_circle)
	mel.eval('CenterPivot')
	print ('End result curve have been selected and its pivot has been centered.')


def ctrl_lever():
	mel.eval('curve -d 1 -p 0 -1 0 -p 0 -2 0 -p 0 -3 0 -p 0 -4 0 -p 0 -5 0 -k 0 -k 1 -k 2 -k 3 -k 4')
	line = cmds.ls(sl=True)
	print 'Line curve has been created.'
	
	mel.eval('circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 0.01 -s 8 -ch 1')
	base_circle = cmds.ls(sl=True)
	
	
	cmds.duplicate(rr=True)
	circle_dup1 = cmds.ls(sl=True)
	cmds.setAttr(circle_dup1[0] + '.rotateX', 90)
	
	cmds.duplicate(rr=True)
	circle_dup2 = cmds.ls(sl=True)
	cmds.setAttr(circle_dup2[0] + '.rotateY', 90)
		
	cmds.duplicate(rr=True)
	circle_dup3 = cmds.ls(sl=True)
	cmds.setAttr(circle_dup3[0] + '.rotateY', 45)
	print 'Circle curves have been created.'
	
	cmds.select(line, base_circle, circle_dup1, circle_dup2, circle_dup3, r=True)
	cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
	print 'Freezing transforms on curves.'
	
	cmds.select(line, circle_dup1, circle_dup2, circle_dup3)
	curves = cmds.ls(sl=True)
	cmds.pickWalk(d='Down')
	shapes = cmds.ls(sl=True)
	
	cmds.select(shapes, base_circle, r=True)
	cmds.parent(r=True, s=True)
	print 'Curve list has been parented into single curve.'
	
	cmds.select(curves, r=True)
	mel.eval('doDelete')
	print 'Unused groups have been deleted.'
	
	cmds.select(base_circle, r=True)
	mel.eval('CenterPivot')
	print 'End result curve have been selected and its pivot has been centered.'
	

def ctrl_jake():
	mel.eval('curve -d 1 -p 0 0 0 -p 0.75 0 0 -p 1 0.25 0 -p 1.25 0 0 -p 1 -0.25 0 -p 0.75 0 0 -p 1 0 0.25 -p 1.25 0 0 -p 1 0 -0.25 -p 1 0.25 0 -p 1 0 0.25 -p 1 -0.25 0 -p 1 0 -0.25 -p 0.75 0 0 -p 0 0 0 -p -0.75 0 0 -p -1 0.25 0 -p -1.25 0 0 -p -1 -0.25 0 -p -0.75 0 0 -p -1 0 0.25 -p -1.25 0 0 -p -1 0 -0.25 -p -1 0.25 0 -p -1 0 0.25 -p -1 -0.25 0 -p -1 0 -0.25 -p -0.75 0 0 -p 0 0 0 -p 0 0.75 0 -p 0 1 -0.25 -p 0 1.25 0 -p 0 1 0.25 -p 0 0.75 0 -p -0.25 1 0 -p 0 1.25 0 -p 0.25 1 0 -p 0 1 0.25 -p -0.25 1 0 -p 0 1 -0.25 -p 0.25 1 0 -p 0 0.75 0 -p 0 0 0 -p 0 -0.75 0 -p 0 -1 -0.25 -p 0 -1.25 0 -p 0 -1 0.25 -p 0 -0.75 0 -p -0.25 -1 0 -p 0 -1.25 0 -p 0.25 -1 0 -p 0 -1 -0.25 -p -0.25 -1 0 -p 0 -1 0.25 -p 0.25 -1 0 -p 0 -0.75 0 -p 0 0 0 -p 0 0 -0.75 -p 0 0.25 -1 -p 0 0 -1.25 -p 0 -0.25 -1 -p 0 0 -0.75 -p -0.25 0 -1 -p 0 0 -1.25 -p 0.25 0 -1 -p 0 0.25 -1 -p -0.25 0 -1 -p 0 -0.25 -1 -p 0.25 0 -1 -p 0 0 -0.75 -p 0 0 0 -p 0 0 0.75 -p 0 0.25 1 -p 0 0 1.25 -p 0 -0.25 1 -p 0 0 0.75 -p -0.25 0 1 -p 0 0 1.25 -p 0.25 0 1 -p 0 0.25 1 -p -0.25 0 1 -p 0 -0.25 1 -p 0.25 0 1 -p 0 0 0.75 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -k 38 -k 39 -k 40 -k 41 -k 42 -k 43 -k 44 -k 45 -k 46 -k 47 -k 48 -k 49 -k 50 -k 51 -k 52 -k 53 -k 54 -k 55 -k 56 -k 57 -k 58 -k 59 -k 60 -k 61 -k 62 -k 63 -k 64 -k 65 -k 66 -k 67 -k 68 -k 69 -k 70 -k 71 -k 72 -k 73 -k 74 -k 75 -k 76 -k 77 -k 78 -k 79 -k 80 -k 81 -k 82 -k 83')
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'
	
	
def ctrl_pointer():
	mel.eval('curve -d 1 -p -1 0 0 -p 1 0 0 -p 1 1 0 -p 1 2 0 -p 1 3 0 -p 2 3 0 -p 0 5 0 -p -2 3 0 -p -1 3 0 -p -1 2 0 -p -1 1 0 -p -1 0 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11')
	ctrl = cmds.ls(sl=True)
	cmds.duplicate(rr=True)
	ctrl2 = cmds.ls(sl=True)
	cmds.setAttr(ctrl2[0] + '.rotateY', 90)
	print 'Curves have been positioned.'
	
	cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
	print 'Freezing transforms on curves.'
	
	cmds.select(ctrl, r=True)
	cmds.pickWalk(d='Down')
	cmds.select(ctrl2, add=True)
	cmds.parent(r=True, s=True)
	print 'Curves have been parented into single curve.'
	
	
	cmds.select(ctrl, r=True)
	mel.eval('doDelete')
	print 'Unsuded groups have been deleted.'
	
	cmds.select(ctrl2)
	mel.eval('CenterPivot')
	print 'Curve has been selected and its pivot has been centered.'







