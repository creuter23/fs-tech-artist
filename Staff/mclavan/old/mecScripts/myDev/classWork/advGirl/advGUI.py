'''
Adventure GUI Character GUI
by Michael Clavan
advGUI.py

Description:
	Contains the interface for adventure girl's character gui.
	
How to Run:
import advGUI
advGUI.gui()

'''

import maya.cmds as cmds
import os.path

def gui():
	'''
	Loads the main interface
	'''
	
	# Check to see if you are on osx or win
	
	os = cmds.about(os=True)
	if( os == "mac" ):
		# macGUI()
		winGUI()
	else:
		winGUI()
	
def winGUI():
	'''
	Loads the windows version of the character interface.
	'''
	win = "advGirlWin"
	if( cmds.window( win, ex=True ) ):
		cmds.deleteUI(win)
	if( cmds.windowPref( win, ex=True )):
		cmds.windowPref( win, remove=True)
		
	cmds.window( win, w=270, h=450 )
	mainForm = cmds.formLayout()
	charSel = winCharSelect(mainForm)

	cmds.showWindow(win)

def manipState(*args):
	localState = cmds.symbolCheckBox( selectBtn, q=True, value=True )
	# print("localState: %s" %localState)
	if( localState ):
		# Move tool in local mode
		cmds.manipMoveContext( "Move", e=1, mode=0 )
	else:
		# Move tool in world mode.
		cmds.manipMoveContext( "Move", e=1, mode=2 )

def controlSelect(obj, manip=None):
	
	selectMode = cmds.symbolCheckBox( localBtn, q=True, value=True)
	
	if( manip == "rot" ):
		# rotate tool
		cmds.RotateTool()
	elif( manip == "trans" ):
		# move tool
		cmds.MoveTool()
	
	if( selectMode ):
		cmds.select( obj, add=True )
	else:
		cmds.select( obj, r=True )


def winCharSelect(curParent):
	imgPath = lambda x: os.path.join( os.path.split(__file__)[0], "icons", x + ".xpm")
	frm = cmds.formLayout()
	
	# (lambda x : controlSelect("controlIcon", "rotTrans"))
	# Row 1
	global localBtn
	localBtn = cmds.symbolCheckBox(image=imgPath('advGirl_01_01_add'), w=85, h=70,
		onImage=imgPath('advGirl_01_01_add'),
		offImage=imgPath('advGirl_01_01_sub'))
	btn12 = cmds.symbolButton(image=imgPath('AdvGirl_01_02_ctrl'), w=16 , h=70,
			command=(lambda x : controlSelect("R_pigtail_end_anim", "trans")) )
	btn13 = cmds.symbolButton(image=imgPath('AdvGirl_01_03_ctrl'), w=59 , h=70,
		command=(lambda x : controlSelect("head_anim", "rot")) )
	btn14 = cmds.symbolButton(image=imgPath('AdvGirl_01_04_ctrl'), w=17 , h=70,
		command=(lambda x : controlSelect("L_pigtail_end_anim", "trans")) )
	global selectBtn
	selectBtn = cmds.symbolCheckBox(image=imgPath('advGirl_01_05_local'), w=85, h=70,
		onImage=imgPath('advGirl_01_05_local'),
		offImage=imgPath('advGirl_01_05_world'),
		cc=manipState)
	# Position
	cmds.formLayout( frm, e=1, af=[[localBtn, "top", 0],[localBtn, "left", 0]] )
	cmds.formLayout( frm, e=1, af=[btn12, "top", 0], ac=[btn12, "left", 0, localBtn] )
	cmds.formLayout( frm, e=1, af=[btn13, "top", 0], ac=[btn13, "left", 0, btn12] )
	cmds.formLayout( frm, e=1, af=[btn14, "top", 0], ac=[btn14, "left", 0, btn13] )
	cmds.formLayout( frm, e=1, af=[selectBtn, "top", 0], ac=[selectBtn, "left", 0, btn14] )
	
	
	# Row 2
	btn21 = cmds.symbolButton(image=imgPath('AdvGirl_02_01_ctrl'), w=43 , h=15,
			command=(lambda x : controlSelect("R_hand_anim")))
	btn22 = cmds.symbolButton(image=imgPath('AdvGirl_02_02_ctrl'), w=49 , h=15,
			command=(lambda x : controlSelect("R_elbow_pole_anim", "trans")))
	btn23 = cmds.symbolButton(image=imgPath('AdvGirl_02_03_ctrl'), w=36 , h=15,
			command=(lambda x : controlSelect("R_shoulder_anim", "trans")))
	btn24 = cmds.symbolButton(image=imgPath('AdvGirl_02_04_ctrl'), w=38 , h=15,
			command=(lambda x : controlSelect("L_shoulder_anim", "trans")))
	btn25 = cmds.symbolButton(image=imgPath('AdvGirl_02_05_ctrl'), w=51 , h=15,
			command=(lambda x : controlSelect("L_elbow_pole_anim", "trans")))
	btn26 = cmds.symbolButton(image=imgPath('AdvGirl_02_06_ctrl'), w=45 , h=15,
			command=(lambda x : controlSelect("L_hand_anim")))
	# Position
	cmds.formLayout( frm, e=1, af=[btn21, "left", 0], ac=[btn21, "top", 0, btn12] )
	cmds.formLayout( frm, e=1, ac=[[btn22, "left", 0, btn21],[btn22, "top", 0, btn12]] )
	cmds.formLayout( frm, e=1, ac=[[btn23, "left", 0, btn22],[btn23, "top", 0, btn12]] )
	cmds.formLayout( frm, e=1, ac=[[btn24, "left", 0, btn23],[btn24, "top", 0, btn12]] )
	cmds.formLayout( frm, e=1, ac=[[btn25, "left", 0, btn24],[btn25, "top", 0, btn12]] )
	cmds.formLayout( frm, e=1, ac=[[btn26, "left", 0, btn25],[btn26, "top", 0, btn12]] )
	#cmds.formLayout( frm, e=1, ac=[[btn27, "left", 0, btn26],[btn27, "top", 0, btn12]] )
	
	
	# Row 3
	btn31 = cmds.symbolButton(image=imgPath('AdvGirl_03_01_ctrl'), w=42 , h=14,
			command=(lambda x : controlSelect("R_hand_FK_anim", "rot")))
	btn32 = cmds.symbolButton(image=imgPath('AdvGirl_03_02_ctrl'), w=32 , h=14,
			command=(lambda x : controlSelect("R_elbow_FK_anim", "rot")))
	btn33 = cmds.symbolButton(image=imgPath('AdvGirl_03_03_ctrl'), w=39 , h=14,
			command=(lambda x : controlSelect("R_shoulder_fk_anim", "rot")))
	btn34 = cmds.symbolButton(image=imgPath('AdvGirl_03_04_ctrl'), w=30 , h=14,
			command=(lambda x : controlSelect("back_upper_rot_anim", "rot")))
	btn35 = cmds.symbolButton(image=imgPath('AdvGirl_03_05_ctrl'), w=45 , h=14,
			command=(lambda x : controlSelect("L_shoulder_fk_anim", "rot")))
	btn36 = cmds.symbolButton(image=imgPath('AdvGirl_03_06_ctrl'), w=28 , h=14,
			command=(lambda x : controlSelect("L_elbow_FK_anim", "rot")))
	btn37 = cmds.symbolButton(image=imgPath('AdvGirl_03_07_ctrl'), w=46 , h=14,
			command=(lambda x : controlSelect("L_hand_FK_anim", "rot")))
	# Position
	cmds.formLayout( frm, e=1, af=[btn31, "left", 0], ac=[btn31, "top", 0, btn21] )
	cmds.formLayout( frm, e=1, ac=[[btn32, "left", 0, btn31],[btn32, "top", 0, btn21]] )
	cmds.formLayout( frm, e=1, ac=[[btn33, "left", 0, btn32],[btn33, "top", 0, btn21]] )
	cmds.formLayout( frm, e=1, ac=[[btn34, "left", 0, btn33],[btn34, "top", 0, btn21]] )
	cmds.formLayout( frm, e=1, ac=[[btn35, "left", 0, btn34],[btn35, "top", 0, btn21]] )
	cmds.formLayout( frm, e=1, ac=[[btn36, "left", 0, btn35],[btn36, "top", 0, btn21]] )
	cmds.formLayout( frm, e=1, ac=[[btn37, "left", 0, btn36],[btn37, "top", 0, btn21]] )
	
	
	# Row 4
	btn41 = cmds.picture(image=imgPath('AdvGirl_04_01_img'), w=115 , h=14)
	btn42 = cmds.symbolButton(image=imgPath('AdvGirl_04_02_ctrl'), w=28 , h=14,
			command=(lambda x : controlSelect("back_mid_rot_anim", "rot")))
	btn43 = cmds.picture(image=imgPath('AdvGirl_04_03_img'), w=119 , h=14)
	# Position	
	cmds.formLayout( frm, e=1, af=[btn41, "left", 0], ac=[btn41, "top", 0, btn31] )
	cmds.formLayout( frm, e=1, ac=[[btn42, "left", 0, btn41],[btn42, "top", 0, btn31]] )
	cmds.formLayout( frm, e=1, ac=[[btn43, "left", 0, btn42],[btn43, "top", 0, btn31]] )
	
	# Row 5
	btn51 = cmds.picture(image=imgPath('AdvGirl_05_01_img'), w=54 , h=25)
	btn52 = cmds.symbolButton(image=imgPath('AdvGirl_05_02_ctrl'), w=45 , h=25,
			command=(lambda x : controlSelect("COG_anim", "rot")))
	# bnt53 = cmds.picture(image=imgPath('AdvGirl_05_03_ctrl'), w=17 , h=25)
	btn53 = cmds.symbolButton(image=imgPath('AdvGirl_05_03_ctrl'), w=61 , h=25,
			command=(lambda x : controlSelect("back_lower_rot_anim")))
	btn54 = cmds.symbolButton(image=imgPath('AdvGirl_05_04_ctrl'), w=56 , h=25,
			command=(lambda x : controlSelect("hips_anim")))
	btn55 = cmds.picture(image=imgPath('AdvGirl_05_05_img'), w=46 , h=25)

# COG
# select -r COG_anim ;

	# Position
	cmds.formLayout( frm, e=1, af=[btn51, "left", 0], ac=[btn51, "top", 0, btn41] )
	cmds.formLayout( frm, e=1, ac=[[btn52, "left", 0, btn51],[btn52, "top", 0, btn41]] )
	cmds.formLayout( frm, e=1, ac=[[btn53, "left", 0, btn52],[btn53, "top", 0, btn41]] )
	cmds.formLayout( frm, e=1, ac=[[btn54, "left", 0, btn53],[btn54, "top", 0, btn41]] )
	cmds.formLayout( frm, e=1, ac=[[btn55, "left", 0, btn54],[btn55, "top", 0, btn41]] )
	
	# Row 6
	btn61 = cmds.picture( image=imgPath('AdvGirl_06_01_img'), w=262 , h=48 )
	cmds.formLayout( frm, e=1, af=[btn61, "left", 0], ac=[btn61, "top", 0, btn51] )
	
	
	# Row 7
	btn71 = cmds.picture(image=imgPath('AdvGirl_07_01_img'), w=103 , h=22)
	btn72 = cmds.symbolButton(image=imgPath('AdvGirl_07_02_ctrl'), w=25 , h=22,
			command=(lambda x : controlSelect("R_knee_pole_anim", "trans")))
	btn73 = cmds.symbolButton(image=imgPath('AdvGirl_07_03_ctrl'), w=25 , h=22,
			command=(lambda x : controlSelect("L_knee_pole_anim", "trans")))
	btn74 = cmds.picture(image=imgPath('AdvGirl_07_04_img'), w=109 , h=22)
	# Position
	cmds.formLayout( frm, e=1, af=[btn71, "left", 0], ac=[btn71, "top", 0, btn61] )
	cmds.formLayout( frm, e=1, ac=[[btn72, "left", 0, btn71],[btn72, "top", 0, btn61]] )
	cmds.formLayout( frm, e=1, ac=[[btn73, "left", 0, btn72],[btn73, "top", 0, btn61]] )
	cmds.formLayout( frm, e=1, ac=[[btn74, "left", 0, btn73],[btn74, "top", 0, btn61]] )
	
	# Row 8
	btn81 = cmds.picture( image=imgPath('AdvGirl_08_01_img'), w=262 , h=36 )
	cmds.formLayout( frm, e=1, af=[btn81, "left", 0], ac=[btn81, "top", 0, btn71] )
	
	# Row 9
	btn91 = cmds.picture(image=imgPath('AdvGirl_09_01_img'), w=93 , h=33)
	btn92 = cmds.symbolButton(image=imgPath('AdvGirl_09_02_ctrl'), w=35 , h=33,
			command=(lambda x : controlSelect("R_foot_anim", "trans")))
	btn93 = cmds.symbolButton(image=imgPath('AdvGirl_09_03_ctrl'), w=38 , h=33,
			command=(lambda x : controlSelect("L_foot_anim", "trans")))
	btn94 = cmds.picture(image=imgPath('AdvGirl_09_04_img'), w=96 , h=33)
	# Position
	cmds.formLayout( frm, e=1, af=[btn91, "left", 0], ac=[btn91, "top", 0, btn81] )
	cmds.formLayout( frm, e=1, ac=[[btn92, "left", 0, btn91],[btn92, "top", 0, btn81]] )
	cmds.formLayout( frm, e=1, ac=[[btn93, "left", 0, btn92],[btn93, "top", 0, btn81]] )
	cmds.formLayout( frm, e=1, ac=[[btn94, "left", 0, btn93],[btn94, "top", 0, btn81]] )	

	cmds.setParent(curParent)
	return frm
	
def macGUI():
	'''
	Loads the osx version of the interface.
	Symbol button icons will contain borders.
	'''
	macWin()
	'''
	win = "advGirlWin"
	if( cmds.window( win, ex=True ) ):
		cmds.deleteUI(win)
	if( cmds.windowPref( win, ex=True )):
		cmds.windowPref( win, remove=True)
		
	cmds.window( win, w=300, h=300 )
	mainForm = cmds.formLayout()
	charSel = osxCharSelect()

	cmds.showWindow(win)
	'''
def osxCharSelect():
	imgPath = lambda x: os.path.join( os.path.split(__file__)[0], "icons", x )



