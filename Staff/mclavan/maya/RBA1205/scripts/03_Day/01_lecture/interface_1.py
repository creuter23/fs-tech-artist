'''
Welcome Script
interface_1.py

Description:
    Interface basics 1.
    
import interface_1
reload(interface_1)
'''

print 'Welcome Script Activated'

import pymel.core as pm

# Creating a window.
win = pm.window(w=150, h=100)
main = pm.columnLayout()

# Interface components go after the main layout,
# Different components simular flags
# They all have a rectangle bounding box!
pm.button(label='Button 1', w=150)
pm.button(label='Button 2', w=150)
pm.button(label='Button 3', w=150)

# Showing a window
win.show()

'''
Notes

# Buttons
pm.button(label='Button 1', width=150)

Flags
width(w)
height(h)
label(l)

'''