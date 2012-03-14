'''
Welcome Script
functions_1.py

Description:
    Function basics.
    
import functions_1
reload(functions_1)
'''

print 'Welcome Script Activated'

import pymel.core as pm

'''
# Creating a window.
win = pm.window(w=150, h=100)
main = pm.columnLayout()
pm.textFieldButtonGrp( label='Float Attribute', buttonLabel='Apply' )
   
# Showing a window
win.show()
'''

def gui():
    # Creating a window.
    win = pm.window(w=150, h=100)
    main = pm.columnLayout()
    
    # Interface components go after the main layout,
    # Different components simular flags
    # They all have a rectangle bounding box!
    pm.textFieldButtonGrp( label='Float Attribute', buttonLabel='Apply' )
    
    
    # Showing a window
    win.show()

'''
Notes

def function_name():
    print 'Function executed'

# Inside the script
function_name()

# Outside of the script
script_name.function_name()

'''