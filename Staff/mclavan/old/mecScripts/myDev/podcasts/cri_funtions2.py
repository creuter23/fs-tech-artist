'''
Functions
Arguments and Return Statements
functions2.py

Description:
	- This script covers how to take advantage of functions by using 
		arguments and return statements.
	
How to Run:

import functions2
reload( functions2 )

'''

'''
Functions
Arguments
'''

def createSphere():
	cmds.sphere()

# To use
# createSphere()

def createSphere( sphName ):
	cmds.sphere(name=sphName)

# To use
# createSphere( "ball" )

def createSphere( sphName, position )
	cmds.sphere(name=sphName)
	cmds.xform( translate=position )

# To use
# createSphere( "ball", [0,3,0] )


'''
Default Values
'''
def createSphere( sphName="ball", radius=1, position=[0,0,0] )
	cmds.sphere(name=sphName)
	cmds.xform( translate=position )


# To use
# createSphere( "ball", 3, [0,3,0] )
# createSphere( )
# createSphere(sphName="beachBall", radius=3, position=[0,3,0] )
# createSphere( radius=3 )



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


