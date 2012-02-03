'''
Generic Rigging Toolset
'''
import maya.cmds as cmds

# Constraints
def pc(*args):
	'''
	Point Consraint
	pointConstraint -offset 0 0 0 -weight 1;
	'''
	cmds.pointConstraint( offset=[0,0,0], weight=1 )
	
	
def pcOption(*args):
	'''
	Point Constaint Options
	PointConstraintOptions;
	'''
	cmds.PointConstraintOptions();
	
def oc(*args):
	'''
	Orient Consraint
	pointConstraint -offset 0 0 0 -weight 1;
	'''
	cmds.orientConstraint( offset=[0,0,0], weight=1 )
	
	
def ocOption(*args):
	'''
	Orient Constaint Options
	PointConstraintOptions;
	'''
	cmds.OrientConstraintOptions();

def parC(*args):
	'''
	Parent Consraint
	pointConstraint -offset 0 0 0 -weight 1;
	'''
	cmds.parentConstraint( offset=[0,0,0], weight=1 )
	
	
def parCOption(*args):
	'''
	Parent Constaint Options
	PointConstraintOptions;
	'''
	cmds.ParentConstraintOptions();	
	
# Low Rez Rig
# Seperate
def sep(*args):
	'''
	Seperates polygon objects
	'''
	cmds.SeparatePolygon()

# Fill Hole
def fillHole(*args):
	'''
	Fills the hole of the selected geometry.
	'''
	cmds.FillHole(*args)

# Smooth
def smoothGeo(*args):
	'''
	Smooths the selected geometry
	'''
	# Get Division value.
	myDiv = cmds.intField("mecRigDiv", q=True, value=True)
	
	cmds.polySmooth( dv=myDiv )
	
# Get Edge Loop
def edgeLoop(*args):
	'''
	Get edge loop.
	'''
	cmds.SelectEdgeLoop()
	
def convFaces(*args):
	'''
	Convert to Faces
	'''
	cmds.ConvertSelectionToFaces()

# Delete History & Freeze Transforms
def delHist(*args):
	'''
	Delete's History
	'''
	cmds.delete(ch=1)
	
def freezeT(*args):
	'''
	Freezes Transforms
	'''
	cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)

def delFrez(*args):
	'''
	Deletes history and freezes transforms
	'''
	cmds.delete(ch=1)
	cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)

def centerPivot(*args):
	'''
	Center's Pivot on selected objects.
	'''
	cmds.xform(cp=True)
	
# Grab Selected (Binding Tool)
holdSelected = ""
def lockHold(*args):
	'''
	Currently selected objects are recoreded in a global variable in the script.
	'''
	global holdSelected
	holdSelected = cmds.ls(sl=True)
	
def selectHeld(*args):
	'''
	Select objects that are contained in the global variable held in the script
	'''
	cmds.select( holdSelected, r=True )
	
win = "mecRigWin"
def gui():
	'''
	Generates the GUI
	'''
	
	if( cmds.window(win, q=True, ex=True) ):
		cmds.deleteUI(win)
	
	cmds.window(win, t="Rigging Gen Tools", w=150, h=300)
	cmds.columnLayout("mecRigMC")
	
	
	genGUI()
	conGUI()
	lowRezGUI()
	
	
	
	cmds.showWindow(win)

def conGUI(guiParent="mecRigMC"):
	# Constraints
	cmds.frameLayout(label="Constraints", w=205, cll=True )
	cmds.rowColumnLayout( nc=2, cw=[[1,125],[2,75]])
	cmds.button( label="Point Contraint", w=125,
		c=pc )
	cmds.button( label="Option", w=75,
		c=pcOption )
	cmds.button( label="Orient Contraint", w=125,
		c=oc )
	cmds.button( label="Option", w=75,
		c=ocOption )
	cmds.button( label="Parent Contraint", w=125,
		c=parC )
	cmds.button( label="Option", w=75,
		c=parCOption )
	cmds.setParent(guiParent)

def lowRezGUI(guiParent="mecRigMC"):	
	# Low Rez Tools
	cmds.frameLayout(label="Low Rez Tools", w=205, cll=True )
	cmds.columnLayout()
	cmds.button( l="Seperate", w=200,
		c=sep )
	cmds.rowColumnLayout(nc=2, cw=[[2,100],[2,100]])
	cmds.button( l="Get EdgeLoop", w=100,
		c=edgeLoop )
	cmds.button( l="conToFace", w=100,
		c=convFaces )
	cmds.setParent("..")
	
	cmds.button( l="Fill Hole", w=200,
		c=fillHole )
	cmds.rowColumnLayout( nc=2, cw=[[1,150], [2,50]])
	cmds.button( l="Smooth Poly", w=150,
		c=smoothGeo )
	cmds.intField( "mecRigDiv", v=1, min=0, max=4 )
	cmds.setParent("..")
	
	cmds.setParent(guiParent)
	
def genGUI(guiParent="mecRigMC"):
	cmds.frameLayout( label="Generic Rigging Tools", w=205, cll=True )
	cmds.columnLayout()
	cmds.rowColumnLayout(nc=2, cw=[[1,100],[2,100]])
	cmds.button("Freeze Transforms", w=100,
		c=freezeT )
		
	cmds.button("Del Hist", w=100,
		c=delHist )
	cmds.setParent("..")
	
	cmds.button("Del Hist/Freeze Trans", w=200,
		c=delFrez )
	cmds.button("Center Pivot", w=200,
		c=centerPivot)
	cmds.rowColumnLayout(nc=2, cw=[])
	cmds.button(l="Select", w=125,
		c=selectHeld )
	cmds.button(l="setSel", w=75,
		c=lockHold )
	cmds.setParent(guiParent)
