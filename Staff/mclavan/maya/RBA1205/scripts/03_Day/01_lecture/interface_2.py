'''
Welcome Script
interface_2.py

Description:
    Interface basics 2.
    
import interface_2
reload(interface_2)
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
pm.text(label='Button 2', w=150)
pm.separator(w=150, h=20)
pm.textField(w=150)

# Showing a window
win.show()

'''
Notes

# Buttons
pm.button(label='Button 1', width=150)

# Text
pm.text(label='User Information', width=150)

# separator
pm.separator(w=150, h=20)


# fields
# Many more examples
pm.intField(w=150)
pm.floatField(w=150)
pm.textField(w=150)
pm.checkBox(label='On/Off', w=150)

# Groups podcast
pm.floatSliderGrp(w=150)

# menu podcasts

# radioButton podcasts

'''