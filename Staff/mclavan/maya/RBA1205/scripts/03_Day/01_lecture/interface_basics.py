'''
Welcome Script
welcome.py

Description:
    Interface basics.
    
import welcome
reload(welcome)
'''

print 'Welcome Script Activated'

import pymel.core as pm

# Creating a window.
win = pm.window(w=150, h=100)
main = pm.columnLayout()

# Interface components go after the main layout,
#   but before the show method.
pm.button(label='Button 1', w=150)
pm.button(label='Button 2', w=150)
pm.button(label='Button 3', w=150)

# Showing a window
win.show()

'''
Notes

# Part 1
win = pm.window(w=150, h=300)
win.show()

# Part 2
# Layouts
win = pm.window(w=150, h=300)
main = pm.columnLayout()
win.show()

# Part 3
win = pm.window(w=150, h=100)
main = pm.columnLayout()

# 3 Buttons
pm.button(label='Button 1', w=150)
pm.button(label='Button 2', w=150)
pm.button(label='Button 3', w=150)

# Showing a window
win.show()
'''