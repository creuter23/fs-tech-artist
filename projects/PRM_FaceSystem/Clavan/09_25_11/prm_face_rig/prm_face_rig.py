'''
PRM Face Rig
prm_face_rig.py

Description:
    - Auto Face Rigging System for PRM
   
How To Run:

import prm_face_rig.prm_face_rig as prm_face
reload(prm_face)
prm_face.gui()

'''

import maya.cmds as cmds
import os.path

def gui():
    icon_path = os.path.join(os.path.split(__file__)[0], 'icons') 
    win_width = 314
    win = 'prm_face_win'
    cmds.window(win, sizeable=0, w=win_width, t='PRM Face System')
    main = cmds.columnLayout(bgc=[.78, .69, .6])
    cmds.image(w=314, h=65, i=os.path.join(icon_path, 'rba_installer.png'))
    icon_width = 128 / 2
    icon_height = 181 / 2
    # Level 1 Mouth Shapes
    cmds.frameLayout(label="Mouth Shapes", w=314, h=icon_height + 65, bgc=[.52, .47, .4])
    cmds.scrollLayout()
    row = cmds.rowColumnLayout(nr=1)
    Face_Button(parent=row, label='Left Smile', image=os.path.join(icon_path, 'lt_mouth_smile.gif'), width=icon_width, height=icon_height)
    Face_Button(parent=row, label='Left Frown', image=os.path.join(icon_path, 'lt_mouth_frown.gif'), width=icon_width, height=icon_height)
    Face_Button(parent=row, label='Left Wide', image=os.path.join(icon_path, 'lt_mouth_wide.gif'), width=icon_width, height=icon_height)
    Face_Button(parent=row, label='Left OO', image=os.path.join(icon_path, 'lt_mouth_oo.gif'), width=icon_width, height=icon_height)

    Face_Button(parent=row, label='Rigth Smile', image=os.path.join(icon_path, 'rt_mouth_smile.gif'), width=icon_width, height=icon_height)
    Face_Button(parent=row, label='Right Frown', image=os.path.join(icon_path, 'rt_mouth_frown.gif'), width=icon_width, height=icon_height)
    Face_Button(parent=row, label='Right Wide', image=os.path.join(icon_path, 'rt_mouth_wide.gif'), width=icon_width, height=icon_height)
    Face_Button(parent=row, label='Right OO', image=os.path.join(icon_path, 'lt_mouth_oo.gif'), width=icon_width, height=icon_height)
    cmds.setParent(main)


    # Level 1 Eye
    # Lt and Rt Eye Close
    
    # Level 2
    # Lt and Rt Upper lid and lower lid surprise and close. (4 Shapes each side)
    cmds.frameLayout(label="Eye Lid Shapes", w=314, h=icon_height + 65, bgc=[.52, .47, .4])
    cmds.scrollLayout()    
    row2 = cmds.rowColumnLayout(nr=1)
    Face_Button(parent=row2, label='Left Up Wide', image=os.path.join(icon_path, 'lt_eye_wide.png'), width=icon_width, height=icon_height)
    Face_Button(parent=row2, label='Left Up Close', image=os.path.join(icon_path, 'lt_eye_closed.gif'), width=icon_width, height=icon_height)
    Face_Button(parent=row2, label='Left Low Wide', image=os.path.join(icon_path, 'lt_eye_wide.png'), width=icon_width, height=icon_height)
    Face_Button(parent=row2, label='Left Low Close', image=os.path.join(icon_path, 'lt_eye_closed.gif'), width=icon_width, height=icon_height)

    Face_Button(parent=row2, label='Right Up Close', image=os.path.join(icon_path, 'rt_eye_closed.gif'), width=icon_width, height=icon_height)
    Face_Button(parent=row2, label='Rigth Up Wide', image=os.path.join(icon_path, 'lt_eye_wide.png'), width=icon_width, height=icon_height)
    Face_Button(parent=row2, label='Right Low Close', image=os.path.join(icon_path, 'rt_eye_closed.gif'), width=icon_width, height=icon_height)
    Face_Button(parent=row2, label='Rigth Low Wide', image=os.path.join(icon_path, 'lt_eye_wide.png'), width=icon_width, height=icon_height)
    cmds.setParent(main)


    # Level 1 Brow
    # Eye Brow Up and Down
    cmds.frameLayout(label="Eye Brow Shapes", w=314, h=icon_height + 47, bgc=[.52, .47, .4])
    cmds.scrollLayout()    
    row3 = cmds.rowColumnLayout(nr=1)
    Face_Button(parent=row3, label='Left Up', image=os.path.join(icon_path, 'lt_brow_up.gif'), width=icon_width, height=icon_height)
    Face_Button(parent=row3, label='Left Down', image=os.path.join(icon_path, 'rt_brow_down.gif'), width=icon_width, height=icon_height)
    Face_Button(parent=row3, label='Right Up', image=os.path.join(icon_path, 'rt_brow_up.gif'), width=icon_width, height=icon_height)
    Face_Button(parent=row3, label='Right Down', image=os.path.join(icon_path, 'rt_brow_down.gif'), width=icon_width, height=icon_height)
    cmds.setParent(main)
    # Level 2 Inside, Mid, Outside (Lt and Rt), Center
    

    # Binding System
    # Jaw System
    
    # Neck System
    
    cmds.button(w=win_width, l='Apply Face System', bgc=[1, 0.9, 0.4])
    
    cmds.showWindow()


class Face_Button():
    def __init__(self, label, image, width=128, height=128, parent=None):
        self.label = label
        self.image = image
        self.state = True
        self.main = cmds.columnLayout()
        self.btn = cmds.symbolButton(bgc=[1, 0, 0], i=self.image, w=width, h=height,
            c=self.toggle_btn)
        self.text = cmds.text(l=self.label, bgc=[1, 0, 0], w=width)
        cmds.setParent(parent)
        
    def toggle_btn(self, *args):
        if self.state:
            cmds.symbolButton(self.btn, e=1, bgc=[0, 1, 0])
            cmds.text(self.text, e=1, bgc=[0, 1, 0])
            
            self.state = False
            print '%s: State True' % self.label
        else:
            cmds.symbolButton(self.btn, e=1, bgc=[1, 0, 0])
            cmds.text(self.text, e=1, bgc=[1, 0, 0])
            self.state = True
            print '%s: State False' % self.label
            
'''        
cmds.window()
cmds.columnLayout()
over_width = 200
cmds.text(label='Mouth System - Level 0', w=over_width)
cmds.rowColumnLayout(nr=1, h=5)
btn_seg = 5
btn_width = over_width / btn_seg
total_seg = 5
color = {'red': [1, 0, 0], 'yellow': [0, 1, 0], 'green': [0, 1, 0]} 
for i in xrange(total_seg):
   cmds.text(l=' ', bgc=color['red'], w=btn_width)

cmds.setParent('..')
cmds.rowColumnLayout(nr=1, h=5)
for i in xrange(total_seg):
   cmds.text(l=' ', bgc=color['red'], w=btn_width)

cmds.setParent('..')
cmds.rowColumnLayout(nr=1, h=5)
for i in xrange(total_seg):
   cmds.text(l=' ', bgc=color['red'], w=btn_width)
# cmds.text(l=' ', bgc=[1, 0, 0], w=btn_width)
# cmds.text(l=' ', bgc=[1, 0, 0], w=btn_width)
# cmds.text(l=' ', bgc=[1, 0, 0], w=btn_width)

cmds.showWindow()        
        
        
class Level_Bar():
    def __init__(self):
        cmds.rowColumnLayout()        
'''