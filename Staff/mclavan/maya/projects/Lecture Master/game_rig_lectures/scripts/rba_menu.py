'''
RBA Lecture Menu's
rba_menu.py

Description:
    - Triggers different scenes to guide the students through the lecture
    
How to Run:
import rba_menu
reload(rba_menu)
rba_menu.exe_menus()
'''

import os.path
import sys
import maya.cmds as cmds
import maya.mel as mel

mel.eval( 'python("import sys")' )


class Callback():
	_callData = None
	def __init__(self,func,*args,**kwargs):
		self.func = func
		self.args = args
		self.kwargs = kwargs
	
	def __call__(self, *args):
		Callback._callData = (self.func, self.args, self.kwargs)
		mel.eval('global proc py_%s(){python("sys.modules[\'%s\'].Callback._doCall()");}'%(self.func.__name__, __name__))
		try:
			mel.eval('py_%s()'%self.func.__name__)
		except RuntimeError:
			pass
		
		if isinstance(Callback._callData, Exception):
			raise Callback._callData
		return Callback._callData 
	
	@staticmethod
	def _doCall():
		(func, args, kwargs) = Callback._callData
		Callback._callData = func(*args, **kwargs)

def exe_menus():
    '''
    Creates the menu's for RBA's Lectures
    '''
    scene_path = cmds.file(q=True, sn=True)
    base_path = os.path.split(scene_path)[0]
    lect5_path = os.path.join(base_path, 'scenes', 'lecture5')
    lect6_path = os.path.join(base_path, 'scenes', 'lecture6')
    print 'Lecture 5: %s\nLecture 6: %s' % (lect5_path, lect6_path)
    maya_menu = mel.eval('string $mainWin_mec = $gMainWindow')
    global rba_menu
    rba_menu = cmds.menu(label='RBA_Menu', p=maya_menu)
    
    
    lect5 = cmds.menuItem(label='Lecture 5', ann='Joints and Controls', sm=True, p=rba_menu)
    joints = cmds.menuItem(label='Joints', ann='Part 1 - Joints', sm=True, p=lect5)
    cmds.menuItem(label='01 - Body',  ann='Joints and Orientation', p=joints, c=Callback(open_scene, os.path.join(lect5_path, 'body.ma')))
    cmds.menuItem(label='02 - Leg',  ann='Joints and Orientation', p=joints, c=Callback(open_scene, os.path.join(lect5_path, 'leg.ma')))
    cmds.menuItem(label='03 - Arm',  ann='Joints and Orientation', p=joints, c=Callback(open_scene, os.path.join(lect5_path, 'arm.ma')))
    cmds.menuItem(label='04 - Hand',  ann='Joints and Orientation', p=joints, c=Callback(open_scene, os.path.join(lect5_path, 'hand.ma')))
    cmds.menuItem(label='05 - Head',  ann='Joints and Orientation', p=joints, c=Callback(open_scene, os.path.join(lect5_path, 'head.ma')))
    cmds.menuItem(label='06 - Full Body',  ann='Joints and Orientation', p=joints, c=Callback(open_scene, os.path.join(lect5_path, 'full.ma')))

    '''
    lect5_conn = cmds.menuItem(label='Connections', ann='Part 1 - Joints', sm=True, p=lect5)
    cmds.menuItem(label='01 - Control Icons',  ann='Joints and Orientation', p=lect5_conn, c=Callback(open_scene, os.path.join(lect5_path, 'body.ma')))
    cmds.menuItem(label='02 - Body',  ann='Joints and Orientation', p=lect5_conn, c=Callback(open_scene, os.path.join(lect5_path, 'leg.ma')))
    cmds.menuItem(label='03 - Arm',  ann='Joints and Orientation', p=lect5_conn, c=Callback(open_scene, os.path.join(lect5_path, 'arm.ma')))
    cmds.menuItem(label='04 - Leg',  ann='Joints and Orientation', p=lect5_conn, c=Callback(open_scene, os.path.join(lect5_path, 'head.ma')))
    cmds.menuItem(label='05 - Head',  ann='Joints and Orientation', p=lect5_conn, c=Callback(open_scene, os.path.join(lect5_path, '.ma')))
    '''
    
    # Lecture 6 Menu
    lect6 = cmds.menuItem(label='Lecture 6', ann='Complex Systems and Binding', sm=True, p=rba_menu)
    cmds.menuItem(label='01 - Body',  ann='Warmup', p=lect6, c=Callback(open_scene, os.path.join(lect6_path, '01_body_warmup.ma')))
    print 'Warm up Path: %s' % os.path.join(lect6_path, '01_body_warmup.ma')
    
    complex_menu = cmds.menuItem(label='Complex Systems', ann='Part 1 - Complex Systems', sm=True, p=lect6)
    cmds.menuItem(label='01 - Body & Shoulders',  ann='Body Shoulders', p=complex_menu, c=Callback(open_scene, os.path.join(lect6_path, '02_body_shoulders.ma')))
    cmds.menuItem(label='02 - SDK',  ann='SDK', p=complex_menu, c=Callback(open_scene, os.path.join(lect6_path, '03_sdk.ma')))
    cmds.menuItem(label='03 - Head',  ann='Head - SDK ', p=complex_menu, c=Callback(open_scene, os.path.join(lect6_path, '04_head_controls.ma')))
    cmds.menuItem(label='04 - Hand',  ann='Hand System - SDK', p=complex_menu, c=Callback(open_scene, os.path.join(lect6_path, '05_hand.ma')))
    cmds.menuItem(label='05 - Leg',  ann='Leg - RFL', p=complex_menu, c=Callback(open_scene, os.path.join(lect6_path, '06_leg_rfl.ma')))

    
    binding_menu = cmds.menuItem(label='Binding', ann='Part 2 - Binding', sm=True, p=lect6)
    cmds.menuItem(label='01 - Settings',  ann='Binding Settings', p=binding_menu, c=Callback(open_scene, os.path.join(lect6_path, '07_BindingSettings.ma')))
    cmds.menuItem(label='02 - Face',  ann='Binding Face', p=binding_menu, c=Callback(open_scene, os.path.join(lect6_path, '08_face.ma')))
    cmds.menuItem(label='03 - Hand',  ann='Binding Hand', p=binding_menu, c=Callback(open_scene, os.path.join(lect6_path, '09_hand_binding.ma')))
    cmds.menuItem(label='03 - Extras',  ann='Binding Extras - Skull and Skirt', p=binding_menu, c=Callback(open_scene, os.path.join(lect6_path, '10_skullsAndSkirt.ma')))

    
    cmds.menuItem(d=True, p=rba_menu)
    cmds.menuItem(label='Remove Menu', p=rba_menu, c=remove_menu)


def open_scene(scene_to_open):
    '''
    Open Requested Scene
    '''
    print 'open: %s' % scene_to_open
    # file -f -options "v=0"  -typ "mayaAscii" -o "/Users/mclavan/Desktop/game_rig_lectures/rba_lecture.ma";addRecentFile("/Users/mclavan/Desktop/game_rig_lectures/rba_lecture.ma", "mayaAscii");
    cmds.file( scene_to_open, f=True, options='v=0', typ='mayaAscii', o=True)

def remove_menu(*args):
    '''
    Removes RBA's Lecture
    '''
    cmds.deleteUI(rba_menu)