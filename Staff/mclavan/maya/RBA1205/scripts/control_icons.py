'''
#controlIcons #RBA #orientation

RBA Code Examples
Control Icons
control_icons.py

Description:
    This script contains different examples of creating control icons and orienting them.
    
import control_icons
reload(control_icons)

control_icons.create_icon_1()
control_icons.create_icon_2()
control_icons.create_icon_3()
control_icons.padding_1()
control_icons.padding_2('ring_root')
control_icons.eval_practice()
'''

import pymel.core as pm


# Joint clean up.
# Freeze Transform and Delete History
# Good for resarch and convert examples


# Create control icons

# Core
# Circle, square, cube
# half circle, quarter circle

def eval_practice():
    # Using a CV curve tool set to linear.  Trace a square on the grid.
    # curve -d 1 -p 1 0 1 -p 1 0 -1 -p -1 0 -1 -p -1 0 1 -p 1 0 1 -k 0 -k 1 -k 2 -k 3 -k 4 ;
    
    # Using mel.eval from pymel
    # Returns FLAT string value NOT a PyNode
    # # Result: u'curve1' # 
    icon_eval = pm.mel.eval('curve -d 1 -p 1 0 1 -p 1 0 -1 -p -1 0 -1 -p -1 0 1 -p 1 0 1 -k 0 -k 1 -k 2 -k 3 -k 4 ;')
    print 'Mel Eval:', icon_eval
    
    # Returns a Pynode
    # Result: nt.Transform(u'curve2') # 
    # Pain to convert!
    icon = pm.curve(d=1, p=[[1, 0, 1], [1, 0, -1], [-1, 0, -1], [-1, 0, 1], [1, 0, 1]], k=[0, 1, 2, 3, 4])
    print 'Mel2Python Conversion:', icon
    
    # Best of both worlds
    # pm.PyNode takes a string name and gets its object.
    icon_eval2 = pm.mel.eval('curve -d 1 -p 1 0 1 -p 1 0 -1 -p -1 0 -1 -p -1 0 1 -p 1 0 1 -k 0 -k 1 -k 2 -k 3 -k 4 ;')    
    icon_obj = pm.PyNode(icon_eval2)
    print 'Using mel eval and still get object: eval_icon: ', icon_eval2, ' object: ', icon_obj
    icon_obj.rename('test_rename')
    print 'After rename: eval_icon: ', icon_eval2, ' object: ', icon_obj

# Arrows
# Single, Double, thin, thick



# What are we trying to accomplish here?
#   Select a joint, then create a control with proper orientation and padding.
# Creating a control icon
def create_icon_1():
    # Just creating a control icon.
    icon = pm.circle(nr=[0,1,0])  
    # Create the nurbs circle returns references to the circle's transform and history node.
    # Result: [nt.Transform(u'nurbsCircle1'), nt.MakeNurbCircle(u'makeNurbCircle1')] #
    # icon is a varable used to store the results of creating the nurbs circle.    
    
    print 'Circle control created:', icon
    
    
def create_icon_2():
    '''
    Select a joint in the scene.  A nurbs circle will be created at the selected joint position.
    '''
    # Get selected objects in maya.
    selected = pm.ls(sl=True)[0] # I only want the first selected control (At this time anyway.)
    
    # Move control icon to selected joint
    icon = pm.circle(nr=[0,1,0])
    
    
    # Get selected transforms
    selected_trans = selected.getTranslation(space='world')
    # Apply to created control icon
    icon[0].translate.set(selected_trans)

# Ask yourself these questions.
# What parts of create_icon_2 could I reuse?
# Will I need to move different control icons to selected joints in the future?
# Could I split this function up into two parts creating icons and then moving icons?
# Reseach functions arguments and return statments (book: Chapter 5 google:"python functions arguments")
 
'''
Research Topics Covered:

Dot Notation # selected.getTranslation(space='world')
Methods vs Functions: What is the difference?

'''
 
  
# At this point we can go into two different directions.
# Work with multiple objects in your scene  (loop)
# or
# Focus on orienting the control to the joint. (parenting, grouping, and constraints)

def create_icon_3():
    '''
    Select a joint in the scene.  A nurbs circle will be created and oriented at the selected joint position.
    '''
    # Get selected objects in maya.
    selected = pm.ls(sl=True)[0] # I only want the first selected control (At this time anyway.)
    
    # Move control icon to selected joint
    icon = pm.circle(nr=[0,1,0])
    
    
    # Using point and Orient constraint for position and orientation.
    point_const = pm.pointConstraint(selected, icon)
    orient_const = pm.orientConstraint(selected, icon)
    # constraints were never meant to be kept.  Deleting them.
    pm.delete(point_const, orient_const)
    
    
def padding_1():
    '''
    Select a control then a joint to sync orientation together and then create the desired amount of pads.
    '''
    selected = pm.ls(sl=True)
    control_icon = selected[0]
    joint_object = selected[1]
    
    pad = pm.group(em=True)
    
    # Move control and pad to joints's position and orientation.  Using constraints!
    icon_point = pm.pointConstraint(joint_object, control_icon)
    pad_point = pm.pointConstraint(joint_object, pad)
    icon_orient = pm.orientConstraint(joint_object, control_icon)
    pad_orient = pm.orientConstraint(joint_object, pad)
    # Delete Constraints
    pm.delete(icon_point, pad_point, icon_orient, pad_orient)
    
    # Parent icon to pad
    pm.parent(control_icon, pad)
    
    
    # What about naming the pad and control icon?
    # What if I want more than one pad?  I should be able to create as many pads as I want.
    # What if I want to insert a pad after the face?
    # Remeber to write down possible additions to the script, but manage you time.
    #   Make sure you get a working system first then add on.
    #   You don't want to spend all you time on a side project.
    

def padding_2(control_name):
    '''
    Select a control then a joint to sync orientation together and then create the desired amount of pads.
    '''
    selected = pm.ls(sl=True)
    control_icon = selected[0]
    joint_object = selected[1]
    
    # Create pad and rename control
    control_icon.rename('%s_icon' % control_name)
    pad = pm.group(em=True, name='%s_pad' % control_name)
    
    # Move control and pad to joints's position and orientation.  Using constraints!
    icon_point = pm.pointConstraint(joint_object, control_icon)
    pad_point = pm.pointConstraint(joint_object, pad)
    icon_orient = pm.orientConstraint(joint_object, control_icon)
    pad_orient = pm.orientConstraint(joint_object, pad)
    # Delete Constraints
    pm.delete(icon_point, pad_point, icon_orient, pad_orient)
    
    # Parent icon to pad
    pm.parent(control_icon, pad)

    