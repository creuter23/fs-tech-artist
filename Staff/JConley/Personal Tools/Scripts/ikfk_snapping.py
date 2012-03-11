"""Ik Fk Snapping Tool"""

"""
Author: Jennifer Conley
Date Modified: 10/18/11

Description: Snaps the Ik and Fk joint chains together based on user selection

How to run:
1) - Copy the script into your scripts folder
2) - Run the following code in the Script Editor of Maya

import ikfk_snapping
reload (ikfk_snapping)
ikfk_snapping.gui()

"""



import maya.cmds as cmds

win = 'Ik_Fk_Win'
width = 150
hight = 80

def gui():
	
	global selection
	
	if (cmds.window(win, q=True, ex=True)):
		cmds.deleteUI(win)
		
	cmds.window(win, w=width, h=hight)
	cmds.columnLayout()
	cmds.text(l='Ik Fk Snapping', w=width)
	cmds.separator(w=width, h=5)
	selection = cmds.radioButtonGrp(nrb = 2, la2=('Ik to Fk', 'Fk to Ik'),
		cw2=[(width/2), (width/2)])
	cmds.button(l='Run', w=width, c=snap)
	cmds.showWindow(win)

def snap(*args):
	sel = cmds.radioButtonGrp(selection, q=True, sl=True)
	
	if sel == 1:
		
		"""Right Arm - Matching IK to FK"""
		#Get FK Shoulder locator Translations
		r_elbow_loc_tx = cmds.getAttr('rt_elbow_loc_01.tx')
		r_elbow_loc_ty = cmds.getAttr('rt_elbow_loc_01.ty')
		r_elbow_loc_tz = cmds.getAttr('rt_elbow_loc_01.tz')
		
		#Get FK Wrist locator Translatons
		r_wrist_loc_tx = cmds.getAttr('rt_wrist_loc_01.tx')
		r_wrist_loc_ty = cmds.getAttr('rt_wrist_loc_01.ty')
		r_wrist_loc_tz = cmds.getAttr('rt_wrist_loc_01.tz')
		
		#Get FK Wrist Locator Rotations
		r_wrist_loc_rx = cmds.getAttr('rt_wrist_loc_01.rx')
		r_wrist_loc_ry = cmds.getAttr('rt_wrist_loc_01.ry')
		r_wrist_loc_rz = cmds.getAttr('rt_wrist_loc_01.rz')
		
		#Set IK Translations and Rotations
		cmds.setAttr('rt_elbow_pv_ctrl_01.tx', r_elbow_loc_tx)
		cmds.setAttr('rt_elbow_pv_ctrl_01.ty', r_elbow_loc_ty)
		cmds.setAttr('rt_elbow_pv_ctrl_01.tz', r_elbow_loc_tz)
		
		cmds.setAttr('rt_hand_ik_ctrl_01.tx', r_wrist_loc_tx)
		cmds.setAttr('rt_hand_ik_ctrl_01.ty', r_wrist_loc_ty)
		cmds.setAttr('rt_hand_ik_ctrl_01.tz', r_wrist_loc_tz)
		
		cmds.setAttr('rt_hand_ik_ctrl_01.rx', r_wrist_loc_rx)
		cmds.setAttr('rt_hand_ik_ctrl_01.ry', r_wrist_loc_ry)
		cmds.setAttr('rt_hand_ik_ctrl_01.rz', r_wrist_loc_rz)
		
		
		"""Left Arm - Matching IK to FK"""
		#Get FK Shoulder locator Translations
		l_elbow_loc_tx = cmds.getAttr('lf_elbow_loc_01.tx')
		l_elbow_loc_ty = cmds.getAttr('lf_elbow_loc_01.ty')
		l_elbow_loc_tz = cmds.getAttr('lf_elbow_loc_01.tz')
		
		#Get FK Wrist locator Translatons
		l_wrist_loc_tx = cmds.getAttr('lf_wrist_loc_01.tx')
		l_wrist_loc_ty = cmds.getAttr('lf_wrist_loc_01.ty')
		l_wrist_loc_tz = cmds.getAttr('lf_wrist_loc_01.tz')
		
		#Get FK Wrist Locator Rotations
		l_wrist_loc_rx = cmds.getAttr('lf_wrist_loc_01.rx')
		l_wrist_loc_ry = cmds.getAttr('lf_wrist_loc_01.ry')
		l_wrist_loc_rz = cmds.getAttr('lf_wrist_loc_01.rz')
		
		#Set IK Translations
		cmds.setAttr('lf_elbow_pv_ctrl_01.tx', l_elbow_loc_tx)
		cmds.setAttr('lf_elbow_pv_ctrl_01.ty', l_elbow_loc_ty)
		cmds.setAttr('lf_elbow_pv_ctrl_01.tz', l_elbow_loc_tz)
		
		cmds.setAttr('lf_hand_ik_ctrl_01.tx', l_wrist_loc_tx)
		cmds.setAttr('lf_hand_ik_ctrl_01.ty', l_wrist_loc_ty)
		cmds.setAttr('lf_hand_ik_ctrl_01.tz', l_wrist_loc_tz)
		
		cmds.setAttr('lf_hand_ik_ctrl_01.rx', l_wrist_loc_rx)
		cmds.setAttr('lf_hand_ik_ctrl_01.ry', l_wrist_loc_ry)
		cmds.setAttr('lf_hand_ik_ctrl_01.rz', l_wrist_loc_rz)
		
	elif sel == 2:
		
		"""Right Arm - Matching FK to IK"""
		#Get IK Shoulder Rotations
		r_ik_arm1_rx = cmds.getAttr('rt_arm_ik_01.rx')
		r_ik_arm1_ry = cmds.getAttr('rt_arm_ik_01.ry')
		r_ik_arm1_rz = cmds.getAttr('rt_arm_ik_01.rz')
		
		#Get IK Elbow Rotation
		r_ik_arm2_rx = cmds.getAttr('rt_arm_ik_02.rx')
		r_ik_arm2_ry = cmds.getAttr('rt_arm_ik_02.ry')
		r_ik_arm2_rz = cmds.getAttr('rt_arm_ik_02.rz')
		
		#Get Ik Wrist Rotation
		r_ik_arm3_rx = cmds.getAttr('rt_arm_ik_03.rx')
		r_ik_arm3_ry = cmds.getAttr('rt_arm_ik_03.ry')
		r_ik_arm3_rz = cmds.getAttr('rt_arm_ik_03.rz')
		
		#Set FK Rotations
		cmds.setAttr('rt_arm_fk_01.rx', r_ik_arm1_rx)
		cmds.setAttr('rt_arm_fk_01.ry', r_ik_arm1_ry)
		cmds.setAttr('rt_arm_fk_01.rz', r_ik_arm1_rz)

		cmds.setAttr('rt_arm_fk_02.rx', r_ik_arm2_rx)
		cmds.setAttr('rt_arm_fk_02.ry', r_ik_arm2_ry)
		cmds.setAttr('rt_arm_fk_02.rz', r_ik_arm2_rz)
		
		cmds.setAttr('rt_arm_fk_03.rx', r_ik_arm3_rx)
		cmds.setAttr('rt_arm_fk_03.ry', r_ik_arm3_ry)
		cmds.setAttr('rt_arm_fk_03.rz', r_ik_arm3_rz)


		"""Left Arm - Matching FK to IK"""
		#Get IK Shoulder Rotations
		l_ik_arm1_rx = cmds.getAttr('lf_arm_ik_01.rx')
		l_ik_arm1_ry = cmds.getAttr('lf_arm_ik_01.ry')
		l_ik_arm1_rz = cmds.getAttr('lf_arm_ik_01.rz')
		
		#Get IK Elbow Rotation
		l_ik_arm2_rx = cmds.getAttr('lf_arm_ik_02.rx')
		l_ik_arm2_ry = cmds.getAttr('lf_arm_ik_02.ry')
		l_ik_arm2_rz = cmds.getAttr('lf_arm_ik_02.rz')
		
		#Get Ik Wrist Rotation
		l_ik_arm3_rx = cmds.getAttr('lf_arm_ik_03.rx')
		l_ik_arm3_ry = cmds.getAttr('lf_arm_ik_03.ry')
		l_ik_arm3_rz = cmds.getAttr('lf_arm_ik_03.rz')

		
		#Set FK Rotations
		cmds.setAttr('lf_arm_fk_01.rx', l_ik_arm1_rx)
		cmds.setAttr('lf_arm_fk_01.ry', l_ik_arm1_ry)
		cmds.setAttr('lf_arm_fk_01.rz', l_ik_arm1_rz)
		
		cmds.setAttr('lf_arm_fk_02.rx', l_ik_arm2_rx)
		cmds.setAttr('lf_arm_fk_02.ry', l_ik_arm2_ry)
		cmds.setAttr('lf_arm_fk_02.rz', l_ik_arm2_rz)

		cmds.setAttr('lf_arm_fk_03.rx', l_ik_arm3_rx)
		cmds.setAttr('lf_arm_fk_03.ry', l_ik_arm3_ry)
		cmds.setAttr('lf_arm_fk_03.rz', l_ik_arm3_rz)
		



