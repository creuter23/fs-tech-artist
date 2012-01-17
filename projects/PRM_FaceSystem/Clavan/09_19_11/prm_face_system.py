'''
PRM Face System

Description:
    This script create a face system with blend shapes provided by the modeler.
    - Different level's of the system can be generated depending upon how many
        blend shapes are provided by the modeler.

Credits:
    Michael Clavan
    Jenifer Conely
    David Vega
   
Updates:
    mclavan -
    
How to Run:
    import prm_face_system
    prm_face_system.gui()
        
'''

# How is the level system going to be broken up?
# Start small.  Think of how the mouth system will be generated.
# David recieves the blend shapes and the object (ty & tx) in which the blend shapes will be triggered.
# Jeniffer generates the different face controls that will drive david's system.


# Proof of concept version
#   - Technically she could create the face system by hand and just give me the object names to do a proof of concept.

def setup_face():
    
    print 'Face System has been created.'

def gui():
    '''
    Generates the interface for the prm_face_system script.
    '''
    
    print 'Interface Generated'
    

'''
Installer
- Open a maya scene.
- Interface pops up and ask premission to copy nessary files on to users computer.
- Check box for making a menu.
- Checks for the existance of the script already.
    - Config file.
        - Outdated?
            - Update old version.
- Check for the existance of modeling menu.
- Modeling Menu installer
    - Installs all of the modeling tools.
- Script env Installer
    - Master installer.
    - Will create a folder system of all the cg careers.
    
- xml driven.

'''
import os
import os.path
import maya.cmds as cmds
def toolset_move():
    current_path = os.path.split(__file__)[0]
    toolset_path = os.path.join(current_path, 'package')
    # By default this will be saved into the users scripts folder.
    # Recursively add all files and folder into scripts folder.
    #   Check to make sure dup files don't exists.
    
    # look for single folder at this time.
    # Just get the thing copied there.
    # If root/package doesn't exists then copy everything.
    script_folder = cmds.internalVar(userScriptDir=True)
    # if not os.path.exists(os.path.join )

'''
# Code Dump
import maya.cmds as cmds
cmds.internalVar(userScriptDir=1)

import os
target_path = r'/Users/mclavan/Desktop/script_installer/package/PRM_FaceSystem'
destin_path = r'/Users/mclavan/Library/Preferences/Autodesk/maya/2011-x64/scripts/PRM_FaceSystem'
os.rename(target_path, destin_path)

import shutil
if os.path.exists(destin_path):
    # Check Date
    print 'Checking date'
else:
    shutil.copytree(target_path, destin_path)

import filecmp
results = filecmp.dircmp(target_path, destin_path)
results.report()
if results.diff_files or results.right_only:
    print 'PRM - Face System currently exists, it does not match this system.\nDO YOU WANT TO CONTINUE?'
   
results.same_files    
help(results)
'''