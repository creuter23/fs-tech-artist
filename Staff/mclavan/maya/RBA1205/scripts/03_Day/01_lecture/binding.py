'''
Welcome Script
binding.py

Description:
    Binding functions to buttons.
    
import binding
reload(binding)
'''

print 'Welcome Script Activated'

import pymel.core as pm



def gui():
    # Creating a window.
    win = pm.window(w=150, h=100)
    main = pm.columnLayout()
    
    # Interface components go after the main layout,
    # Different components simular flags
    # They all have a rectangle bounding box!
    pm.button(w=150, command=work)
    global object
    object = pm.textFieldButtonGrp( label='Float Attribute',
                          buttonLabel='Apply',
                          buttonCommand=work)
    
    
    # Showing a window
    win.show()

def work(*args):
    '''
    Print out what has been done to the scene.
    '''
    print 'Work has been completed.'
    print object.getValue()
    
    
'''
Notes

def function_name():
    print 'Function executed'

# Inside the script
function_name()

# Outside of the script
script_name.function_name()

'''