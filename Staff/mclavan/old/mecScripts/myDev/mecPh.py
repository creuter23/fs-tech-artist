'''
Connecting with Photoshop
Create a list of active photoshop programs.

'''
import maya.cmds as cmds
'''
import win32com.client
psApp = win32com.client.Dispatch("Photoshop.Application")
'''
win = "mecPhWin"
winWidth = 200
winHeight = 300

def gui():
	'''
	Generates the gui for the script.
	'''
	if( cmds.window(win, q=True, ex=True)):
		cmds.deleteUI(win)
		
	if( cmds.windowPref(win, q=True, ex=True) ):
		# cmds.windowPref(win, r=True, wh=[winWidth, winHeight])
		cmds.windowPref(win, r=True)
		
	cmds.window(win, title="Photoshop Tool", w=winWidth, h=winHeight)	
	cmds.columnLayout()
	
	cmds.textScrollList("mecPhTSL", w=winWidth-15, h=150)

	cmds.button(label="Refresh", w=winWidth-15,
		c="mecPh.phAddTSL()")
	cmds.rowColumnLayout( nc=2, 
		cw=[[1,80],[2,105]])
	cmds.button(label="Close All",
		c="mecPh.phCloseAll()")
	cmds.button(label="Close Selected",
		c="mecPh.phCloseSel()")
	cmds.showWindow(win)
	
# Function needed to add the open files into the textScrollList.
def phAddTSL():
	# Grab all the items that are current open in photoshop
	psCount = psApp.Documents.count
	i = 0
	while( i < psCount ):
		# Add them to the textScrollList
		cmds.textScrollList("mecPhTSL", e=True, append=psApp.Documents[i].name)
		i = i + 1

def phCloseAll():
	'''
	This function closes all the open files in photoshop.
	'''
	counter = psApp.Documents.count
	i = 0
	while( psApp.Documents.count ):
	    psApp.Documents[i].Close(2)
	    i = i+1	

# Function needed to close selected files
def phCloseSel():
	'''
	Close all the selected files represented in the textScrollList
	'''
	
	# Obtain all the items from the textScrollList
	tslItems = cmds.textScrollList("mecPhTSL", q=True, ai=True)
	
	# Check to see if there is anything selected in the textScrollList
	if(tslItems):
		phClose(tslItems)
	
def phClose( phFiles ):
	'''
	Close the chosen photoshop files.
	phFiles -> A list of strings contain each file you wish to close in photoshop.
	'''	
	for phFile in phFiles:
		i = phFindIndex(phFile)
		# Close with out saving.
		psApp.Documents[i].close(2)
	

# A function might be nessary to find which index number it is in photoshop.
def phFindIndex( phFile ):
	'''
	This function will return the file index for the name.
	Also if there isn't a match then the function returns 0.
	'''
	# how many file are currently open in photoshop
	psCount = psApp.Documents.count

	i = 0
	while( i < psCount):
		if( phFile == psApp.Documents[i].name ):
			return i
		i = i + 1
		
	return 0

'''
import win32com.client
psApp = win32com.client.Dispatch("Photoshop.Application")


# Document counts
counter = psApp.Documents.count
i = 0
while( psApp.Documents.count ):
    psApp.Documents[i].Close(2)
    i = i+1
'''
	
