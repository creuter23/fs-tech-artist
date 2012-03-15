'''
Lecture 4 - Catching Data

Description:
    Lecture 4 consists of developing basic tools.
    Students will learn how to research and convert commands into python.
    Students will also learn how to break down complex system and replicate them in code.
    Topics Covered:
        - Variables
        - Lists
        - Maya Command Anatomy
        - Automating systems
        - Functions args and returns statment
        
    What should I know after looking at this script?
        - How to get selected object in a Maya scene.
        - How to get attribute values from a object in Maya.
        - How to take values from one object and apply it to another in Maya.
        
    Questions you should ask yourself:
        
'''

import pymel.core as pm
'''
Catching Informatino
'''

# Select two object in your scene.
selected = pm.ls(sl=True)  # Returns selected objects in the scene.
print selected
# It will print out something like this (depends on what you have selected.)
# Result: [nt.Transform(u'control1_icon'), nt.Transform(u'control2_icon'), nt.Transform(u'control3_icon')] # 
# Three transforms selected in our scene

# Creating objects
icon = pm.circle(nr=[0, 1, 0])
print icon
# [nt.Transform(u'nurbsCircle1'), nt.MakeNurbCircle(u'makeNurbCircle2')]
# Returns the transform and history node of the nurbs circle created.

# Getting object position
# Built in methon in pymel
# icon[0] is the transform node created above.
trans = icon[0].getTranslation()
print trans  # [0, 0, 0]

# Getting values by attribute
tx_value = icon[0].tx.get()  # prints 0
trans_value = icon[0].translate.get()  # translate
# Long and short names work
trans_value = icon[0].t.get()  # translate

'''
Snapping one object to another.
'''
# Get first item selected
selected = pm.ls(sl=True)[0] # Remember zero index if first item.

# Create control icon
icon = pm.circle(nr=[0, 1, 0]) # Returns the transform and history node
#                              0                                    1
# Result: [nt.Transform(u'nurbsCircle2'), nt.MakeNurbCircle(u'makeNurbCircle3')] # 

# Get selected transform
sel_trans = selected.translate.get()
# Set icon's Transform to selected position.
icon[0].translate.set(sel_trans)

'''
Interfaces - Review
'''
# Remember: global variables and scope
def gui():
    win = pm.window(w=200, h=300, title='Values')
    main = pm.columnLayout()
    global border_slider
    border_slider = pm.floatSliderGrp(field=True, min=0.01, max=10, dc=border_size)  # border_slider now contains the slider object.
    win.show()

def border_size(*args):
    '''
    Change normal size
    '''
    # get value from slider
    border_thick = border_slider.getValue()
    
    # Show Border edge
    pm.polyOptions(db=True)
    pm.polyOptions(sb=border_thick)

'''
Cool Stuff
'''


'''
Podcast Request
Reference - ls command
'''

'''
Podcast Request
Reference - Tramsform and Shape
'''


'''
Podcast Request
Reference - 
'''

