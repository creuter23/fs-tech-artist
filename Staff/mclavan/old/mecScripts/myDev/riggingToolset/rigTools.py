'''
Rigging Toolset

Description:

How to run

'''


import maya.cmds as cmds
import pymel.core as pm

win = "mecRigWin"
winWidth = 300
winHeight = 300


def selectDriver( *args ):
    cmds.select( driverAttr.split(".")[0], r=True )
    
    
def setupDriver( *args ):
    global driverAttr
    driverAttr = "%s.%s" %( cmds.ls(sl=True)[0], cmds.channelBox( "mainChannelBox", q=True, sma=True )[0] )
    cmds.text( driverText, e=1, label=driverAttr )
   
def selectDriven(*args):
    cmds.select( drivenAttrs, r=True )
       
def stampSDK( *args ):
    global drivenAttrs
    drivenAttrs = cmds.ls(sl=True)
    
    # Stamp SDK
    for sel in drivenAttrs:
        cmds.setDrivenKeyframe( "%s.%s" %(sel, cmds.channelBox( "mainChannelBox", q=True, sma=True )[0]), 
            cd=driverAttr)    
            
def gui():
	
	if( cmds.window( win, ex=True ) ):
		cmds.deleteUI(win)
	if( cmds.windowPref(win, ex=True) ):
		cmds.windowPref(win, r=True)
		
	cmds.window(win, title="Rigging Toolset", w=winWidth, h=winHeight)
	mainCol = cmds.columnLayout()
	
	primeGUI(mainCol)
	constGUI(mainCol)
	sdkToolGui(mainCol)
	
	cmds.showWindow(win)

def sdkToolGui(curParent):
	frm = cmds.formLayout( parent=curParent )

	btn1 = cmds.button( label="Driver Attr", w=75, c=setupDriver )

	global driverText
	driverText = cmds.text( label="Current Driver", h=20 )
	btn2 = cmds.button( label="Select Driver", c=selectDriver, w=75 )
	
	btn3 = cmds.button( label="Stamp SDK", c=stampSDK, w=75 )
	btn4 = cmds.button( label ="Select Driven", c=selectDriven, w=75 )
	
	# Positioning
	cmds.formLayout( frm, e=1, af=[[btn1, "left", 5],[btn1, "top", 5]] )
	cmds.formLayout( frm, e=1, af=[driverText, "top", 5],ac=[[driverText, "left", 10, btn1]])	
	cmds.formLayout( frm, e=1, af=[btn2, "top", 5], ac=[btn2, "left", 10, driverText])
	
	cmds.formLayout( frm, e=1, af=[btn3, "left", 5],ac=[btn3, "top", 3, btn1] )
	cmds.formLayout( frm, e=1, ac=[[btn4, "top", 3, btn1], [btn4, "left", 5, btn3]] )

	cmds.setParent(curParent)
	return frm	
	
def primeGUI(curParent):
	frm = cmds.formLayout( parent=curParent )
	btn1 = cmds.button( label="Prime Control", w=110,
		c=pm.Callback(primeOptions))
	global primeChoice
	primeChoice = cmds.radioButtonGrp( nrb=4, labelArray4=['Point', 'Orient', 'Parent', 'None'],
		label="", cw=[[1,5],[2,60],[3,60],[4,60],[5,60]], sl=4)

	cmds.formLayout( frm, e=1, af=[[btn1, "left", 5],[btn1, "top", 5]] )
	cmds.formLayout( frm, e=1, ac=[primeChoice, "left", 5, btn1], af=[primeChoice, "top", 5] )
	
	cmds.setParent(frm)
	return frm

def constGUI(curParent):

	frm = cmds.formLayout( parent=curParent )

	btn1 = cmds.button( label="Point", w=75,
		c=pm.Callback(const, 1))
	btn2 = cmds.button( label="Orient", w=75,
		c=pm.Callback(const, 2))	
	btn3 = cmds.button( label="Parent", w=75,
		c=pm.Callback(const, 3))
	global offsetChk
	offsetChk = cmds.checkBox( label="Offset", value=0, w=50 )	
	center = returnCenter([btn1, btn2, btn3, offsetChk], win )
	print(center)
	cmds.formLayout( frm, e=1, af=[[btn1, "left", 5],[btn1, "top", 5]])
	cmds.formLayout( frm, e=1, af=[btn2, "top", 5], ac=[btn2, "left", 3, btn1])
	cmds.formLayout( frm, e=1, af=[btn3, "top", 5], ac=[btn3, "left", 3, btn2])
	cmds.formLayout( frm, e=1, af=[offsetChk, "top", 5], ac=[offsetChk, "left", 3, btn3])
	
	cmds.setParent(frm)
	return frm

def returnCenter(controls, win):
	total = 0
	curWidth = cmds.window(win,q=1,w=1)
	for ctrl in controls:
		total += cmds.control( ctrl, q=1, w=1 )
	center = curWidth/2 - total	
	print("GUI Controls Total: %s Window W: %s Half: %s CtrlOffset: %s" %(total, curWidth, curWidth/2, (curWidth-total)/2))
	return center	
		
def const(constType):
	'''
	Work function for constraint interface
	'''
	offset = cmds.checkBox( offsetChk, q=1, value=1)
	if(constType==1):
		# PointConstraint
		cmds.pointConstraint( mo=offset )
	elif(constType==2):
		cmds.orientConstraint( mo=offset )
	elif(constType==3):
		cmds.parentConstraint( mo=offset )
		

def primeOptions():
	# Constraint Option
	const = cmds.radioButtonGrp( primeChoice, q=True, sl=True)
	
	selected = cmds.ls(sl=True)
	driver = selected[0]
	driven = selected[1]
	# selected[0] == joint
	# selected[1] == control	

	controls = primeControl( driver, driven )
	
	if( const == 1 ):
		# PointConstraint
		cmds.pointConstraint(driven, driver)
	elif( const == 2 ):
		# OrientConstraint
		cmds.orientConstraint(driven, driver)
	elif( const == 3 ):
		# Parent Constraint
		cmds.parentConstraint(driven, driver)

def primeControl(driver, driven):	
	'''
	# Priming a control
	
	Return driver, grp, driven
	'''
	
	# Group needs to be created
	# Name group after control icon that is going to be created.
	grpNamePieces = driven.split("_")
	if( len(grpNamePieces) > 1 ): 
	    grpNamePieces = grpNamePieces[0:-1]
	grpNamePieces.append("grp")
	grpName = "_".join(grpNamePieces)
	grp = cmds.group( name=grpName, em=True, world=True )
	pc = cmds.pointConstraint( driver, grp )
	oc = cmds.orientConstraint( driver, grp )
	cmds.delete(pc, oc)
	# Option to snap control to position.
	pc = cmds.pointConstraint( driver, driven )
	
	cmds.delete( pc )
	cmds.parent( driven, grp )
	cmds.makeIdentity( apply=True, t=1, r=1, s=1, n=0 )
	
	# Position option to constrain driver to driven
	# Options: Point, Orient, Parent, and None

	return [driver, grp, driven]
