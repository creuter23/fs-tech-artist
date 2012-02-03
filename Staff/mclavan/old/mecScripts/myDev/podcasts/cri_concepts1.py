'''
Breaking down the Concept
concept1.py

Description:
	- This script covers the how to automate a character rigging 
		process through scripting.
		
How to Run:
import concept1
reload( concept1 )

'''


'''
Idea:
Automate setting up a control icon.
'''

# I'd like to be able to match a joints orientation onto a control icon, by 
# selecting the joint and then the control icon.

'''
Break down the concept.
- Do it in the interface, watch the script editor and take notes on the process.
'''

# Write comments for each step.

# 1) User selected joint then icon
# 	- That means I'm going to have to get selected.
# 2) Control is point and orient constraint to joint
#	- To match orientations
# 3) Constraints are deleted
#	- Because they were only used to match orientations.


'''
Script Editor
Watch what the script editor is doing.
'''

'''
# Selection
select -r lt_arm_elbow_bj ;
select -tgl controlIcon ;

# 1st == joint, 2nd == control icon
selection = cmds.ls(sl=True)  # Selection order is preserved
'''


'''
# constraints

doCreatePointConstraintArgList 1 { "0","0","0","0","0","0","0","1","","1" };
pointConstraint -offset 0 0 0 -weight 1;
// Result: controlIcon_pointConstraint1 // 
doCreateOrientConstraintArgList 1 { "0","0","0","0","0","0","0","1","","1" };
orientConstraint -offset 0 0 0 -weight 1;
// Result: controlIcon_orientConstraint1 // 


# There isn't an effected object, will work based on selection!
cmds.pointConstraint( offset=[0,0,0], weight=1 )
cmds.orientConstraint( offset=[0,0,0], weight=1 )

# The return the name of the constrains.
pointConst = cmds.pointConstraint( offset=[0,0,0], weight=1 )
orientConst = cmds.orientConstraint( offset=[0,0,0], weight=1 )
'''

'''
# Delete Constraints
# I need a command to delete the constraint on the control icon
# delete command
cmds.delete(pointConst, orientConst)
'''

'''
Constrain the joint to the control icon
# Choosing orient for now.
# cmds.orientConstraint( offset[0,0,0], weight=1 )
# pc = cmds.pointConstraint([targets], obj, offset=[0,0,0], weight=1 )
# cmds.orientConstraint("controlIcon", "joint", offset=[0,0,0], weight=1 )

cmds.orientConstraint(selected[1], selected[0], offset=[0,0,0], weight=1 )
'''



'''
Creating a function.
'''

def setupIcon():
	'''
	This function will match the orientations from the first item selected to the second item selected.
	Object will move to match.
	'''
	selection = cmds.ls(sl=True) # 0 == "joint", 1 == "icon"
	pointConst = cmds.pointConstraint( offset=[0,0,0], weight=1 )
	orientConst = cmds.orientConstraint( offset=[0,0,0], weight=1 )
	cmds.delete( pointConst, orientConst )
	cmds.orientConstraint(selected[1], selected[0], offset=[0,0,0], weight=1 )
	
	
	
	
