'''
Welcome Script
functions_1.py

Description:
    Breaking up inteface functions.
    
import functions_2
reload(functions_2)
functions_2.gui()
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
    
    # Call attr_gui function
    attr_gui()
    # button_gui()
    
    # Showing a window
    win.show()

def attr_gui():
    '''
    Guts of the attribute interface.
    '''
    pm.textFieldButtonGrp( label='Separator Attribute' )
    pm.textFieldButtonGrp( label='Float Attribute' )
    pm.textFieldButtonGrp( label='Int Attribute' )
        
def button_gui():
    pm.button(label='Button 1', w=150)
    pm.button(label='Button 2', w=150)
    pm.button(label='Button 3', w=150)
