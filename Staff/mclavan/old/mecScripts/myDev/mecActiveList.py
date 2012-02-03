'''
mecActiveList.py

How to run:

import mecActiveList
mecActiveList.gui()

'''
import maya.cmds as cmds

def refresh(*args):
	cmds.textScrollList("mecTSL", e=True, ra=True)
	cmds.textScrollList("mecTSL", e=True, append=cmds.ls(sl=True))

	
def liveOff(*args):
	cmds.scriptJob( kill=sjNum )
	
	
def live(*args):
	# scriptJob -event "SelectionChanged" "refresh";	
	# cmds.scriptJob( event=["SelectionChanged", "mecActiveList.refresh()"] )
	global sjNum
	sjNum = cmds.scriptJob( event=["SelectionChanged", "mecActiveList.refresh()"], 
		p="mecActiveWin")

def update(*args):
	allItems = cmds.textScrollList("mecTSL", q=True, ai=True)
	cmds.select( allItems, r=True )
	
def moveTop(*args):
	allItems = cmds.textScrollList("mecTSL", q=True, ai=True)
	selItems = cmds.textScrollList("mecTSL", q=True, si=True)
	
	for sel in selItems:
		allItems.remove(sel)
	i = len(selItems)
	while(i != 0):
		print(selItems[i-1])
		allItems.insert(0,selItems[i-1])
		i = i-1	
	
	print(allItems)
	
	cmds.textScrollList("mecTSL", e=True, ra=True)
	cmds.textScrollList("mecTSL", e=True, append=allItems)
	update()
	
	
def moveBottom(*args):	
	allItems = cmds.textScrollList("mecTSL", q=True, ai=True)
	selItems = cmds.textScrollList("mecTSL", q=True, si=True)
	
	for sel in selItems:
		allItems.remove(sel)
		allItems.append(sel)
	
	print(allItems)
	
	cmds.textScrollList("mecTSL", e=True, ra=True)
	cmds.textScrollList("mecTSL", e=True, append=allItems)
	update()
		
def moveUp(*args):
	allItems = cmds.textScrollList("mecTSL", q=True, ai=True)
	selItems = cmds.textScrollList("mecTSL", q=True, si=True)

	# Get the current position
	selIndex = cmds.textScrollList( "mecTSL", q=True, selectIndexedItem=True)
	
	for i, sel in enumerate( selItems ):
		print("Test")
		if( selIndex[i] == 1 ):
			print("Break Out")
			break
		allItems.remove(sel)	
		allItems.insert(selIndex[i]-2, sel)

	cmds.textScrollList("mecTSL", e=True, ra=True)
	cmds.textScrollList("mecTSL", e=True, append=allItems)
	
	update()
	for sel in selItems:
		print("Here is: %s" %sel)
		cmds.textScrollList("mecTSL", e=True, si=sel)
	
def moveDown(*args):
	allItems = cmds.textScrollList("mecTSL", q=True, ai=True)
	selItems = cmds.textScrollList("mecTSL", q=True, si=True)

	# Get the current position
	selIndex = cmds.textScrollList( "mecTSL", q=True, selectIndexedItem=True)
	
	i = len(selItems)-1
	while(i >= 0):
		if( selIndex[-1] == len(allItems) ):
			break
		print(selItems[i])
		# allItems.insert(0,selItems[i-1])
		
		allItems.remove(selItems[i])	
		allItems.insert(selIndex[i], selItems[i])
		i = i-1	
	
	
	print(allItems)
	
	cmds.textScrollList("mecTSL", e=True, ra=True)
	cmds.textScrollList("mecTSL", e=True, append=allItems)
	
	update()
	for sel in selItems:
		print("Here is: %s" %sel)
		cmds.textScrollList("mecTSL", e=True, si=sel)	
	
	
def remItem(*args):
	selItems = cmds.textScrollList( "mecTSL", q=True, si=True)
	for sel in selItems:
		cmds.textScrollList("mecTSL", e=True, ri=sel)
	update()
	

win = "mecActiveWin"

def gui():
	if( cmds.window( win, q=True, ex=True) ):
		cmds.deleteUI(win)
		
	cmds.window(win, title="Active List Script")
	mainCol = cmds.columnLayout()
	cmds.text(l="", h=3)
	cmds.rowColumnLayout( nc=2, cw=[[1,165],[2,25]], co=[1,"both",5] )
	cmds.textScrollList("mecTSL", w=170, h=200, ams=True,
		append=cmds.ls(sl=True) )
	cmds.columnLayout()
	'''
	cmds.button( label="U", w=25, h=40 )
	cmds.button( label="U", w=25, h=40 )
	cmds.button( label="R", w=25, h=40 )
	cmds.button( label="D", w=25, h=40 )
	cmds.button( label="D", w=25, h=40 )
	'''
	cmds.symbolButton( i="top.xpm", w=25, h=40, c=moveTop )
	cmds.symbolButton( i="up.xpm", w=25, h=40, c=moveUp)
	cmds.symbolButton( i="del.xpm", w=25, h=40, c=remItem )
	cmds.symbolButton( i="down.xpm", w=25, h=40, c=moveDown )
	cmds.symbolButton( i="bottom.xpm", w=25, h=40, c=moveBottom )
	
	cmds.setParent( mainCol )
	
	cmds.text(l="", h=5 )
	
	cmds.rowColumnLayout( nc=2, cw=[[1,95],[2,100]], co=[[1,"left",5],[2,"right",5]])
	cmds.symbolCheckBox( w=100, h=30, image="live.xpm", 
		oni="live.xpm", ofi="pause.xpm",
		onc=live, ofc=liveOff, v=1)
	# cmds.button(label="Live", h=30, w=95)
	# cmds.button(label="Refresh", c=refresh)
	cmds.symbolButton( i="refreshAL.xpm", w=100, h=30, c=refresh )
	
	cmds.setParent(mainCol)
	

	cmds.showWindow()
	live()


