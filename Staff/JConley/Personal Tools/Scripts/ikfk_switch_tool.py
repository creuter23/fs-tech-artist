"""Rename Tool"""

"""
Author: Jennifer Conley
Date Modified: 8/29/11

Description: A script to quickly set up an ik/fk switch inside of Maya.

How to run:
import ikfk_switch_tool
reload (ikfk_switch_tool)
ikfk_switch_tool.gui()

"""

import maya.cmds as cmds
import maya.mel as mel

win = 'rename_win'
scriptname = __name__
width = 200


"""
Creates the window for the ikfk switch tool
"""
def gui():
	if (cmds.window(win, q=True, ex=True)):
		cmds.deleteUI(win)
		
	cmds.window(win, t='Rename Tool', w=width, h=300)
	
	global ik_ctrl, pv_ctrl, fk_root, fk_mid, sys_type, other, switch
	
	main_layout = cmds.columnLayout(w=width, nch=2)
	cmds.separator(style='single', w=width, h=5)
	cmds.text(l='Ik System', w=width)
	cmds.separator(style='single', w=width, h=5)
	
	cmds.rowColumnLayout(w=width, nc=2)
	cmds.text(l='Ik Ctrl:')
	ik_ctrl = cmds.textField(tx='curve1')
	
	cmds.text(l='Pv Ctrl:')
	pv_ctrl = cmds.textField(tx='curve3')
	cmds.setParent(main_layout)
	
	cmds.separator(style='single', w=width, h=5)
	cmds.text(l='Fk System', w=width)
	cmds.separator(style='single', w=width, h=5)
	
	cmds.rowColumnLayout(w=width, nc=2)	
	cmds.text(l='Fk Root Ctrl:')
	fk_root = cmds.textField(tx='nurbsCircle1')
	
	cmds.text(l='Fk Mid Ctrl:')
	fk_mid = cmds.textField(tx='nurbsCircle2')
	cmds.setParent(main_layout)
	
	cmds.separator(style='single', w=width, h=5)
	cmds.text(l='Ik Fk Switch', w=width)
	cmds.separator(style='single', w=width, h=5)
	sys_type = cmds.radioButtonGrp(nrb=3, 
		cw3=[(width/3), (width/3),(width/3)],
		la3=('Arm', 'Leg', 'Other'), sl=1)
	
	cmds.rowColumnLayout(w=width, nc=2)
	cmds.text(l='Other:')
	other = cmds.textField()
	
	cmds.text(l='Ik Fk Switch Ctrl:')
	switch = cmds.textField(tx='curve2')
	cmds.setParent(main_layout)
	
	cmds.button(l='Create Switch', w=width, c=scriptname + '.ikfk_switch()')
	
	print 'Gui created.'
	
	
	cmds.showWindow()
	
def ikfk_switch():
	"""
	Creates the fuction which will create the ikfk swtich.
	"""
	root_joint = cmds.ls(sl=True)
	
	ik = cmds.textField(ik_ctrl, q=True, tx=True)
	pv = cmds.textField(pv_ctrl, q=True, tx=True)
	fk_r = cmds.textField(fk_root, q=True, tx=True)
	fk_m = cmds.textField(fk_mid, q=True, tx=True)
	sys = cmds.radioButtonGrp(sys_type, q=True, sl=True)
	oth = cmds.textField(other, q=True, tx=True)
	ikfk_switch = cmds.textField(switch, q=True, tx=True)
	
	print 'Data stored'
	
	if sys == 1:
		cmds.select(root_joint)
		mel.eval('SelectHierarchy')
		bind_chain = cmds.ls(sl=True)
		
		cmds.duplicate(bind_chain)
		mel.eval('searchReplaceNames "arm" "arm_ik" "selected"')
		ik_chain = cmds.ls(sl=True)
		cmds.select(cl=True)
		
		cmds.select(bind_chain)
		cmds.duplicate(bind_chain)
		mel.eval('searchReplaceNames "arm" "arm_fk" "selected"')
		fk_chain = cmds.ls(sl=True)
		
		name = 'arm'
		
		print 'Joints duplicated and named'
	
	elif sys == 2:
		cmds.select(root_joint)
		mel.eval('SelectHierarchy')
		bind_chain = cmds.ls(sl=True)
		
		cmds.duplicate(bind_chain)
		mel.eval('searchReplaceNames "leg" "leg_ik" "selected"')
		ik_chain = cmds.ls(sl=True)
		cmds.select(cl=True)
		
		cmds.select(bind_chain)
		cmds.duplicate(bind_chain)
		mel.eval('searchReplaceNames "leg" "leg_fk" "selected"')
		fk_chain = cmds.ls(sl=True)
		
		name = 'leg'
		
		print 'Joints duplicated and named'
		
	elif sys == 3:
		"""
		searchReplaceNames currently not renaming
		"""
		
		cmds.select(root_joint)
		mel.eval('SelectHierarchy')
		bind_chain = cmds.ls(sl=True)
		
		cmds.duplicate(bind_chain)
		oth_ik = oth + '_ik'
		mel.eval('searchReplaceNames oth oth_ik "selected"')
		ik_chain = cmds.ls(sl=True)
		cmds.select(cl=True)
		
		
		cmds.select(bind_chain)
		cmds.duplicate(bind_chain)
		oth_fk = oth + '_fk'
		mel.eval('searchReplaceNames oth oth_fk "selected"')
		fk_chain = cmds.ls(sl=True)
		
		name = oth
		
		print 'Joints duplicated and named'
		
		
	"""
	Creates the Ik System.
	"""
	ik_end = len(ik_chain) - 1
	cmds.select(ik_chain[0] + '.rotatePivot')
	cmds.select((ik_chain[ik_end] + '.rotatePivot'), add=True)
	cmds.ikHandle(sol='ikRPsolver', s='sticky')
	rn_ik = cmds.select('ikHandle1')
	new_ik = cmds.rename(rn_ik, (name + '_ikHandle_01'))
	cmds.select(cl=True)
	
	print 'Ik handle created.'
	
	
	"""
	Creates the constraints for the Ik System based on ctrls specified
	"""
	cmds.select(ik, r=True)
	cmds.select(new_ik, add=True)
	cmds.parentConstraint(mo=True, weight=1)
	cmds.select(cl=True)
	
	cmds.select(pv, r=True)
	cmds.select(new_ik, add=True)
	cmds.poleVectorConstraint(weight=1)
	cmds.select(cl=True)
	
	print 'Parent constraint and pole vector constraint created.'
	
	
	"""
	Creats the constraints for the Fk System based on ctrls specified
	"""
	cmds.select(fk_r, r=True)
	cmds.select(fk_chain[0], add=True)
	cmds.orientConstraint(mo=True, weight=1)
	cmds.select(cl=True)

	cmds.select(fk_m, r=True)
	cmds.select(fk_chain[1], add=True)
	cmds.orientConstraint(mo=True, weight=1)
	cmds.select(cl=True)
	
	print 'Fk system created.'
	
	"""
	Parent constrains the bind joints between the ik and fk chains.
	"""
	i=0
	bind_list = []
	for each in bind_chain:
		cmds.select(ik_chain[i], r=True)
		cmds.select(fk_chain[i], add=True)
		cmds.select(bind_chain[i], add=True)
		cmds.parentConstraint(mo=True, weight=1)
		pc_name = bind_chain[i] + '_parentConstraint1'
		bind_list.append(pc_name)
		i += 1
		
	print 'Bind joints constrained between ik and fk joint chains.'
	
	"""
	Creates the set driven key for the ik system.
	"""
	x=0
	switch_attr = ikfk_switch + '.Ik_Fk_Switch'
	cmds.setAttr(switch_attr, 0)
	
	for each1 in bind_list:
		ik_weight1 = each1 + '.' + ik_chain[x] + 'W0'
		fk_weight1 = each1 + '.' + fk_chain[x] + 'W1'
		
		cmds.setAttr(ik_weight1, 1)
		cmds.setAttr(fk_weight1, 0)
		
		cmds.setDrivenKeyframe(ik_weight1, cd=switch_attr)
		cmds.setDrivenKeyframe(fk_weight1, cd=switch_attr)
		x += 1
		
	print 'Bind chain constraints set and keyed for ik.'
	
	
	"""
	Creates the set driven key for the fk system.
	"""	
	j=0
	cmds.setAttr(switch_attr, 10)
	
	for each2 in bind_list:
		ik_weight2 = each2 + '.' + ik_chain[j] + 'W0'
		fk_weight2 = each2 + '.' + fk_chain[j] + 'W1'
		
		cmds.setAttr(ik_weight2, 0)
		cmds.setAttr(fk_weight2, 1)

		cmds.setDrivenKeyframe(ik_weight2, cd=switch_attr)
		cmds.setDrivenKeyframe(fk_weight2, cd=switch_attr)
		j += 1
		
	print 'Bind chain constraints set and keyed for fk.'
	
	cmds.setAttr(switch_attr, 0)
	
	print 'Ik fk switch created and set to the defualt setting of ik.'
	
	
		

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
