
import maya.cmds as cmds





def myLattice(dx=4, dy=4, dz=4):
	print("Lattice Created: %s" %dx )
	print("Lattice Created: %s" %dy )
	print("Lattice Created: %s" %dz )

def smooth(dv):
	print("Smooth: %s" %dv)	
	
def gui():
	cmds.window()
	cmds.columnLayout()
	cmds.button(label="Lattice", 
		c=(lambda *args: myLattice(dy=2, dz=6)))
	'''
	cmds.button(label="Button2",
		c=(lambda x: print("Hello")))
	'''
	cmds.button(label="Button2",
		c=(lambda *args: smooth(2)))
	cmds.showWindow()

	
	
