'''
--------------------------------------------------------------------------------
///////////////////////////// ceb_quickSdkGUI_v3.py ////////////////////////////
--------------------------------------------------------------------------------

Title: Quick SDK Creator

by: Craig Buchanan

How to Run:
	
import ceb_quickSdkGUI_v3
reload(ceb_quickSdkGUI_v3)


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


'''
class definition section
'''

class TSL( object ):
	'''
	creates a textScrollList
	'''
	
	
	def __init__( self, tsl, multiVal, height, selCmd ):
		self.name = cmds.textScrollList( tsl, h=height, selectCommand=selCmd )
		
		if ( multiVal == 1 ):
			cmds.textScrollList( tsl, e=True, ams=True )
	
	def getName( self ):
		return self.name
	
	def clearAll( self ):
		'''
		remove all items from the textScrollList
		'''
	
		cmds.textScrollList( self.name, e=True, removeAll=True )
	
	
	def clearSel( self,tsl ):
		'''
		remove selected items from the textScrollList
		'''
		
		# grab selected items from the textScrollList
		sel = cmds.textScrollList( tsl, q=True, selectItem=True )
		
		# remove all from the textScrollList
		cmds.textScrollList( tsl, e=True, removeItem=sel )
	
	
	def queryAll( self ):
		'''
		query all items in the textScrollList
		'''
		
		tslItems = cmds.textScrollList( tsl, q=True, allItems=True )
		
		return tslItems
		
		
	def addObj( self ):
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



class Text( object ):
	'''
	creates text
	'''
	
	def __init__( self, obj, lText, wid ):
		self.name = cmds.text( obj, l=lText, w=wid )
		
	def getName( self ):
		return self.name
	
	def getLabel( self ):
		return cmds.text( self.name, q=True, label=True)
		
	def setLabel( self, lText ):
		cmds.text( self.name, e=True, label=lText)



class Button( Text ):
	'''
	creates a button based on class Text
	'''
	
	def __init__( self, obj, lText, wid, cmd ):
		cmds.button( obj, l=lText, w=wid, c=cmd )
	
	
	
class TextField( object ):
	'''
	creates a textField
	'''
	
	def __init__( self, obj, wid, txt ):
		cmds.textField( obj, w=wid, tx=txt )



class FloatField( object ):
	'''
	creates a floatField
	'''
	
	def __init__( self, obj, wid, val, precVal ):
		cmds.floatField( obj, w=wid, v=val, pre=precVal )
	
	
		
class Window( object ):
	'''
	creates a button based on class Text
	'''
	
	def __init__( self, name, lText, wid, hgt  ):
		cmds.window( name, w=wid, h=hgt )
		
	def show( self, name ):
		cmds.showWindow( name )
		
	



'''
end class definitions
'''


# import the maya module		
import maya.cmds as cmds


# create variables to use in the script
winName = "quickSdkGUI_v3"
scriptName = __name__




def checkGUI():
	'''
	check for the GUI
	'''
	
	# if the window exists, delete it
	if ( cmds.window( winName, ex=True ) ):
		cmds.deleteUI( winName )



# define the GUI creation function for Mac
def macGUI():
	'''
	create the GUI for Mac format
	'''
	
	# check to see if the GUI exists
	checkGUI()
	
	
	# create a variable to set the width of the window
	width = 430
	
	# create the window
	win1 = Window( winName, 'Quick SDK GUI', width, 480 )
	
	
	
	# create columnLayout as main layout
	cmds.formLayout( 'mainForm' )
	
	
	# create a frameLayout to encapsulate and label the window elements
	cmds.frameLayout('mainFrame', label="Quick SDK", borderStyle='etchedIn',
		w=370 )
	
	
	
	# create formLayout as a sub layout
	cmds.formLayout( 'subForm', h=300 )
	
	
	# create a frameLayout to encapsulate and label the window elements
	drvrFr = cmds.frameLayout('drvrFrame', label="Driver:", 
		borderStyle='etchedIn' )
	
	
	
	# create variable for the textField widths
	tFld1W = 120
	tFld2W = 60
	tFld3W = 80
	
	
	# create a rowColumnLayout for the Driver
	cmds.rowColumnLayout(nc=3, cw= ([1, tFld1W], [2, tFld2W], [3, tFld3W]) )
	
	
	
	# create GUI elements for Driver
	
	nTxt = Text( 'nameTxt', "Name:", 50 )
	aTxt = Text( 'attrTxt', "Attr:", 50 )
	bTxt1 = Text( 'blankTxt1', " ", 50 )
	
	drvr1 = TextField( 'drvrNameFld', tFld1W, "Driver" )
	drvr2 = TextField( 'drvrAttrFld', tFld2W, "Attribute" )
	lBtn1 = Button('drvrBtn', "Load Selected", tFld3W, scriptName + ".loadSel()")
	
	# close the driver rowColumnLayout
	cmds.setParent( ".." )
	
	# close the driver frameLayout
	cmds.setParent( ".." )
	
	
	
	# create a frameLayout to encapsulate and label the window elements
	drvnFr = cmds.frameLayout('drvnFrame', label="Driven:", 
		borderStyle='etchedIn' )
	
	# create a columnLayout
	cmds.columnLayout()
	
	
	
	# create variable for the tsl selectCommand
	selCmd=scriptName + ".changeAnim('drvnTSL','keyOutline', 'keyOutFrame')"
	
	# create a textScrollList for the driven objects and attrs
	dTSL = TSL( 'drvnTSL', 1, 100, selCmd )
	#cmds.textScrollList( 'drvnTSL', ams=True, h=100, selectCommand=scriptName + ".changeAnim2('drvnTSL','keyOutline')" )
	
	
	# create variables for width values
	tslBtnW1 = 50
	tslBtnW2 = 70
	
	
	# create a rowLayout to eonclose the TSL buttons
	cmds.rowLayout( nc=3, cw3= (tslBtnW1, tslBtnW2, tslBtnW2) )
	
	addBtn1 = Button( 'addBtn', "Add", tslBtnW1, scriptName + ".addObj('drvnTSL')" )
	rAllBtn1 = Button( 'remAllBtn', "Remove All", tslBtnW2, scriptName + ".clearAll('drvnTSL')" )	
	rSelBtn1 = Button( 'remSelBtn', "Remove Sel", tslBtnW2, scriptName + ".clearSel('drvnTSL')" )
	
	
	# close the button rowLayout
	cmds.setParent( ".." )
	
	
	# close the driven columnLayout
	cmds.setParent( ".." )
	# close the driven frameLayout
	cmds.setParent( ".." )
	
	
	
	# create a frameLayout to encapsulate and label the window elements
	valFr = cmds.frameLayout('valFrame', label="Values:", 
		borderStyle='etchedIn' )
	
	# create a columnLayout
	cmds.columnLayout()
		
	# create optionMenu to determine # of SDKs to perform
	cmds.optionMenu( 'sdkOpt', w=50 )
	cmds.menuItem( label='1' )
	cmds.menuItem( label='2' )
	cmds.menuItem( label='3' )
	cmds.menuItem( label='4' )
	cmds.menuItem( label='5' )
	
	
	fldVal1=40
	fldVal2=60
	'''
	flt1 = cmds.floatFieldGrp( 'fld1Grp', nf=5, value1=0.0, 
		value2=0.0, value3=0.0, value4=0.0, value5=0.0,
		pre=2, cw=( [1, fldVal1], [2, fldVal1], [3, fldVal1],
		[4, fldVal1], [5, fldVal1]) )
	'''
	
	# create a rowColumnLayout for the text and value fields
	cmds.rowColumnLayout(nc=5, cw= ([1, fldVal1], [2, fldVal1], [3, fldVal1],
		[4, fldVal1], [5, fldVal1]) )
	
	
	# create text to describe the floatFields using the Text class
	valTxt1 = Text( 'valTxt1', "1:", fldVal1 )
	valTxt2 = Text( 'valTxt2', "2:", fldVal1 )
	valTxt3 = Text( 'valTxt3', "3:", fldVal1 )
	valTxt4 = Text( 'valTxt4', "4:", fldVal1 )
	valTxt5 = Text( 'valTxt5', "5:", fldVal1 )
	
	
	# create floatFields for the driver using the FloatField class
	drFlt1 = FloatField( 'drFltFld1', fldVal1, 0.0, 2 )
	drFlt2 = FloatField( 'drFltFld2', fldVal1, 0.0, 2 )
	drFlt3 = FloatField( 'drFltFld3', fldVal1, 0.0, 2 )
	drFlt4 = FloatField( 'drFltFld4', fldVal1, 0.0, 2 )
	drFlt5 = FloatField( 'drFltFld5', fldVal1, 0.0, 2 )
	
	
	# create floatFields for the driven using the FloatField class
	dnFlt1 = FloatField( 'dnFltFld1', fldVal1, 0.0, 2 )
	dnFlt2 = FloatField( 'dnFltFld2', fldVal1, 0.0, 2 )
	dnFlt3 = FloatField( 'dnFltFld3', fldVal1, 0.0, 2 )
	dnFlt4 = FloatField( 'dnFltFld4', fldVal1, 0.0, 2 )
	dnFlt5 = FloatField( 'dnFltFld5', fldVal1, 0.0, 2 )
	
	
	# close the rowColumnLayout
	cmds.setParent( ".." )
	
	
	# create variable for the sdk command
	sdkCmd = scriptName + ".makeSdk( 'drFltFld1', 'drFltFld2', 'drFltFld3', 'drFltFld4', 'drFltFld5', 'dnFltFld1', 'dnFltFld2', 'dnFltFld3', 'dnFltFld4', 'dnFltFld5' )"
	sdkCmd = scriptName + ".makeSdk()"
	
	# create button to run sdk function
	sdkBtn = Button( 'sdkBtn', "Create SDK", 80, sdkCmd )
	
	
	# close the columnLayout
	cmds.setParent( ".." )
	
	# close the frameLayout
	cmds.setParent( ".." )
	
	
	
	# create a frameLayout to encapsulate and label the window elements
	keyFr = cmds.frameLayout('keyOutFrame', l="Driven Key Values:", 
		borderStyle='etchedIn', collapsable=True, h=150 )
	
	
	# create a formLayout to contain the keyframeOutliner
	cmds.formLayout( 'keyForm' )
	
	
	# create a keyframeOutliner
	keyOut = cmds.keyframeOutliner( 'keyOutline', dsp="narrow", 
		animCurve='animCurve1' )	
	
	
	# close the formLayout
	cmds.setParent( ".." )
	
	# close the frameLayout
	cmds.setParent( ".." )
	
	
	
	# edit the main formLayout
	cmds.formLayout( 'mainForm', e=True,
		
		af=[ ( 'mainFrame', "left", 5),
		('mainFrame', "top", 5) ] )
	
	
	
	# edit the sub formLayout
	cmds.formLayout( 'subForm', e=True, 
		
		af=[ (drvrFr, "left", 5),
		(drvrFr, "top", 5),
		(drvrFr, "right", 5)],
		
		ac=[ (drvnFr, "top", 5, drvrFr),
		(valFr, "top", 5, drvnFr),
		(keyFr, "top", 5, valFr)],
		
		aoc=[ (drvnFr, "left", 0, drvrFr),
		(drvnFr, "right", 0, drvrFr),
		(valFr, "left", 0, drvrFr),
		(valFr, "right", 0, drvrFr),
		(keyFr, "left", 0, drvnFr),
		(keyFr, "right", 0, drvnFr)] )
	
	
	
	# edit the keyOutline formLayout
	cmds.formLayout( 'keyForm', e=True, 
	
		af=[ (keyOut, 'top', 0), 
		(keyOut, 'left', 0), 
		(keyOut, 'bottom', 0), 
		(keyOut, 'right', 0) ] )
	
	
	
	# show the window
	win1.show( winName )



# define the GUI creation function for Windows
def winGUI():
	'''
	create the GUI for PC format
	'''
	
	# run macGUI function since there currently isn't a difference
	macGUI()



'''
check OS version and run appropriate function
'''

if ( cmds.about( os=True ) == "nt" ):
	print( "You are using a PC!" )
	winGUI()
	
elif ( cmds.about( os=True ) == "mac" ):
	print( "You are using a Mac!" )
	macGUI()

else:
	print( "You are using an unsupported type of OS" )
	


	
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
	
	
	
def queryDrvr():
	'''
	query the textFields for the driver name and attr
	'''
	
	# query the textFields to use values in SDK process
	drvrNameTx = cmds.textField( 'drvrNameFld', q=True, tx=True )	
	drvrAttrTx = cmds.textField( 'drvrAttrFld', q=True, tx=True )
	
	driver = drvrNameTx + "." + drvrAttrTx
	return driver
	
	
	
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
end textScrollList functions
'''	

'''
def makeSdk( [], [] ):
def makeSdk( *args ):
	# Check for even number of arguments.
'''

def makeSdk():
	# Getting how many sdk's to create.
	sdkNum = int(cmds.optionMenu( 'sdkOpt', q=True, v=True ))
	driverField = 'drFltFld'
	drivenField = 'dnFltFld'
	drivenList = queryAll('drvnTSL')
	driver = queryDrvr()

	i = 0
	while( i < sdkNum ):
		# Get my values from the gui
		drivenVal = cmds.floatField( drivenField + str(i+1) , q=True, v=True )
		driverVal = cmds.floatField( driverField + str(i+1) , q=True, v=True )
	
		for currDriven in drivenList:
			cmds.setDrivenKeyframe( currDriven, currentDriver=driver, 
					driverValue=driverVal, value=drivenVal )	
		i = i + 1

	
"""				
def makeSdk( drFld1, drFld2, drFld3, drFld4, drFld5, 
	dnFld1, dnFld2, dnFld3, dnFld4, dnFld5 ):
	'''
	query from the GUI and loop the desired SDK values
	'''
	
	
	# query the textFields and optionMenu to use values in SDK process
	driver = queryDrvr()
	
	tslList = queryAll('drvnTSL')
	
	sdkNum = cmds.optionMenu( 'sdkOpt', q=True, v=True )
		
	# place names of driver and driven floatFields into a list
	drFltFldNames = [ drFld1, drFld2, drFld3, drFld4, drFld5 ]
	
	dnFltFldNames = [ dnFld1, dnFld2, dnFld3, dnFld4, dnFld5 ]

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
		drvrFldVals.append( cmds.floatField( drFltFldNames[i], q=True, 
			v=True ) )
			
		# query the value 1 and value 2 flags from the floatFieldGrps
		drvnFldVals.append( cmds.floatField( dnFltFldNames[i], q=True, 
			v=True ) )
				
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

"""

def changeAnim(tsl, kOut, kOutFr):
	'''
	load an animation curve into the keyframeOutliner
	'''
	
	selItem = cmds.textScrollList( tsl, q=True, selectItem=True )
	
	splitSel = selItem[0].split( "." )
	
	attr = splitSel[1]
	
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
		
	curveName = splitSel[0] + "_" + attr
	
	cmds.keyframeOutliner( kOut, e=True, animCurve=curveName )
	
	#cmds.frameLayout( kOutFr, e=True, l="Driven Key Values: " + curveName )
