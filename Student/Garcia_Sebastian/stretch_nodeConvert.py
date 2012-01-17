'''
Utility convert expresions to nodes
'''

arc_curve = cmds.arclen(ch=1)
# Resting arcLength (constant)
curve_len = cmds.getAttr(arc_curve + ".arcLength")

selected_joints = cmds.ls(sl=True)
for sel in selected_joints:

    # Loop though all the joints
    # shadingNode -asUtility multiplyDivide;
    current_mult = cmds.createNode('multiplyDivide', n='%s_scaleNode' % sel)
    cmds.setAttr('%s.operation' % current_mult, 2)
    cmds.setAttr('%s.input1X' % current_mult, curve_len)
    cmds.connectAttr('%s.arcLength' % arc_curve, '%s.input2X' % current_mult)

    cmds.connectAttr('%s.outputX' % current_mult, '%s.sx' % sel)
