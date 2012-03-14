'''
Welcome Script
global_var.py

Description:
    Discussion on scope.
    Scope means when variables and function exists.
    
import global_var
reload(global_var)
'''

print 'Welcome Script Activated'

import pymel.core as pm

# Global Variables


def gui():
    # Creating a window.
    win = pm.window(w=150, h=100)
    main = pm.columnLayout()
    
    # Here a three examples of interface components
    # EVERY interface element is named. Just like geometry in Maya.
    # You are given access to this name when a object is created in Maya.
    
    # 1) Maya names the textFieldButtonGrp.
    #    User chooses not to catch the name of the interface comp.
    pm.textFieldButtonGrp( label='Separator Attribute',
                          buttonLabel='Apply',
                          buttonCommand=work)
    # 2) User desides to catch the name of the textFieldButtonGrp.
    #    But it is local scope.  Only visible inside of this function.
    float_text = pm.textFieldButtonGrp( label='Float Attribute',
                          buttonLabel='Apply',
                          buttonCommand=work)    

    # 3) User catches interface name and makes it global to the script.
    global int_text
    int_text = pm.textFieldButtonGrp( label='Integer Attribute',
                          buttonLabel='Apply',
                          buttonCommand=work)
    
    # Showing a window
    win.show()


def work(*args):
    '''
    Print out what has been done to the scene.
    '''
    # Print out textFieldButtonGrp names
    # print float_text # Error, variable we are references only exists inside of gui function.
    
    print int_text
    
    # EXTRA NOTE
    # If you try to change the value of a global variable,
    #   you will have to define it global in the function if not done so already.
    # global int_text
    # int_text = 'new value'
    
    
    # Print out 
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