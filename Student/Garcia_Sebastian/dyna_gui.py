import maya.cmds as cmds
import pymel.core as pm

dyna_delete = ''
def gui():
    win_width = 225
    cmds.window( title='Attr Field Slider Groups' )
    main = cmds.columnLayout()
    
    selected = cmds.ls(sl=True)
    attrs = ['ty']
    cmds.text(label='TranslateY', w=win_width)
    
    # Dynanmic Area
    global dyn_delete
    # Anchor Point (Cannot be deleted)
    dyn_gui = cmds.columnLayout()
    # Removed dynamicly
    dyn_delete = cmds.columnLayout()
    dynamic1 = update_gui(dyn_delete, selected, attrs)
    cmds.setParent(main)    
    
    cmds.button(w=win_width, label='Update', c=pm.Callback(update_selected, dyn_gui, attrs))
    cmds.showWindow()

def update_selected(current_parent, attrs):
    selected = cmds.ls(sl=True)
    global dyna_delete    
    cmds.deleteUI(dyna_delete)
    dyna_delete = update_gui(current_parent, selected, attrs)
    
def update_gui(current_parent, selected, attrs):
    main = cmds.columnLayout(parent=current_parent)
    for sel in selected:
        for attr in attrs:
            cmds.attrFieldSliderGrp( w=225, cw=[[1,75], [2,50], [3,100]], label='%s' % sel, min=-10.0, max=10.0, at='%s.%s' % (sel, attr) )
    
    return main
  
gui()