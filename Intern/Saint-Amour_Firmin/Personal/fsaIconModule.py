'''
test at creating module
module will contain some commonly used icons

'''
import maya.cmds as cmds
import maya.mel as mel


    
    
# icons
# all icons recieve 3 agrs
# first the name
# second is postion what the object will be pointConstrained to, so the icon will be placed where the joint is
# last is the size which controls the initial scale, by default size is 0 



def cube(name, position, size=1):
    j=mel.eval('curve -d 1 -p 0.872112 0.872112 -0.872112 -p -0.872112 0.872112 -0.872112 \
             -p -0.872112 0.872112 0.872112 -p 0.872112 0.872112 0.872112 \
             -p 0.872112 0.872112 -0.872112 -p 0.872112 -0.872112 -0.872112 -p -0.872112 -0.872112 -0.872112 \
             -p -0.872112 0.872112 -0.872112 -p -0.872112 -0.872112 -0.872112 -p -0.872112 -0.872112 0.872112 \
             -p -0.872112 0.872112 0.872112 -p -0.872112 -0.872112 0.872112 -p 0.872112 -0.872112 0.872112 -p 0.872112 0.872112 0.872112 \
             -p 0.872112 -0.872112 0.872112 -p 0.872112 -0.872112 -0.872112 -k 0 -k 1.744225 -k 3.48845 -k 5.232675 -k 6.976899 \
             -k 8.721124 -k 10.465349 -k 12.209574 -k 13.953799 -k 15.698024 -k 17.442249 -k 19.186474 -k 20.930698 -k 22.674923 -k 24.419148 -k 26.163373 ;')
    cmds.select(j)
    k=cmds.rename(name)
    cmds.scale( size,size,size )
    i=cmds.pointConstraint(position, k)
    # deletes constraint and freezes transforms
    cmds.delete(i)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=1)
    return k

    

def circleH(name, position, size=1):
    j=cmds.circle(c=[0,0,0], nr=[0,1,0], sw=360, r=size, d=3, ut=0, tol=0.01, s=8, ch=1, n=name)
    i=cmds.pointConstraint(position, j)
    # deletes constraint nad freezes transforms
    cmds.delete(i)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=1)
    return j

def circleV(name, position, size=1):
    j=cmds.circle(c=[0,0,0], nr=[0,1,0], sw=360, r=size, d=3, ut=0, tol=0.01, s=8, ch=1, n=name)
    cmds.delete(j,ch=True)
    cmds.setAttr("%s.rz" % name, 90)
    i=cmds.pointConstraint(position, name)
    # deletes constraint nad freezes transforms
    cmds.delete(i)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=1)
    return j
    
def plusH(name, position, size=1):
    j=mel.eval('curve -d 1 -p -1 0 1 -p -3 0 1 -p -3 0 -1 -p -1 0 -1 -p -1 0 -3 \
            -p 1 0 -3 -p 1 0 -1 -p 3 0 -1 -p 3 0 1 -p 1 0 1 -p 1 0 3 -p -1 0 3 \
            -p -1 0 1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 ;')
    cmds.delete(j, ch=True)
    k=cmds.rename(j,name)
    cmds.scale( size,size,size )
    i=cmds.pointConstraint(position, k)
    # deletes constraint nad freezes transforms
    cmds.delete(i)
    cmds.makeIdentity(k, apply=True, t=1, r=1, s=1, n=1)
    cmds.move( 0,0,-5, k , os=True)
    cmds.makeIdentity(k, apply=True, t=1, r=1, s=1, n=1)
    return k
    
def plusV(name, position, size=1):
    j=mel.eval('curve -d 1 -p -1 0 1 -p -3 0 1 -p -3 0 -1 -p -1 0 -1 -p -1 0 -3 \
            -p 1 0 -3 -p 1 0 -1 -p 3 0 -1 -p 3 0 1 -p 1 0 1 -p 1 0 3 -p -1 0 3 \
            -p -1 0 1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 ;')
    cmds.delete(j,ch=True)
    k=cmds.rename(j,name)
    cmds.setAttr(k+".rx", 90)
    cmds.scale( size,size,size )
    i=cmds.pointConstraint(position, k)
    # deletes constraint nad freezes transforms
    cmds.delete(i)
    cmds.makeIdentity(k, apply=True, t=1, r=1, s=1, n=1)
    cmds.move( 0,0,-5, k , os=True)
    cmds.makeIdentity(k, apply=True, t=1, r=1, s=1, n=1)
    return k


# create a nurbs line that goes from the pole vector icon to the elbow or knee joint
# name-name of the curve, icon=name of the polevector icon, joint= name of joint
def pvLine(name, icon, joint):
    j=mel.eval('curve -d 1 -p 0 0 0 -p 1 0 0 -k 0 -k 1 ;')
    k=cmds.rename(name)
    c1=cmds.cluster('%s.cv[0]' % k, n='%s_cluster' % k)
    c2=cmds.cluster('%s.cv[1]' % k, n='%s_cluster' % k)
    cmds.parentConstraint(icon, c1, mo=0)
    cmds.parentConstraint(joint, c2, mo=0)
    i=cmds.group(k,c1,c2, n='%s_pad' % name)
    cmds.setAttr('%sHandle.visibility' % c1[0], 0)
    cmds.setAttr('%sHandle.visibility' % c2[0], 0)
    cmds.setAttr('%sShape.overrideDisplayType' % k, 2)
    cmds.setAttr('%sShape.overrideEnabled' % k, 1)
    return i
    


# orients the icon and pads it
# icon= icon for pading
# joint= joint to base orientation off of
def orientpad(icon, joint):
    i=cmds.group( em=1, name="%s_pad" % icon[0])    
    k=cmds.pointConstraint(joint, i)
    cmds.delete(k)    
    cmds.parent(icon[0], i )
    cmds.parent(i, joint)
    cmds.setAttr("%s.rx" % i, 0)     
    cmds.setAttr("%s.ry" % i, 0)     
    cmds.setAttr("%s.rz" % i, 0)     
    cmds.parent(i, w=1)
    cmds.makeIdentity(icon[0], apply=True, t=1, r=1, s=1, n=0)
    cmds.orientConstraint(icon[0], joint)
    return i
    

# create the icon that will have the IK_FK switch Attr
def SwitchIKFK(name, position, size):
    j=mel.eval('curve -d 1 -p 0 0 0 -p 0 0 -2 -p -1 0 -3 -p 0 0 -4 -p 1 0 -3 -p 0 0 -2 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 ;')
    cmds.delete(j,ch=True)
    k=cmds.rename(name)
    cmds.scale(size, size, size)
    i=cmds.pointConstraint(position, k)
    # deletes constraint nad freezes transforms
    cmds.delete(i)
    cmds.makeIdentity(k, apply=True, t=1, r=1, s=1, n=1)
    
    cmds.addAttr(k, ln="IK_FK", at="double", min=0, max=10, dv=0,k=True, r=True, w=True, s=True )
    cmds.select(cl=1)
    pad=cmds.group(em=1, n='%s_pad' % k)
    cmds.parentConstraint(position, pad, mo=0)
    cmds.parent(k, pad)
    return k
