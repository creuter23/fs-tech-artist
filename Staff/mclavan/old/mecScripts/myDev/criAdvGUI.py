'''
Adventure Girl Rig Interface
criAdvGUI.py

Description:
	
How To Run:
	
import criAdvGUI
criAdvGUI.gui()

'''

import maya.cmds as cmds
scriptName = __name__

def gui():
	'''
	Generates the interface for adventure girl.
	'''
	win = "criAdvGUIWin"

	if( cmds.window(win, q=True, ex=True)):
		cmds.deleteUI(win)
		
	cmds.window(win, title="Adventure Girl Rig Interface", w=300, h=300)
	cmds.columnLayout("criAdvGUIMC")
	
	# Generate the character Selection area
	tabLayout = cmds.tabLayout()
	tab1 = cmds.columnLayout("criCharLayout")
	charSel()
	cmds.setParent(tabLayout)
	
	tab2 = cmds.columnLayout()
	switches()
	cmds.setParent(tabLayout)
	
	# tab3 = cmds.columnLayout()
	camWindow()
	cmds.setParent("criAdvGUIMC")
	cmds.showWindow(win)	
	
def switches():
	# IK FK Switches
	ltIKFK = cmds.floatSliderGrp( label="Left IKFK", field=True, min=0, max=10, step=.1 )
	rtIKFK = cmds.floatSliderGrp( label="Left IKFK", field=True, min=0, max=10, step=.1 )
	cmds.connectControl( ltIKFK, "lt_hand_controls.IK_FK_Switch" )
	cmds.connectControl( rtIKFK, "rt_hand_controls.IK_FK_Switch" )
	
	# Face Shapes
	rtPuff = cmds.floatSliderGrp( label='Right Puff', field=True, min=0, max=2, step=.1 )
	cmds.connectControl(rtPuff , "mouth_control_group|control_slider_curves|puff_marker_r_curve.translateX" )
	# cmds.attrFieldSliderGrp(at="mouth_control_group|control_slider_curves|puff_marker_r_curve.translateX")

def camWindow():
	faceCam = cmds.modelEditor(   )
	cmds.modelEditor( faceCam, edit=True, camera="camera1")
	
def charSel():
	'''
	This is the character selection gui for adventure girl.
	'''
	
	# ColumnLayout Name
	# string $mainCol = "criAdvGUIMC"
	# mainCol = "criAdvGUIMC"
	mainCol = "criCharLayout"
	# Full Image 374x395
	# Seperate into rows. 9 Rows
	
	# Row 1
	# h=100
	cmds.rowColumnLayout( nc=5, cw=[[1,122],[2,21],[3,86],[4,23],[5,122]] )
	# AdvGirl_01_01.xpm
	cmds.picture( image="AdvGirl_01_01.xpm", w=122, h=100 )
	cmds.symbolButton( image="AdvGirl_01_02.xpm", w=21, h=100, 
		command=scriptName + ".selectCtrl( 'head_control' )" )
	cmds.symbolButton( image="AdvGirl_01_03.xpm", w=86, h=100, 
		command=scriptName + ".selectCtrl( 'head_control' )")
	cmds.symbolButton( image="AdvGirl_01_04.xpm", w=23, h=100, 
		command=scriptName + ".selectCtrl( 'head_control' )" )
	cmds.picture( image="AdvGirl_01_05.xpm", w=122, h=100 )
	cmds.setParent(mainCol)
	# Row 2
	# h=20
	cmds.rowColumnLayout( nc=6, cw=[[1,62],[2,70],[3,52],[4,53],[5,73], [6,64]] )
	cmds.symbolButton( image="AdvGirl_02_01.xpm", w=62 ,h=20, 
		command=scriptName + ".selectCtrl( 'rt_hand_IK_control' )" )
	cmds.symbolButton( image="AdvGirl_02_02.xpm", w=70 ,h=20, 
		command=scriptName + ".selectCtrl( 'rt_elbow_control' )" )
	cmds.symbolButton( image="AdvGirl_02_03.xpm", w=52 ,h=20, 
		command=scriptName + ".selectCtrl( 'shoulder_control' )" )
	cmds.symbolButton( image="AdvGirl_02_04.xpm", w=53 ,h=20, 
		command=scriptName + ".selectCtrl( 'shoulder_control' )" )
	cmds.symbolButton( image="AdvGirl_02_05.xpm", w=73,h=20, 
		command=scriptName + ".selectCtrl( 'lt_elbow_control' )" )	
	cmds.symbolButton( image="AdvGirl_02_06.xpm", w=64 ,h=20, 
		command=scriptName + ".selectCtrl( 'lt_hand_IK_control' )" )	
	cmds.setParent(mainCol)

	# Row 3
	# h=22
	cmds.rowColumnLayout( nc=7, cw=[[1,60],[2,46],[3,56],[4,43],[5,64],[6,40],[7,65]] )
	cmds.symbolButton( image="AdvGirl_03_01.xpm", w=60 ,h=20, 
		command=scriptName + ".selectCtrl( 'rt_wrist_control_fk' )" )
	cmds.symbolButton( image="AdvGirl_03_02.xpm", w=46 ,h=20, 
		command=scriptName + ".selectCtrl( 'rt_elbow_control_fk' )" )
	cmds.symbolButton( image="AdvGirl_03_03.xpm", w=56 ,h=20, 
		command=scriptName + ".selectCtrl( 'rt_upperArm_control_fk' )" )
	cmds.symbolButton( image="AdvGirl_03_04.xpm", w=43 ,h=20, 
		command=scriptName + ".selectCtrl( 'ct_spine_1_control_fk' )" )
	cmds.symbolButton( image="AdvGirl_03_05.xpm", w=64 ,h=20, 
		command=scriptName + ".selectCtrl( 'lt_upperArm_control_fk' )" )	
	cmds.symbolButton( image="AdvGirl_03_06.xpm", w=40 ,h=20, 
		command=scriptName + ".selectCtrl( 'lt_elbow_control_fk' )" )
	cmds.symbolButton( image="AdvGirl_03_07.xpm", w=65 ,h=20, 
		command=scriptName + ".selectCtrl( 'lt_wrist_control_fk' )" )
	cmds.setParent(mainCol)
	
	# Row 4
	# h=20
	cmds.rowColumnLayout( nc=3, cw=[[1,163],[2,42],[3,169]] )
	cmds.picture( image="AdvGirl_04_01.xpm" )
	cmds.symbolButton( image="AdvGirl_04_02.xpm", w=163, h=20, 
		command=scriptName + ".selectCtrl( 'ct_spine_3_control_fk' )" )
	cmds.picture( image="AdvGirl_04_03.xpm" )	
	cmds.setParent(mainCol)

	# Row 5
	# h=34
	cmds.rowColumnLayout( nc=3, cw=[[1,142],[2,85],[3,147]] )
	cmds.picture( image="AdvGirl_05_01.xpm" )
	cmds.symbolButton( image="AdvGirl_05_02.xpm", w=85, h=34, 
		command=scriptName + ".selectCtrl( 'COG_control' )" )
	cmds.picture( image="AdvGirl_05_03.xpm" )
	cmds.setParent(mainCol)
	
	# Row 6 is only one doesn't need a rowcolumn
	# 374 x 68
	cmds.picture( image="AdvGirl_06_01.xpm" )
	
	# Row 7
	# h=32
	cmds.rowColumnLayout( nc=4, cw=[[1,148],[2,36],[3,34],[4,156]] )
	cmds.picture( image="AdvGirl_07_01.xpm" )
	cmds.symbolButton( image="AdvGirl_07_02.xpm", w=36, h=32, 
		command=scriptName + ".selectCtrl( 'rt_knee_control' )" )
	cmds.symbolButton( image="AdvGirl_07_03.xpm", w=34, h=32, 
		command=scriptName + ".selectCtrl( 'lt_knee_control' )" )
	cmds.picture( image="AdvGirl_07_04.xpm" )
	cmds.setParent(mainCol)
	
	# Row 8 is only one doesn't need a rowcolumn
	# 374 x 51
	cmds.picture( image="AdvGirl_08_01.xpm" )
	
	# Row 9
	# h=48
	cmds.rowColumnLayout( nc=4, cw=[[1,132],[2,52],[3,53],[4,137]] )
	cmds.picture( image="AdvGirl_09_01.xpm" )
	cmds.symbolButton( image="AdvGirl_09_02.xpm", w=52, h=48, 
		command=scriptName + ".selectCtrl( 'rt_foot_control' )" )
	cmds.symbolButton( image="AdvGirl_09_03.xpm", w=53, h=48, 
		command=scriptName + ".selectCtrl( 'lt_foot_control' )" )
	cmds.picture( image="AdvGirl_09_04.xpm" )	
	cmds.setParent(mainCol)
	
def selectCtrl( ctrl ):
	'''
	Select given control while removing every thing else.
	'''
	cmds.select( ctrl, r=True)
	print(ctrl + " has been selected.")
	
