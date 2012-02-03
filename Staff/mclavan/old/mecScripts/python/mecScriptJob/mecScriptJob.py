'''
Script Job Monitoring Station

Disc:
This script shows all the scriptJobs currently running in the scene.
Options for refreshing the list along will killing normal and protected 
	script jobs is offered through a menu.

How to use:

import mecScriptJob
mecScriptJob.gui()

'''
import maya.cmds as cmds
from callback import Callback

win = "mecSJWin"  
tsl = "mecSJList"
scriptName = __name__

def sjKillGUI():
	'''
	GUI guts
	'''
	global mainCol
	global tsl
	
	# mainCol = cmds.columnLayout( adjustableColumn=True )
	cmds.paneLayout()
	tsl = cmds.textScrollList( w=1200, h=180, ams=True,
		append=cmds.scriptJob(listJobs=True))
	'''
	cmds.rowColumnLayout( nc=3, cat=[[1, "both", 0],[2, "both", 0],[3, "both", 0]] )
	cmds.button(label="Refresh")
	cmds.button(label="Kill Normal")
	cmds.button(label="Kill Protected")	
	'''
	
def sjRefresh():
	'''
	Refresh Script Jobs
	'''	
	global tsl
	# Remove tsl elements.
	cmds.textScrollList(tsl, edit=True, ra=True)
	cmds.textScrollList(tsl, edit=True, append=cmds.scriptJob(listJobs=True))


	
def sjKill():
	'''
	Kill a scriptJob
	Argument:
		forceVal(int) == 1 means kill protected
	'''
	forceVal=0
	global tsl
	# Get textScrollList item to kill
	selectedTSL = cmds.textScrollList( tsl, q=True,  si=True)
	for selTSL in selectedTSL:
		sjSplit = selTSL.split(":")
		# kill scriptJob
		cmds.scriptJob( kill=int(sjSplit[0]), force=forceVal)
		# refresh the list
	sjRefresh()

def sjKillProtected():
	'''
	Kill a scriptJob
	Argument:
		forceVal(int) == 1 means kill protected
	'''
	forceVal=1
	global tsl
	# Get textScrollList item to kill
	selectedTSL = cmds.textScrollList( tsl, q=True,  si=True)
	for selTSL in selectedTSL:
		sjSplit = selTSL.split(":")
		# kill scriptJob
		cmds.scriptJob( kill=int(sjSplit[0]), force=forceVal)
		# refresh the list
	sjRefresh()
	
def gui():
	'''
	Generate scriptJob Win GUI.
	'''
	
	if( cmds.window( win, q=True, ex=True) ):
		cmds.deleteUI(win)
		
	cmds.window(win, title="Script Jobs Info", mb=True, w=300, h=200)
	
	cmds.menu(label = "ScriptJob Edit")
	cmds.menuItem( label = "Refresh List",
		c=Callback(sjRefresh))
	cmds.menuItem( divider=True )
	cmds.menuItem( label = "Kill Normal",
		c=Callback(sjKill))
	cmds.menuItem( label = "Kill Protected",
		c=Callback(sjKillProtected))
	sjKillGUI()
	
	cmds.showWindow(win)
	


"""
# Orginal function, must of been changed to keep this function alive inside another script it must of been rewriten.
def sjKill(forceVal=0):
	'''
	Kill a scriptJob
	Argument:
		forceVal(int) == 1 means kill protected
	'''
	forceVal=0
	global tsl
	# Get textScrollList item to kill
	selectedTSL = cmds.textScrollList( tsl, q=True,  si=True)
	for selTSL in selectedTSL:
		sjSplit = selTSL.split(":")
		# kill scriptJob
		cmds.scriptJob( kill=int(sjSplit[0]), force=forceVal)
		# refresh the list
	sjRefresh()
"""
	
	


