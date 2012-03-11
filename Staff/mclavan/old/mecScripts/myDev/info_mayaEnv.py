'''
Information on Maya's enviroment paths
info_mayaEnv.py

Description:
	- Different ways of access the different paths of Maya's enviroment.	

'''


# maya.env
# Base enviroment file
# File exists for each version of Maya
# Gets loaded up and runtime and will add to the existing system enviroment variables.

'''
Syntax

XBMLANGPATH == icons paths
MAYA_PLUG_IN_PATH == plug-in paths
PYTHONPATH == python scripts paths
MAYA_SCRIPT_PATH == mel scripts path

maya.env

PYTHONPATH = C:\firstPath; C:\secondPath


# This is old school no "".
# All the added path MUST be on one line seperated by ;
# These will be added to the existing system enviroment

'''


# Access and appending paths from within Pythons enviroment.
import os  # os module includes the environ dictionary

envPaths = os.environ
lines = [ "%s: %s" %(key, envPaths[key]) for key in envPaths.keys()]
print( "\n".join(lines) )




# Can this be updated in real time?
