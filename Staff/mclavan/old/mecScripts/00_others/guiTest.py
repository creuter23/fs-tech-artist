
import maya.cmds as cmds

def gui():
	win = "myTestWin"
	
	if(cmds.window(win, q=True, ex=True)):
		cmds.deleteUI(win)
		
	cmds.window(win, t="Hello", w=300, h=300)
	cmds.columnLayout()
	cmds.button(label="Hit me", command=myCallback)


	
	cmds.showWindow(win)

def myCallback():
    print "This is from a Python callback"


