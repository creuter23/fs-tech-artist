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
    lect5_path = os.path.join(base_path, 'scenes', 'lecture5', 'scenes')
    lect6_path = os.path.join(base_path, 'scenes', 'lecture5', 'scenes')
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

    
    lect5_conn = cmds.menuItem(label='Connections', ann='Part 1 - Joints', sm=True, p=lect5)
    cmds.menuItem(label='01 - Control Icons',  ann='Joints and Orientation', p=lect5_conn, c=Callback(open_scene, os.path.join(lect5_path, 'body.ma')))
    cmds.menuItem(label='02 - Body',  ann='Joints and Orientation', p=lect5_conn, c=Callback(open_scene, os.path.join(lect5_path, 'body.ma')))
    cmds.menuItem(label='03 - Arm',  ann='Joints and Orientation', p=lect5_conn, c=Callback(open_scene, os.path.join(lect5_path, 'body.ma')))
    cmds.menuItem(label='04 - Leg',  ann='Joints and Orientation', p=lect5_conn, c=Callback(open_scene, os.path.join(lect5_path, 'body.ma')))
    cmds.menuItem(label='05 - Head',  ann='Joints and Orientation', p=lect5_conn, c=Callback(open_scene, os.path.join(lect5_path, 'body.ma')))
    
    cmds.menuItem(label='Lecture 6', ann='Complex Systems and Binding', sm=True, p=rba_menu)
    
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