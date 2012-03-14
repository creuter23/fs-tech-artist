'''
Welcome Script
joint_resize.py

Description:
    Easy joint resize
    
import joint_resize
joint_resize.gui()

'''

print 'Welcome Script Activated'

import pymel.core as pm

def gui():
    # Creating a window.
    global win
    win = pm.window(w=150, h=100, title='Rigging toolset')
    main = pm.columnLayout()
    
    resize_gui()
    
    # Showing a window
    win.show()

def resize_gui():
    global joint_slider
    joint_slider = pm.floatSliderGrp(label='Joint Resize',
                            field=True, value=.2,
                            cc=joint_resize)
    
def joint_resize(*args):
    '''
    Resizes scenes joints
    '''
    # Get values from interface
    joint_size = joint_slider.getValue()
    # Apply values to command
    pm.jointDisplayScale(joint_size)

'''
Notes


'''