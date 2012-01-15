'''
hud_maya.py
Michael Clavan

Description:
    Renders out hud for selected geometry, then send it into nuke to have a
        hud created and a movie generated.
    If any of the options haven't been changed, then the script will use default
        settings.
        
How To Run:

import hud_maya
hud_maya.gui()

'''

import maya.cmds as cmds
import pymel.core as pm

win_width = 260
win_heigth = 337
win_name = 'hud_win'

def gui():
    '''
    Interface for the HUD generator.
    '''
    if cmds.window(win_name, ex=True):
        cmds.deleteUI(win_name)
    if cmds.windowPref(win_name, ex=True):
        cmds.windowPref(win_name, r=True)
            
    cmds.window(win_name, w=260, h=337, title='HUD Interface')
    main = cmds.columnLayout()
    # cmds.image(w=240, h=51)
    cmds.rowColumnLayout(nc=2)
    cmds.textField(w=183, h=26, text='Ref Path')
    cmds.button(w=48, h=28, l='Ref',
                ann='Swap out reference')
    cmds.setParent(main)
    
    cmds.rowColumnLayout(nc=2)
    cmds.textField(w=135, h=26, text='hud_material')
    cmds.button(w=89, h=28, l='Material',
                ann='Grabs the selected material',
                command=ref_swap)
    cmds.setParent(main)
    
    cmds.rowColumnLayout(nc=3)
    cmds.text(w=105 , h=21 , l='Frame Range')
    cmds.intField(w=65, h=26, v=0)
    cmds.intField(w=65, h=26, v=100)
    cmds.setParent(main)
    
    cmds.rowColumnLayout(nc=2)
    cmds.textField(w=183, h=26, text='output path')
    cmds.button(w=42, h=28, l='Out')
    cmds.setParent(main)
    
    cmds.button(w=232, h=28, l='Render') 
    cmds.showWindow()
    
def ref_swap(*args):
    '''
    Swaps out with new reference.
    '''
    # From interface get the reference to be swapped.
    
    # Apply material to all children
    print 'ref swapped.'
    
    
def text_swap(*args):
    '''
    Swap new material.
    '''
    
    print 'text swapped.'

'''
import maya.cmds as cmds
import sys
sys.path.append(r'/Users/mclavan/Documents/Projects/HUD/HUD_Shot')

import os
os.environ['ref_path'] = ''
os.environ['ref_material'] = ''
os.environ['ref_type']
os.environ['ref_name']
os.environ['ref_artist']
# type, name, 
setAttr "defaultRenderGlobals.endFrame" 1;
cmds.getAttr('defaultRenderGlobals.endFrame')
cmds.setAttr('defaultRenderGlobals.endFrame', 3)
import hud_maya
reload(hud_maya)
hud_maya.gui()

cmds.Mayatomr(render=True)

print 'Starting Render'
cmds.BatchRender();
print 'Render Compelte'
win = cmds.window(t='post render', w=100, h=100)
cmds.showWindow(win)
defaultRenderGlobals.postRenderMel
setAttr -type "string" defaultRenderGlobals.preMel "python(\"print 'Before Render'\");";


python("import subprocess;subprocess.call(['/Applications/ScreenFlow.app/Contents/MacOS/ScreenFlow'])")
mclavan$ /Applications/ScreenFlow.app/Contents/MacOS/ScreenFlow

# Render Notes
/Applications/Autodesk/maya2012/Maya.app/Contents/scripts/others/mayaBatchRender.mel

# Script Editor Echo On Render
BatchRender;
mayaBatchRender;
commandPort -rnc -n "mclavan.local:7835" -prefix "batchRender -status";
// Saving temporary file: /Users/mclavan/Documents/Projects/HUD/HUD_Shot/hud_shot__1386.mb // 
file -f -ea -type mayaBinary "/Users/mclavan/Documents/Projects/HUD/HUD_Shot/hud_shot__1386.mb";
fileCmdCallback;
about -application;
// maya // 
about -product;
// Maya 2012 // 
about -version;
// 2012 Hotfix 4 x64 // 
about -cutIdentifier;
// 201107271632-806479 // 
about -osv;
// Mac OS X 10.6.8 // 
pluginInfo -q -pluginsInUse -activeFile;
// Mayatomr 2012.0m - 3.9.1.43  stereoCamera 10.0 // 
memory -he;
// 269.238281 // 
memory -fr;
// 0 // 
memory -pf;
// 66 // 
// /Users/mclavan/Documents/Projects/HUD/HUD_Shot/hud_shot__1386.mb // 
// Rendering with mental ray... // 
selectToolValues nurbsSelect;
toolPropertyShow;
changeToolIcon;
// Result: Percentage of rendering done: 0 (/Users/mclavan/Documents/Projects/HUD/HUD_Shot/images/hud_shot.001.tga) // 
// Result: Percentage of rendering done: 5 (/Users/mclavan/Documents/Projects/HUD/HUD_Shot/images/hud_shot.001.tga) // 
// Result: Percentage of rendering done: 10 (/Users/mclavan/Documents/Projects/HUD/HUD_Shot/images/hud_shot.001.tga) // 
// Result

# Console
"/Applications/Autodesk/maya2012/Maya.app/Contents/bin/Render" -interactive 1  -r interBatch  -proj "/Users/mclavan/Documents/Projects/HUD/HUD_Shot" -A mclavan.local:7835 "/Users/mclavan/Documents/Projects/HUD/HUD_Shot/hud_shot__1386.mb" 1>> "/Users/mclavan/Library/Logs/Maya/mayaRender.log" 2>&1

'''