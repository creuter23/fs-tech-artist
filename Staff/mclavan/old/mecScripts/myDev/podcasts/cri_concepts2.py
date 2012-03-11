'''
Breaking down the Concept
concept2.py

Description:
	- This script covers the how to automate a character rigging 
		process through scripting.
		
How to Run:
import concept2
reload( concept2 )

'''

'''
Refinement
- Create a pad above the control icon.
'''

# Do it in the interface

# 1) User selected joint then icon
# 	- That means I'm going to have to get selected.
# 2) Create a group
# 	- Name it based on the control icon, include "_grp" added as a suffix.
# 3) Group and Control Icon is point and orient constraint to joint
#	- To match orientations.
# 3) Constraints are deleted
#	- Because they were only used to match orientations.
# 4) Control icon is parent to group to pad the control icon.


'''
Groups
cmds.group( name="groupName" )
- Flags
-empty  ( Nothing included in the group. )
-world  ( Group will be placed in the root. )
'''



'''
Returning Values
- Group returns the name of the group it created.
grp = cmds.group( name="grpName", world=True, empty=True )
- Constraints return the names of the constraint nodes it creates.
pc = cmds.pointConstraint( offset=[0,0,0], weight=1 )
oc = cmds.orientConstraint( offset=[0,0,0], weight=1 )

Using object names
selected = cmds.ls(sl=True)
grp = cmds.group( name="grpName", world=True, empty=True )

pc = cmds.pointConstraint(selected[0], grp, offset=[0,0,0], weight=1 )
oc = cmds.orientConstraint(selected[0], grp, offset=[0,0,0], weight=1 )

'''

# Selected items in the secene	
selection = cmds.ls(sl=True) # 0 == "joint", 1 == "icon"

# Group Created for padding (named after control icon)
grp = cmds.group( name=selected[0]+"_grp", empty=True, world=True )

# Matching Constraints
pointConstIcon = cmds.pointConstraint(selection[0], selection[1], offset=[0,0,0], weight=1 )
pointConstGrp = cmds.pointConstraint(selection[0], grp, offset=[0,0,0], weight=1 )
orientConstIcon = cmds.orientConstraint(selection[0], selection[1], offset=[0,0,0], weight=1 )
orientConstGrp = cmds.orientConstraint(selection[0], grp, offset=[0,0,0], weight=1 )

# Deleting unwanted constraints
cmds.delete( pointConstIcon, pointConstGrp, orientConstIcon, orientConstGrp )

'''
Parenting
cmds.parent( "obj1", "obj2", "parentObj" )
'''

def setupIconGrp(mode=0):
	'''
	This function will match the orientations from the first item selected to the second item selected.
	Object will move to match.
	'''
	# Selected items in the secene	
	selection = cmds.ls(sl=True) # 0 == "joint", 1 == "icon"
	
	# Group Created for padding (named after control icon)
	grp = cmds.group( name=selected[0]+"_grp", empty=True, world=True )

	# Matching Constraints
	pointConstIcon = cmds.pointConstraint(selection[0], selection[1], offset=[0,0,0], weight=1 )
	pointConstGrp = cmds.pointConstraint(selection[0], grp, offset=[0,0,0], weight=1 )
	orientConstIcon = cmds.orientConstraint(selection[0], selection[1], offset=[0,0,0], weight=1 )
	orientConstGrp = cmds.orientConstraint(selection[0], grp, offset=[0,0,0], weight=1 )
	
	# Deleting unwanted constraints
	cmds.delete( pointConstIcon, pointConstGrp, orientConstIcon, orientConstGrp )
	
	# Parenting & Matching control icon's orientations to the groups 
	cmds.parent( selection[1], grp )
	

'''
Constraint Option
- Give the user the option if they wish to constrain the control icon to the joint.
'''

'''
Giving the user the option to constrain the control icon to the joint.

# Modes:   0 == pointConstraint, 1 == orientConstraint,  2 == parentConstraint

mode = 0  

# Constraining joint to control icon
if( mode == 0 ):
	cmds.pointConstraint(selected[1], selected[0], offset=[0,0,0], weight=1 )

# mode == 1 is orient constraint
elif( mode == 1 ):
	cmds.orientConstraint(selected[1], selected[0], offset=[0,0,0], weight=1 )

# mode == 2 is parent constraint
else:
	cmds.parentConstraint(selected[1], selected[0], offset=[0,0,0], weight=1 )

'''


'''
Function
Argument & Return Statement
'''


def setupIconGrp(mode=0):
	'''
	This function will match the orientations from the first item selected to the second item selected.
	Object will move to match.
	'''
	# Selected items in the secene	
	selection = cmds.ls(sl=True) # 0 == "joint", 1 == "icon"
	
	# Group Created for padding (named after control icon)
	grp = cmds.group( name=selected[0]+"_grp", empty=True, world=True )

	# Matching Constraints
	pointConstIcon = cmds.pointConstraint(selection[0], selection[1], offset=[0,0,0], weight=1 )
	pointConstGrp = cmds.pointConstraint(selection[0], grp, offset=[0,0,0], weight=1 )
	orientConstGrp = cmds.orientConstraint(selection[0], selection[1], offset=[0,0,0], weight=1 )
	
	# Deleting unwanted constraints
	cmds.delete( pointConstIcon, pointConstGrp, orientConstGrp )
	
	# Parenting & Matching control icon's orientations to the groups 
	cmds.parent( selection[1], grp )
	cmds.makeIdentity( selected[1], apply=True, t=1, r=1, s=1, n=0 )
	
	# Constraining joint to control icon
	if( mode == 0 ):
		cmds.pointConstraint(selected[1], selected[0], offset=[0,0,0], weight=1 )
	
	# mode == 1 is orient constraint
	elif( mode == 1 ):
		cmds.orientConstraint(selected[1], selected[0], offset=[0,0,0], weight=1 )
	
	# mode == 2 is parent constraint
	else:
		cmds.parentConstraint(selected[1], selected[0], offset=[0,0,0], weight=1 )
		

'''
Return statements
Return statements allow the user to return values from a function back to the caller.


def createSphere( sphName ):
	sphCreated = cmds.sphere(name=sphName)
	# sphere command returns a list [Transform, History]
	# I only want to return the name of the sphere (Transform)
	return sphCreated[0]
	
# To use it
sphereName = createSphere( "ball" )
print(sphereName )
'''


# I'd like to return the name of the group created by this object.
def setupIconGrp2(mode=0):
	'''
	This function will match the orientations from the first item selected to the second item selected.
	Object will move to match.
	'''
	# Selected items in the secene	
	selection = cmds.ls(sl=True) # 0 == "joint", 1 == "icon"
	
	# Group Created for padding (named after control icon)
	grp = cmds.group( name=selected[0]+"_grp", empty=True, world=True )

	# Matching Constraints
	pointConstIcon = cmds.pointConstraint(selection[0], selection[1], offset=[0,0,0], weight=1 )
	pointConstGrp = cmds.pointConstraint(selection[0], grp, offset=[0,0,0], weight=1 )
	orientConstGrp = cmds.orientConstraint(selection[0], selection[1], offset=[0,0,0], weight=1 )
	
	# Deleting unwanted constraints
	cmds.delete( pointConstIcon, pointConstGrp, orientConstGrp )
	
	# Parenting & Matching control icon's orientations to the groups 
	cmds.parent( selection[1], grp )
	cmds.makeIdentity( selected[1], apply=True, t=1, r=1, s=1, n=0 )
	
	# Constraining joint to control icon
	if( mode == 0 ):
		cmds.pointConstraint(selected[1], selected[0], offset=[0,0,0], weight=1 )
	
	# mode == 1 is orient constraint
	elif( mode == 1 ):
		cmds.orientConstraint(selected[1], selected[0], offset=[0,0,0], weight=1 )
	
	# mode == 2 is parent constraint
	else:
		cmds.parentConstraint(selected[1], selected[0], offset=[0,0,0], weight=1 )

	# Returning the name of the group
	return grp
	
