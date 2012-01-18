import pymel.core as pm

def joint_rotation(joints):
    '''
    Checks through given joints for rotation values. 
    Arguments:
        joints - list of joints to check.
    '''
    invalid_joints = []
    for joint in joints:
        rotation_values = pm.xform(joint, q=1, rotation=True)
        if rotation_values[0] != 0 or rotation_values[1] != 0 or rotation_values[2] != 0:
            invalid_joints.append(joint)
    return invalid_joints
    
# Usage

def joint_gui():
    invalid_joints = joint_rotation(pm.ls(type='joint'))
    pm.window()
    pm.columnLayout()
    pm.text(l='Invalid Rotations', w=150)
    for joint in invalid_joints:
        pm.button(l=joint, w=150, c=pm.Callback(select_obj, joint))
    pm.showWindow()
 
def select_obj(obj):
    pm.select(obj, r=1)
