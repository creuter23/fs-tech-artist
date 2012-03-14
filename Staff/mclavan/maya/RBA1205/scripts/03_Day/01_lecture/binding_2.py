'''
Welcome Script
binding_2.py

Description:
    Different interface components have different triggers.
    Button has command
    intField has changeCommand and dragCommand
    
    
import binding_2
reload(binding_2)
'''

print 'Binding interface components to functions 2.'

import pymel.core as pm



def gui():
    # Creating a window.
    win = pm.window(w=150, h=100)
    main = pm.columnLayout()
    
    # Interface components go after the main layout,
    # Different components simular flags
    # They all have a rectangle bounding box!
    pm.button(w=150, command=work)
    
    pm.textFieldButtonGrp( label='Float Attribute',
                          buttonLabel='Apply',
                          buttonCommand=work)
    
    pm.intField(w=150, changeCommand=work)
    pm.floatSliderGrp(changeCommand=work)

    pm.floatSliderGrp(cc=work, dc=work)
    
    # Showing a window
    win.show()

def work(*args):
    '''
    Print out what has been done to the scene.
    '''
    print 'Work has been completed.'
 
    
'''
Notes

def function_name():
    print 'Function executed'

# Inside the script
function_name()

# Outside of the script
script_name.function_name()

'''