'''
Michael Clavan
errors.py

Description:
	Code for generating different types of errors.


'''

'''
# raise a runtimeError
'''
def errorFunction():
	weFailed = True
	if( weFailed ):
		raise RuntimeError('error "memory error"')

errorFunction()

'''
# OpenMaya's warning and errors
'''
import maya.OpenMaya

#warning
maya.OpenMaya.MGlobal.displayWarning("warning message")

#error
maya.OpenMaya.MGlobal.displayError("error message")


'''
# python's sys.stderr.write command
'''
import sys
sys.stderr.write("Failed to get mesh vertex.\n")
sys.stderr.write("Failed to get attribute for node: %s.\n" % "myTestNode" )
sys.stderr.write("Error %d: fail to get attribute for node: %s\n" %(32,"myTestNode") )


'''
# Help area
# These are different ways a pulling up help for the user.
'''
# rampColorPort command help in the script editor
cmds.help( 'rampColorPort', language='python' )
# rampColorPort command help brought up in the web browser
cmds.help( 'rampColorPort', language='python', doc=True )

# Brings up the api help on a web page
cmds.showHelp("API/main.html", docs=True)
# Web page (python docs)
cmds.help(documentation=True, language='python')



