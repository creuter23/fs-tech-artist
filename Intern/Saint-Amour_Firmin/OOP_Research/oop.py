'''
test to understand OOP

my version of the critterCareTakerProgram

'''

import maya.cmds as cmds 
class Kidz(object):
    def __init__(self,size, name, mom):
       print('%s you now have a baby' % mom.name)
       self.name = name
       self.size= size
       
       
    # creates a cube a parents it under it's parent
    def birth(self, mom):
       x=2
       cmds.polyCube(n=self.name, w=0, h=0, d=0)
       cmds.scale(self.size-x,self.size-x,self.size-x, absolute = True)       
       p=cmds.pointConstraint(mom, self.name)
       cmds.delete(p)
       cmds.parent(self.name, mom)
   
    # returns the cube to ( 0 , 0 , 0 )
    def origin(self):
       cmds.setAttr('%s.translateX' % self.name, 0)
       cmds.setAttr('%s.translateY' % self.name, 0)
       cmds.setAttr('%s.translateZ' % self.name, 0)
   
    # increases the size of the cube
    def growUp(self):
       x=4
       cmds.select(self.name)       
       cmds.scale(self.size+x, self.size+x, self.size+x ,absolute = True)   
   
    # unparents the cube from its 'mom'  
    def free(self):
       cmds.parent(self.name, world = True)
    
    # deletes the cube
    def death():
       cmds.delete(self.name)
    
    # the cube gets pointConstrained back to the parent, and get parent to its parent, aslo shrinks down  
    def returnHome(self, mom):
       x=4
       p=cmds.pointConstraint(mom.name, self.name)
       cmds.delete(p)
       cmds.parent(self.name, mom.name)
       cmds.scale(-4,-4,-4, absolute = True)
    
    # a method to move the cube .walk() takes two args the axis and the value, 1 = x , 2 = y , 3 = z   
    def walk(self, axis,steps):
        self.axis=axis
        self.steps=steps
        a1=cmds.getAttr('%s.translateX' % self.name )
        a2=cmds.getAttr('%s.translateY' % self.name )
        a3=cmds.getAttr('%s.translateZ' % self.name )
      
        if self.axis == 3:       
           old=cmds.getAttr('%s.translateZ' % self.name )
           cmds.move( a1, a2, old+steps, self.name , localSpace = True, absolute = True, relative = True)
       
        if self.axis == 2:       
           old=cmds.getAttr('%s.translateY' % self.name )
           cmds.move( a1, old+steps ,a3, self.name , localSpace = True, absolute = True,  relative = True)
       
        if self.axis == 1:       
           old=cmds.getAttr('%s.translateX' % self.name )
           cmds.move( old+steps, a2 ,a3, self.name , localSpace = True, absolute = True, relative = True)
       
        else:
            print('no way Jose')


class Cubez(object):
    def __init__(self, name, size):
       self.name = name
       self.size = size
       print('you made a cube name %s just use the .creation funciton to see it' % self.name)
    
    # returns the cube to ( 0 , 0 , 0 )
    def origin(self):
       cmds.setAttr('%s.translateX' % self.name, 0)
       cmds.setAttr('%s.translateY' % self.name, 0)
       cmds.setAttr('%s.translateZ' % self.name, 0)
     
    #creates the cube   
    def creation(self):
       cmds.polyCube(n=self.name, w=self.size, h=self.size, d=self.size)
    
    # this method will invoke the child from the Kidz class birth method   
    def reproduce(self, child):
       child.birth(self.name)
    
    # this deletes the cube
    def death(self):
       cmds.delete(self.name)
    
    # a method to move the cube .walk() takes two args the axis and the value, 1 = x , 2 = y , 3 = z 
    def walk(self, axis,steps):
       self.axis=axis
       self.steps=steps
       a1=cmds.getAttr('%s.translateX' % self.name )
       a2=cmds.getAttr('%s.translateY' % self.name )
       a3=cmds.getAttr('%s.translateZ' % self.name )
      
       if self.axis == 3:       
           old=cmds.getAttr('%s.translateZ' % self.name )
           cmds.move( a1, a2, old+steps, self.name , absolute = True, objectSpace = True)
       
       if self.axis == 2:       
           old=cmds.getAttr('%s.translateY' % self.name )
           cmds.move( a1, old+steps ,a3, self.name , absolute = True, objectSpace = True)
       
       if self.axis == 1:       
           old=cmds.getAttr('%s.translateX' % self.name )
           cmds.move( old+steps, a2 ,a3, self.name , absolute = True, objectSpace = True)
       
       else: 
           print('no way Jose')
           
 
       
       
       