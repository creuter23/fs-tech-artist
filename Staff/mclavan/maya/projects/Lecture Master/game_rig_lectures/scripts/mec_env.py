'''
mec_env.py
Michael Clavan

Description:
    Different scripts for handelling setting up maya scene enviroment.
    
'''


import maya.cmds as cmds
import maya.mel as mel

import os.path
import sys
# Get the workspace directory and remove the ending backslash.


scene_path = cmds.file(q=True, sn=True)
base_path = os.path.split(scene_path)
print 'Scene Path: %s\nBase Path: %s' % (scene_path, base_path)

def quick_set_proj():
    '''
    Sets the project to where the current file is located.
    '''
    
    scene_path = cmds.file(q=True, sn=True)
    base_path = os.path.split(scene_path)
    
    # Setting Project and workspace
    # Find out how workspace and setting parent differ.
    mel.eval('setProject("%s")' % base_path[0])
    cmds.workspace(dir=base_path[0])

def generate_menu():
    '''
    Generates a RBA menu for lecture 5 and 6.
    '''
    '''
    # sceneDir = cmds.workspace( q=True, dir=True )[:-1]
    scripts_path = os.path.join(base_path[0], 'scripts')
    scenes_path = os.path.join(base_path[0], 'scenes')
    sys.path.append(scripts_path)
    '''
    import rba_menu
    # reload(rba_menu)
    quick_set_proj()
    rba_menu.exe_menus()


