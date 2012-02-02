'''
--------------------------------------------------------------------------------
///////////////////////////// ceb_quickSdkGUI_v2.py ////////////////////////////
--------------------------------------------------------------------------------

Title: Quick SDK Creator

by: Craig Buchanan

How to Run:
	
import ceb_quickSdkGUI_v2
reload(ceb_quickSdkGUI_v2)
ceb_quickSdkGUI_v2.guiCreate()

	load the required information into the textFields by selecting an 
	object in the scene and an attribute in the channel box, then click the
	"Load Selected" buttons. Do this for both the driver an driven sections,
	then select the number of values you wish to keyframe. This decides how 
	many SDKs to create with "1" only keyframing from the "Default" field 
	and any above that from the other fields.

--------------------------------------------------------------------------------
////////////////////////////////////////////////////////////////////////////////
--------------------------------------------------------------------------------

'''

import maya.cmds as cmds

# create variables to use in the script
winName = "quickSdkGUI_v2"
scriptName = __name__


# define the GUI creation function
def guiCreate():
	
	
	# if the window exists, delete it
	if ( cmds.window( winName, ex=True ) ):
		cmds.deleteUI( winName )
		
	width = 430
	
	# create the window
	cmds.window( winName, w=width, h=480 )
	
	
	
	# create columnLayout as main layout
	cmds.formLayout( 'mainForm' )
	
	# create a frameLayout to encapsulate and label the window elements
	cmds.frameLayout('mainFrame', label="Quick SDK", borderStyle='etchedIn',
		w=width-10 )
	
	# create columnLayout as main layout
	cmds.formLayout( 'subForm', w=width-20, h=300 )
	
	
	
	# create a frameLayout to encapsulate and label the window elements
	drvrFr = cmds.frameLayout('drvrFrame', label="Driver:", 
		borderStyle='etchedIn')
		
		
		
	# create variable for the textField widths
	tFld1W = 120
	tFld2W = 60
	tFld3W = 80
	
	cmds.columnLayout()
	
	cmds.rowLayout( nc=3, cw3= (tFld1W, tFld2W, tFld3W) )
	
	# create GUI elements for Driver
	cmds.text( 'nameTxt', l="Name:", w=50 )
	cmds.text( 'attrTxt', l="Attr:", w=50 )
	blankTxt1 = cmds.text( l=" ")
	
	cmds.setParent( ".." )
	
	cmds.rowLayout( nc=3, cw3= (tFld1W, tFld2W, tFld3W) )
	
	drvr1 = cmds.textField( 'drvrNameFld', w=tFld1W )
	drvr2 = cmds.textField( 'drvrAttrFld', w=tFld2W )
	cmds.button( 'drvrBtn', label="Load Selected", w=tFld3W,
		c=scriptName + ".loadSel()" )
		
	cmds.setParent( ".." )
	
	cmds.setParent( ".." )
	cmds.setParent( ".." )
	
	
	# create a frameLayout to encapsulate and label the window elements
	drvnFr = cmds.frameLayout('drvnFrame', label="Driven:", 
		borderStyle='etchedIn' )
		
	cmds.columnLayout()
	
	# create driven textScrollList
	cmds.textScrollList( 'drvnTSL', ams=True, h=100, selectCommand=scriptName + ".changeAnim2('drvnTSL','keyOutline')" )
	
	
	tslBtnW1 = 50
	tslBtnW2 = 70

	
	cmds.rowLayout( nc=3, cw3= (tslBtnW1, tslBtnW2, tslBtnW2) )
	
	cmds.button( 'addBtn', label="Add", w=tslBtnW1,
		c=scriptName + ".addObj('drvnTSL')" )
	cmds.button( 'remAllBtn', label="Remove All", w=tslBtnW2,
		c=scriptName + ".clearAll('drvnTSL')" )
	cmds.button( 'remSelBtn', label="Remove Sel", w=tslBtnW2,
		c=scriptName + ".clearSel('drvnTSL')" )
		
	cmds.setParent( ".." )
	
	cmds.setParent( ".." )
	cmds.setParent( ".." )
	
	
	# create a frameLayout to encapsulate and label the window elements
	valFr = cmds.frameLayout('valFrame', label="Values:", 
		borderStyle='etchedIn' )
	
		
	cmds.columnLayout()
	
	fldVal1=80
	fldVal2=40
	
	cmds.rowLayout(nc=3, cw3=( fldVal1, fldVal2, fldVal2 ) )
	
	blankTxt2 = cmds.text( l=" ")
	cmds.text( 'drvrFldTxt', l="Driver:", w=fldVal2 )
	cmds.text( 'drvnFldTxt', l="Driven:", w=fldVal2 )
	
	cmds.setParent( ".." )
	
	flt1 = cmds.floatFieldGrp( 'fld1Grp', nf=2, label='1 (Default):', value1=0.0, 
		value2=0.0, pre=2, cw3=( fldVal1, fldVal2, fldVal2 ) )
	flt2 = cmds.floatFieldGrp( 'fld2Grp', nf=2, label='2:', value1=0.0, 
		value2=0.0, pre=2, cw3=( fldVal1, fldVal2, fldVal2 ) )
	flt3 = cmds.floatFieldGrp( 'fld3Grp', nf=2, label='3:', value1=0.0, 
		value2=0.0, pre=2, cw3=( fldVal1, fldVal2, fldVal2 ) )
	flt4 = cmds.floatFieldGrp( 'fld4Grp', nf=2, label='4:', value1=0.0, 
		value2=0.0, pre=2, cw3=( fldVal1, fldVal2, fldVal2 ) )
	flt5 = cmds.floatFieldGrp( 'fld5Grp', nf=2, label='5:', value1=0.0, 
		value2=0.0, pre=2, cw3=( fldVal1, fldVal2, fldVal2 ) )
	
	
	val1 = 50
	val2 = 80
	
	
	cmds.rowLayout(nc=2, cw2=( val1, val2 ) )
	
	# create optionMenu to determine # of SDKs to perform
	cmds.optionMenu( 'sdkOpt', w=val1 )
	cmds.menuItem( label='1' )
	cmds.menuItem( label='2' )
	cmds.menuItem( label='3' )
	cmds.menuItem( label='4' )
	cmds.menuItem( label='5' )
	
	#fill = " , "
	#passSdk = ".makeSdk( " + flt1 + fill + flt2 + fill + flt3 + fill + flt4 + fill + flt5 + " )"
	
	# create button to run sdk function
	cmds.button( 'sdkBtn', l="Create SDK", w=val2, c=scriptName + ".makeSdk( 'fld1Grp', 'fld2Grp', 'fld3Grp', 'fld4Grp', 'fld5Grp' )" )
	
		
	cmds.setParent( ".." )
	
	cmds.setParent( ".." )
	
	cmds.setParent( ".." )
	
	
	
	# create a frameLayout to encapsulate and label the window elements
	animCvFr = cmds.frameLayout('animCrvFrame', label="Animation Curves:", 
		borderStyle='etchedIn', h=150 )
	
	cmds.columnLayout()
	
	# create driven textScrollList
	animTSL = cmds.textScrollList( 'animTSL', h=100, selectCommand=scriptName + ".changeAnim('animTSL','keyOutline')" )
	
	
	cmds.rowLayout( nc=3, cw3= (tslBtnW1, tslBtnW2, tslBtnW2) )
	
	cmds.button( 'addBtn2', label="Add", w=tslBtnW1,
		c=scriptName + ".addCrv('animTSL')" )
	cmds.button( 'remAllBtn2', label="Remove All", w=tslBtnW2,
		c=scriptName + ".clearAll('animTSL')" )
	cmds.button( 'remSelBtn2', label="Remove Sel", w=tslBtnW2,
		c=scriptName + ".clearSel('animTSL')" )
		
	cmds.setParent( ".." )
	
	cmds.setParent( ".." )
	cmds.setParent( ".." )
	
	
	
	# create a frameLayout to encapsulate and label the window elements
	keyFr = cmds.frameLayout('keyOutFrame', label="Driven Key Values:", 
		borderStyle='etchedIn', collapsable=True, h=150 )
	
	cmds.formLayout( 'keyForm' )
	#cmds.columnLayout()
	
	keyOut = cmds.keyframeOutliner( 'keyOutline', dsp="narrow", 
		animCurve='animCurve1' )	
		
	cmds.setParent( ".." )
	
	cmds.setParent( ".." )
	
	
	
	offVal = 5
	
	
	# edit the main formLayout
	cmds.formLayout( 'mainForm', e=True,
		
		af=[ ( 'mainFrame', "left", 5),
		('mainFrame', "top", 5) ] )
	
	
	
	# edit the sub formLayout
	cmds.formLayout( 'subForm', e=True, 
		
		af=[ (drvrFr, "left", 5),
		(drvrFr, "top", 5) ],
		
		ac=[ (drvnFr, "top", 5, drvrFr),
		(valFr, "left", 5, drvnFr),
		(animCvFr, "top", 5, drvnFr),
		(keyFr, "top", 5, animCvFr) ],
		
		aoc=[ (drvnFr, "left", 0, drvrFr),
		(valFr, "top", 0, drvnFr),
		(keyFr, "left", 0, drvnFr),
		(keyFr, "right", 0, valFr),
		(animCvFr, "left", 0, drvrFr) ] )
	
	
	# edit the keyOutline formLayout
	cmds.formLayout( 'keyForm', e=True, 
	
		af=[ (keyOut, 'top', 0), 
		(keyOut, 'left', 0), 
		(keyOut, 'bottom', 0), 
		(keyOut, 'right', 0) ] )
	
	
	# show the window
	cmds.showWindow(winName)
	




# create function to load selected objects or attributes into textFields
def loadSel():
	
		
	# list first selected item into variable
	selItem = cmds.ls( sl=True )
	
	# list first selected attribute into variable
	selAttr = cmds.channelBox( 'mainChannelBox', q=True, sma=True )
	
	# edit the Driver name textField with first selection
	cmds.textField( 'drvrNameFld', e=True, tx=selItem[0] )
	
	# edit the Driver attr textField with first selection
	cmds.textField( 'drvrAttrFld', e=True, tx=selAttr[0] )	

	'''
	# No selection: 
	# IndexError: list index out of range # 

	# check to see if selection is blank and warn user
	if ( selItem == False ):
		print( "Please select an object before pressing button." )
	
	# otherwise load first selected object into textField
	else:
		
		# if statement determines which name field is updated
		if (b2 == 1):
			
			# edit the Driver name textField with first selection
			cmds.textField( 'drvrNameFld', e=True, tx=selItem[0] )
			
		else:
			
			# edit the Driven name textField with first selection
			cmds.textField( 'drvnNameFld', e=True, tx=selItem[0] )
		
			
	# if statement determines that the attribute fields will be updated		
	elif (b1 == 2):
		
		# list first selected attribute into variable
		selAttr = cmds.channelBox( 'mainChannelBox', q=True, sma=True )
		
		# No attr selection: 
		# TypeError: 'NoneType' object is unsubscriptable # 

		# check to see if selection is blank and warn user
		if ( selAttr == " "):
			print( "Please select an attribute in the Channel Box before pressing button." )
		
		# otherwise load first selected attribute into textField
		else:
			
			# if statement determines which attribute field is updated
			if (b2 == 1):
				
				# edit the Driver attr textField with first selection
				cmds.textField( 'drvrAttrFld', e=True, tx=selAttr[0] )
				
			else:
				# edit the Driven attr textField with first selection
				cmds.textField( 'drvnAttrFld', e=True, tx=selAttr[0] )
	'''
	
# query the textFields for the driver name and attr
def queryDrvr():
	
	# query the textFields to use values in SDK process
	drvrNameTx = cmds.textField( 'drvrNameFld', q=True, tx=True )	
	drvrAttrTx = cmds.textField( 'drvrAttrFld', q=True, tx=True )
	
	driver = drvrNameTx + "." + drvrAttrTx
	return driver



# create function to query from the GUI and loop the desired SDK values			
def makeSdk( fldGrp1, fldGrp2, fldGrp3, fldGrp4, fldGrp5 ):
	
	
	# query the textFields and optionMenu to use values in SDK process
	driver = queryDrvr()
	
	tslList = queryAll('drvnTSL')
	
	sdkNum = cmds.optionMenu( 'sdkOpt', q=True, v=True )
	
	'''
	# check to see if any fields were left blank, and warn user to fill them
	if ( drvrNameTx == ""):
		print( "Please select a Driver object and enter it into the field." )
	elif ( drvnNameTx == ""):
		print( "Please select a Driven object and enter it into the field." )
	elif ( drvrAttrTx  == ""):
		print( "Please select a Driver attribute and enter it into the field." )
	elif ( drvnAttrTx  == ""):
		print( "Please select a Driven attribute and enter it into the field." )	
	else:
		
	'''
		
	# place names of driver and driven floatFields into a list
	fltFldNames = [ fldGrp1, fldGrp2, fldGrp3, fldGrp4, fldGrp5 ]

	# declare lists to store values to use in sdk loop
	drvrFldVals = []
	drvnFldVals = []
		
	
	
	#declare counters for loops
	i = 0
	j = 0
	k = 0
	
	
	
	# loop to place the queried values of the floatFields into a list
	while ( i < int(sdkNum) ):
		
		# query the value 1 and value 2 flags from the floatFieldGrps
		drvrFldVals.append( cmds.floatFieldGrp( fltFldNames[i], q=True, 
			v1=True ) )
		drvnFldVals.append( cmds.floatFieldGrp( fltFldNames[i], q=True, 
			v2=True ) )
				
		#increment counter
		i += 1
	
	# loop sdk values based on the length of tslList
	while ( k < len(tslList) ):
		
		j = 0
		
		# loop sdk values based on the number queried from optionMenu
		while ( j < int(sdkNum) ):
			
			cmds.setDrivenKeyframe( tslList[k], currentDriver=driver, 
				driverValue=drvrFldVals[j], value=drvnFldVals[j] )
				
			#increment counter
			j += 1
			
		#increment counter	
		k += 1

	#updateKeyOutline()
	
	
	
	
'''
textScrollList functions that are reusable
'''

	
def addObj(tsl):
	'''
	add selected attributes to the textScrollList
	'''
	
	# grab selected item from the scene
	selItem = cmds.ls( sl=True )
	
	# list first selected attribute into variable
	selAttr = cmds.channelBox( 'mainChannelBox', q=True, sma=True )
	
	# loop based on items in selAttr list
	for sel in selAttr:
		# add them to the textScrollList
		cmds.textScrollList( tsl, e=True, append=selItem[0] + "." + sel )


		
def addCrv(tsl):
	'''
	add animation curves from selected object to the textScrollList
	'''
	
	# grab selected item from the scene
	selItem = cmds.ls( sl=True )
	
	# list animation curves into variable
	animCrv = cmds.listConnections( selItem, source=True, t="animCurve" )
	
	cmds.textScrollList( tsl, e=True, append=animCrv, selectItem=animCrv[0] )

	cmds.keyframeOutliner( 'keyOutline', e=True, animCurve=animCrv[0] )
	
	'''
	# loop based on items in selAttr list
	for sel in selAttr:
		# add them to the textScrollList
		cmds.textScrollList( tsl, e=True, append=selItem[0] + "." + sel )
	'''	
	
	
def clearAll(tsl):
	'''
	remove all items from the textScrollList
	'''
	
	# remove all from the textScrollList
	cmds.textScrollList( tsl, e=True, removeAll=True )



def clearSel(tsl):
	'''
	remove selected items from the textScrollList
	'''
	
	# grab selected items from the textScrollList
	sel = cmds.textScrollList( tsl, q=True, selectItem=True )
	
	# remove all from the textScrollList
	cmds.textScrollList( tsl, e=True, removeItem=sel )



def queryAll(tsl):
	'''
	query all items in the textScrollList
	'''
	tslItems = cmds.textScrollList( tsl, q=True, allItems=True )
	
	return tslItems

'''	
def seekAnimCrvs(objs):
	
	#declare counter for loop
	i = 0
	
	# loop to add the animation curves to the top menu
	while ( i < len(objs) ):
		
		if ( i==0 ):
			
			#get names of animation curves attatched to an object
			curveNames = cmds.listConnections( objs[i], source=True, 
				t="animCurve" )
			
			#increment counter
			i += 1
			
		else:
			#get names of animation curves attatched to an object
			curveNames.append( cmds.listConnections( objs[i], 
				source=True, t="animCurve" ) )
			
			#increment counter
			i += 1
		
	return curveNames
'''	
	
def changeAnim(tsl, kOut):
	
	selItem = cmds.textScrollList( tsl, q=True, selectItem=True )
	
	cmds.keyframeOutliner( kOut, e=True, animCurve=selItem[0] )
	
	
	
def changeAnim2(tsl, kOut):
	
	selItem = cmds.textScrollList( tsl, q=True, selectItem=True )
	
	splitSel = selItem[0].split( "." )
	
	attr=""
	
	if (splitSel[1] == "tx"):
		attr = "translateX"
	elif (splitSel[1] == "ty"):
		attr = "translateY"
	elif (splitSel[1] == "tz"):
		attr = "translateZ"
	elif (splitSel[1] == "rx"):
		attr = "rotateX"
	elif (splitSel[1] == "ry"):
		attr = "rotateY"
	elif (splitSel[1] == "rz"):
		attr = "rotateZ"
	elif (splitSel[1] == "sx"):
		attr = "scaleX"
	elif (splitSel[1] == "sy"):
		attr = "scaleY"
	elif (splitSel[1] == "sz"):
		attr = "scaleZ"
	else:
		attr = splitSel[1]
		
	curveName = splitSel[0] + "_" + attr
	
	cmds.keyframeOutliner( kOut, e=True, animCurve=curveName )

'''	
def updateKeyOutline(): 
	
	tslList = queryAll('drvnTSL')
	
	animCrvs = seekAnimCrvs(tslList)
	
	
	cmds.menu( "keyMenu", e=True, deleteAllItems=True )
	
	#declare counter for loop
	i = 0
	
	# loop to add the animation curves to the top menu
	while ( i < len(animCrvs) ):
		
		
		cmds.menuItem( label=animCrvs[i], p="keyMenu", 
			c=scriptName + ".updateKeyMenu(" + animCrvs[i] + ")" )
		
		#increment counter
		i += 1
		
		
		
def updateKeyMenu(curve):
	
	cmds.keyframeOutliner( 'keyOutline', e=True, animCurve=curve )
	
'''


'''


import maya.cmds as cmds

cmds.window( 'myWindow', rtf=0, width=200 )
cmds.formLayout( 'myForm' )
cmds.keyframeOutliner( 'myOutliner', animCurve='pSphere1_translateY', dsp="narrow" )
cmds.formLayout( 'myForm', e=True, af=[('myOutliner', 'top', 0), ('myOutliner', 'left', 0), ('myOutliner', 'bottom', 0), ('myOutliner', 'right', 0)] )
cmds.showWindow()



cmds.listConnections( destination=True, type="animCurve" )

'''

