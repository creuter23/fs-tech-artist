'''
--------------------------------------------------------------------------------
///////////////////////////// ceb_quickSdkGUI_v3.py ////////////////////////////
--------------------------------------------------------------------------------

Title: Quick SDK Creator


By: Craig Buchanan
Special Thanks: Michael Clavan, for suggestions and guidance


How to Run:
	
import ceb_quickSdkGUI_v4
reload(ceb_quickSdkGUI_v4)
ceb_quickSdkGUI_v4.guiCreate()


	

	Select an object in the scene and an attribute name from the channel
	box, then click the "Load Selected" button to designate your driver. 
	Next select the object(s) and attribute(s) that should be driven
	and click the "Add" button. Now select the number of values you wish 
	to keyframe and enter values in the fields. 
	
	Selecting from the list of driven objects will load any newly created
	or previously existing animation curves into the lowest section of the
	UI. You can use this to modify the values of the driver and driven
	attributes.
	
	To remove the entire animation curve from an atribute, select it in
	the list of driven objects and press the "Del Keys" button. To delete 
	any of the indices from the animation curve, right click on the 
	"Del Keys" button and select the index number to remove.

--------------------------------------------------------------------------------
////////////////////////////////////////////////////////////////////////////////
--------------------------------------------------------------------------------

'''

# import the maya module for cmds, warning messages, and mel evals
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.mel as mel

mel.eval( 'python( "import sys")' )


#from callback import Callback

# create variables to use in the script
winName = "quickSdkGUI_v4"
scriptName = __name__



'''
Class definition section
'''



class Callback():
	'''
	Class that fixes Maya from using each line in a function as an undo stack
	'''
	
	_callData = None
	def __init__( self, func, *args, **kwargs ):
		self.func = func
		self.args = args
		self.kwargs = kwargs
		
	def __call__( self, *args ):
		Callback._callData = ( self.func, self.args, self.kwargs )
		mel.eval( 'global proc py_%s() { python( "sys.modules[\'%s\'].Callback._doCall()" ) ; }' %( self.func.__name__, __name__ ) )
		
		try:
			mel.eval( 'py_%s()' %( self.func.__name__ ) )
			
		except RuntimeError:
			pass
			
		if isinstance( Callback._callData, Exception ):
			raise Callback._callData
		
		return Callback._callData
	
	@staticmethod
	def _doCall():
		( func, args, kwargs ) = Callback._callData
		Callback_callData = func( *args, **kwargs )
	
	
	
class TSL( object ):
	'''
	Class that creates a textScrollList
	'''
	
	
	
	def __init__( self, tsl, multiVal, width, height, selCmd ):
		self.name = cmds.textScrollList( tsl, w=width, h=height, 
			selectCommand=selCmd )
		
		if ( multiVal == 1 ):
			cmds.textScrollList( tsl, e=True, ams=True )
		
		
	def __str__( self ):
		
		return self.name
		
		
	def getName( self ):
		'''
		Return name of instanced TSL
		'''
		
		return self.name
		
		
		
	def clearAll( self ):
		'''
		Remove all items from the textScrollList
		'''
	
		cmds.textScrollList( self.name, e=True, removeAll=True )
	
	
	
	def clearSel( self ):
		'''
		Remove selected items from the textScrollList
		'''
		
		try:	# run code, but catch errors
			
			# grab selected items from the textScrollList
			sel = cmds.textScrollList( self.name, q=True, selectItem=True )
			
			if ( sel ):
				
				# remove all from the textScrollList
				cmds.textScrollList( self.name, e=True, removeItem=sel )
				
			else:
			
				OpenMaya.MGlobal.displayWarning( "Please select an item from the TSL, or load an item to select." )
				
		except:
	
			OpenMaya.MGlobal.displayWarning( "Please select an item from the TSL, or load an item to select." )
	
	
	
	def queryAll( self ):
		'''
		Query all items in the textScrollList
		'''
		
		tslItems = cmds.textScrollList( self.name, q=True, allItems=True )
		
		if ( tslItems ):
			
			return tslItems
			
		else:
			return []
		
		
		
	def querySel( self ):
		'''
		Query selected items in the textScrollList
		'''
		
		tslItems = cmds.textScrollList( self.name, q=True, si=True )
		
		if ( tslItems ):
			
			return tslItems
			
		else:
			return []
		
		
		
	def addSel( self ):
		'''
		Add selected attributes to the textScrollList
		'''
		
		# grab selected item from the scene
		selItem = cmds.ls( sl=True )
		
		# grab current items in TSL
		tslItems = self.queryAll()
		
		# loop based on items in selAttr list
		for sel in selItem:
			
			try:	# run code, but catch errors
			
				# if element isn't already in TSL, append it
				if (tsl not in tslItems):
					
					# add items to the textScrollList
					cmds.textScrollList( self.name, e=True, 
						append=sel )
					
			except TypeError:	# nothing is in TSL
				
				# add items into TSL if nothing exists
				cmds.textScrollList( self.name, e=True, append=sel )
			
		
		
		
class Text( object ):
	'''
	Creates class for GUI text
	'''
	
	def __init__( self, obj, lText, wid ):
		self.name = cmds.text( obj, l=lText, w=wid )
		
	def getName( self ):
		'''
		Return name of instanced Text
		'''
		
		return self.name
	
	def getLabel( self ):
		'''
		Return label of instanced Text
		'''
		
		return cmds.text( self.name, q=True, label=True)
		
	def setLabel( self, lText ):
		'''
		Set label of instanced Text
		'''
		
		cmds.text( self.name, e=True, label=lText)
	
	
	
class Button( Text ):
	'''
	Creates class for a button based on class Text
	'''
	
	def __init__( self, obj, lText, wid, cmd ):
		self.name = cmds.button( obj, l=lText, w=wid, c=cmd )
	
	def setAnn( self, ann ):
		'''
		Sets the annotation of the button
		'''
		
		cmds.button( self.name, e=True, annotation=ann )
	
	
	
class TextField( object ):
	'''
	Creates class for a textField
	'''
	
	def __init__( self, obj, wid, txt ):
		self.name = cmds.textField( obj, w=wid, tx=txt )
		
	def getName( self ):
		'''
		Return name of instanced TextField
		'''
		
		return self.name

	def getTxt( self ):
		'''
		Return text of instanced TextField
		'''
		
		return cmds.textField( self.name, q=True, tx=True )
	
	
	
class FloatField( object ):
	'''
	Creates class for a floatField
	'''
	
	def __init__( self, obj, wid, val, precVal ):
		self.name = cmds.floatField( obj, w=wid, v=val, pre=precVal )
	
	
	
class Window( object ):
	'''
	Creates class for window creation
	'''
	
	def __init__( self, name, lText, wid, hgt  ):
		self.name = cmds.window( name, t=lText, w=wid, h=hgt )
	
	
	def show( self ):
		'''
		Show the window using maya command
		'''
		cmds.showWindow( self.name )
		
	def getName( self ):
		'''
		Return name of instanced Window
		'''
		
		return self.name
		



'''
End class definitions
'''


'''
Define work functions
'''



def checkGUI( win ):
	'''
	check for the GUI
	'''
	
	# if the window exists, delete it
	if ( cmds.window( win, ex=True ) ):
		cmds.deleteUI( win )



def makeGUI( wWid, wHigh, f1H, f2H, f3H ):
	'''
	create the GUI for Mac format
	'''
	
	# check to see if the GUI exists
	checkGUI( winName )
	
	
	# create a variable to set the width of the window
	frWidth = wWid-10
	
	# create the window
	win1 = Window( winName, 'Quick SDK GUI', wWid, wHigh )
	
	
	
	# create columnLayout as main layout
	cmds.formLayout( 'mainForm', w=frWidth)
	
	
	# create a frameLayout to encapsulate and label the window elements
	cmds.frameLayout( 'mainFrame', label="Quick SDK", borderStyle='etchedIn',
		w=frWidth )
	
	
	
	# create formLayout as a pad layout for the Window
	cmds.formLayout( 'padForm', h=300 )
	
	
	# create a frameLayout to encapsulate and label the window elements
	drvrFr = cmds.frameLayout( 'drvrFrame', label="Driver:", 
		borderStyle='etchedIn', collapsable=True )
	
	
	# create formLayout as a pad layout for the Driver Section
	cmds.formLayout( 'drvrPadForm', height=f1H )
	# height is 54 on Mac, 43 on PC
	
	
	# create variable for the textField widths
	tFld1W = 120
	tFld2W = 60
	#tFld3W = 80
	
	
	# create a rowColumnLayout for the Driver Section
	cmds.rowColumnLayout( 'drvrMainLayout', nc=4, 
		cw= ( [1, tFld1W], [2, tFld2W], [3, tFld2W], [4, tFld2W] ) )
	
	
	
	# create GUI elements for Driver
	
	nTxt = Text( 'nameTxt', "Name:", 50 )
	aTxt = Text( 'attrTxt', "Attr:", 50 )
	bTxt1 = Text( 'blankTxt1', " ", 50 )
	bTxt2 = Text( 'blankTxt2', " ", 50 )
	
	global drvr1
	drvr1 = TextField( 'drvrNameFld', tFld1W, "Driver" )
	global drvr2
	drvr2 = TextField( 'drvrAttrFld', tFld2W, "Attribute" )
	lBtn1 = Button( 'drvrBtn', "Load Sel", tFld2W, Callback( loadSel, drvr1.name, drvr2.name ) )
	lBtn1.setAnn( "Loads a selected driver object and a selected attribute from the channel box." )
	selObjBtn = Button( 'selDrvrBtn', "Sel Obj", tFld2W, Callback( selObj, drvr1.name, 1 ) )
	selObjBtn.setAnn( "Selects the driver object specified in the driver field." )
	
	
	# close the driver rowColumnLayout
	cmds.setParent( ".." )
	
	# close the driver formLayout
	cmds.setParent( ".." )
	
	
	# close the driver frameLayout
	cmds.setParent( ".." )
	
	
	
	# create a frameLayout to encapsulate and label the window elements
	drvnFr = cmds.frameLayout( 'drvnFrame', label="Driven:", 
		borderStyle='etchedIn', collapsable=True )
	
	
	# create formLayout as a pad layout for the Driven Section
	cmds.formLayout( 'drvnPadForm', height=f2H )
	# height is 105 on Mac, 115 on PC
	
	# create a columnLayout
	cmds.rowLayout( 'drvnMainLayout', nc=2, cw = ( [1, 175], [2, 70] ) )
	
	
	
	# create a textScrollList for the driven objects and attrs
	global dTSL
	dTSL = TSL( 'drvnTSL', 1, 175, 100, Callback( changeAnim, 'drvnTSL', 'keyOutline', 'keyOutFrame' ) )
	
	
	# create variables for width values
	tslBtnW1 = 50
	tslBtnW2 = 70
	
	
	# create a columnLayout to enclose the TSL buttons
	cmds.columnLayout( 'tslBtnCol' )
	
	# consider looping these
	
	# create TSL buttons
	addBtn1 = Button( 'addBtn', "Add", tslBtnW2, Callback( addObj, dTSL.name ) )
	addBtn1.setAnn( "Adds driven objects an selected attributes to the textScrollList." )
	rAllBtn1 = Button( 'remAllBtn', "Remove All", tslBtnW2, Callback( dTSL.clearAll ) )
	rAllBtn1.setAnn( "Removes all objects from the textScrollList." )
	rSelBtn1 = Button( 'remSelBtn', "Remove Sel", tslBtnW2, Callback( dTSL.clearSel ) )
	rSelBtn1.setAnn( "Removes selected objects from the textScrollList." )
	delAnimBtn1 = Button( 'delAnimBtn', "Del Keys", tslBtnW2, Callback( delAnim, dTSL.name ) )
	delAnimBtn1.setAnn( "Deletes animation curve associated with this attribute, right click for menu." )
	revAnimBtn1 = Button( 'revAnimBtn', "Reverse", tslBtnW2, Callback( revAnim, dTSL.name ) )
	revAnimBtn1.setAnn( "Reverses the driven values of the animation curve associated with this attribute." )
	
	
	
	# create popUpMenu for Del Keys button
	global animIndexMenu
	animIndexMenu = cmds.popupMenu( 'dr1Pop', parent=delAnimBtn1.name, button=3 )
	cmds.menuItem( label="Del Index:" )
	cmds.menuItem( divider=True )
	cmds.menuItem( label="No animation curves present" )
	
	
	
	# close the driven columnLayout
	cmds.setParent( ".." )
	
	# close the button rowLayout
	cmds.setParent( ".." )
	
	# close the driven formLayout
	cmds.setParent( ".." )
	
	
	# close the driven frameLayout
	cmds.setParent( ".." )
	
	
	
	# create a frameLayout to encapsulate and label the window elements
	valFr = cmds.frameLayout( 'valFrame', label="Values:", 
		borderStyle='etchedIn', collapsable=True )
	
		
	# create formLayout as a pad layout for the Value Section
	cmds.formLayout( 'valPadForm', height=f3H )
	# height is 125 on Mac, 111 on PC
	
	
	# create a columnLayout
	cmds.columnLayout( 'valMainLayout' )
	
	
	# create a rowLayout
	cmds.rowLayout( nc=2, cw2= [50, 50] )
	
	
	# create text element to identify the value optionMenu
	vNumTxt1 = Text( 'valNumTxt1', "Value #: ", 50 )
	
	
	# create optionMenu to determine # of SDKs to perform
	sdkOptName = cmds.optionMenu( 'sdkOpt', w=50 )
	
	sdkOptNum = [ '1', '2', '3', '4', '5' ]
	
	for num in sdkOptNum:
		
		cmds.menuItem( label=num )
	
	
	# close the rowLayout
	cmds.setParent( ".." )
	
	
	
	# create a rowColumnLayout
	cmds.rowLayout(nc=2 )
	
	# create a columnLayout
	cmds.columnLayout(w=100)
	
	
	
	# create text elements to identify the value fields
	blIdTxt1 = Text( 'blankIdTxt1', " ", 100 )
	drIdTxt1 = Text( 'driverIdTxt1', "Driver Values: ", 100 )
	dnIdTxt1 = Text( 'drivenIdTxt1', "Driven Values: ", 100 )
	
	
	# close the columnLayout
	cmds.setParent( ".." )
	
	
	# create variables to control width values
	fldVal1=40
	fldVal2=60
	
	
	
	# create a rowColumnLayout for the text and value fields
	cmds.rowColumnLayout(nc=5, w=200, cw= ([1, fldVal1], [2, fldVal1], [3, fldVal1],
		[4, fldVal1], [5, fldVal1]) )
	
	'''
	loop the creation of these
	'''
	
	# create text to describe the floatFields using the Text class
	
	valTxtNums = [ "1", "2", "3", "4", "5" ]
	valTxtNames = [ 'valTxt1', 'valTxt2', 'valTxt3', 'valTxt4', 'valTxt5' ]
	valTxt = [ ]
	
	# declare counter
	i = 0
	
	for num in valTxtNums:
		
		valTxt.append( Text( valTxtNames[i], "%s:" %(num), fldVal1 ) )
		
		# increment counter
		i += 1
	
	
	# create floatFields for the driver using the FloatField class
	
	drValFldNames = [ 'drFltFld1', 'drFltFld2', 'drFltFld3', 'drFltFld4', 'drFltFld5' ]
	drValFld = [ ]
	
	for name in drValFldNames:
		
		drValFld.append( FloatField( name, fldVal1, 0.0, 2 ) )
		
		
	
	# create floatFields for the driven using the FloatField class
	
	dnValFldNames = [ 'dnFltFld1', 'dnFltFld2', 'dnFltFld3', 'dnFltFld4', 'dnFltFld5' ]
	dnValFld = [ ]
	
	for name in dnValFldNames:
		
		drValFld.append( FloatField( name, fldVal1, 0.0, 2 ) )
	
	
	# create popupMenus for each floatField
	
	# declare counter
	i = 0
	
	while ( i < len( valTxtNums ) ):
		
		# create popupMenu to load attribute values and inverse into driver fields
		cmds.popupMenu( 'dr%sPop' %( str(i+1) ), parent=drValFldNames[i], button=3 )
		cmds.menuItem( label="Load Attr Value", c=Callback( loadAttrVal, 'dr', str(i+1), 1 ) )
		cmds.menuItem( label="Load Inverse Value", c=Callback( loadAttrVal, 'dr', str(i+1), -1 ) )
		
		# create popupMenu to load attribute values and inverse into driven fields
		cmds.popupMenu( 'dn%sPop' %( str(i+1) ), parent=dnValFldNames[i], button=3 )
		cmds.menuItem( label="Load Attr Value", c=Callback( loadAttrVal, 'dn', str(i+1), 1 ) )
		cmds.menuItem( label="Load Inverse Value", c=Callback( loadAttrVal, 'dn', str(i+1), -1 ) )
		
		# increment counter
		i += 1
	
	
	# close the rowColumnLayout
	cmds.setParent( ".." )
	
	# close the rowColumnLayout
	cmds.setParent( ".." )
	
	
	
	# create button to run sdk function
	sdkBtn = Button( 'sdkBtn', "Create SDK", 80, Callback( makeSdk, sdkOptName ) )
	sdkBtn.setAnn( "Sets Driven Keyframes based on information provided above to the UI." )
	
	
	
	# close the columnLayout
	cmds.setParent( ".." )
	
	# close the formLayout
	cmds.setParent( ".." )
	
	# close the frameLayout
	cmds.setParent( ".." )
	
	
	
	# create a text object to identify the current animation curve
	crvTxt = cmds.text( 'curveTxt', l="Current Curve: No Curve Selected" )
	
	
	
	# create a frameLayout to encapsulate and label the window elements
	keyFr = cmds.frameLayout( 'keyOutFrame', l="Driven Key Values:", 
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
		('mainFrame', "top", 5), 
		('mainFrame', "right", 5) ] )
	
	
	# edit the pad window formLayout
	cmds.formLayout( 'padForm', e=True, 
		
		af=[ (drvrFr, "left", 5),
		(drvrFr, "top", 5),
		(drvrFr, "right", 5)],
		
		ac=[ (drvnFr, "top", 5, drvrFr),
		(valFr, "top", 5, drvnFr),
		(crvTxt,"top", 5, valFr),
		(keyFr, "top", 0, crvTxt)],
		
		aoc=[ (drvnFr, "left", 0, drvrFr),
		(drvnFr, "right", 0, drvrFr),
		(valFr, "left", 0, drvrFr),
		(valFr, "right", 0, drvrFr),
		(crvTxt,"left", 0, drvrFr),
		(crvTxt,"right", 0, drvrFr),
		(keyFr, "left", 0, drvnFr),
		(keyFr, "right", 0, drvnFr)] )
	
	
	# edit the pad driver formLayout
	cmds.formLayout( 'drvrPadForm', e=True,
		
		af=[ ( 'drvrMainLayout', "left", 5),
		('drvrMainLayout', "top", 5), 
		('drvrMainLayout', "right", 5) ] )
	
	
	# edit the pad driven formLayout	
	cmds.formLayout( 'drvnPadForm', e=True,
		
		af=[ ( 'drvnMainLayout', "left", 5),
		('drvnMainLayout', "top", 5), 
		('drvnMainLayout', "right", 5) ] )
	
	
	# edit the pad value formLayout	
	cmds.formLayout( 'valPadForm', e=True,
		
		af=[ ( 'valMainLayout', "left", 5),
		('valMainLayout', "top", 5), 
		('valMainLayout', "right", 5) ] )
	
	
	# edit the keyOutline formLayout
	cmds.formLayout( 'keyForm', e=True, 
	
		af=[ (keyOut, 'top', 0), 
		(keyOut, 'left', 0), 
		(keyOut, 'bottom', 0), 
		(keyOut, 'right', 0) ] )
	
	
	
	# show the window
	win1.show()



def guiCreate( ):
	'''
	check OS version and pass appropriate variables
	'''
	
	# check the OS that the user is running
	osType = cmds.about( os=True )
	
	if ( osType == "nt" or osType == "win64" ):
		print( "\nYou are using a PC!" )
		
		# call makeGUI function using pixel dimensions for PC
		makeGUI( 350, 585, 48, 120, 116 )
		
	elif ( osType == "mac" ):
		print( "\nYou are using a Mac!" )
		
		# call makeGUI function using pixel dimensions for Mac
		makeGUI( 340, 620, 59, 110, 130 )
	
	else:
		print( "\nYou are using an unsupported type of OS" )
		
	
	
	
def loadSel( nameFld, attrFld ):
	'''
	Function that loads selected objects or attributes into the driver textFields
	'''
	
	try:	# run code, but catch errors
		
		# list first selected item into variable
		selItem = cmds.ls( sl=True )
		
		# list first selected attribute into variable
		selAttr = cmds.channelBox( 'mainChannelBox', q=True, sma=True )
		
		# edit the Driver name textField with first selection
		#cmds.textField( 'drvrNameFld', e=True, tx=selItem[0] )
		cmds.textField( nameFld, e=True, tx=selItem[0] )
		
		# edit the Driver attr textField with first selection
		#cmds.textField( 'drvrAttrFld', e=True, tx=selAttr[0] )
		cmds.textField( attrFld, e=True, tx=selAttr[0] )
		
	except IndexError: # nothing is selected
		
		OpenMaya.MGlobal.displayWarning( "Please select an object then attribute from the channel box." )
		
	except TypeError: # no attr is selected
		
		OpenMaya.MGlobal.displayWarning( "Please select an attribute from the channel box." )
	
	
	
def selObj( selName, val ):
	'''
	Function that selects objects or attributes into the driver textFields
	'''
	
	if ( val ):
		
		try:
			
			# query the driver
			selObj = cmds.textField( selName, q=True, tx=True )
			
			# select the object
			cmds.select( selObj, replace=True )
			
		except TypeError:
			
			OpenMaya.MGlobal.displayWarning( 'Please select an object and attribute from the channel box, then press the "Load Selected" Button.' )
		
	else:
		
		# clear the selection
		cmds.select( clear=True )
		
		# query selected items from TSL
		selItems = dTSL.querySel()
		
		objNames = [ ]
		
		# split the list to remove the ".attr"
		for item in selItems:
			
			# split the items in the list by "."
			splitSel = item.split( "." )
			objNames.append( splitSel[0] )
		
		# select all objects in the scene that are selected in the TSL
		for name in objNames:
			
			cmds.select( name, add=True )
			
	
def queryDrvr( ):
	'''
	Function that queries the textFields for the driver name and attr
	'''
	
	# query the textFields to use values in SDK process
	driver = "%s.%s" %( drvr1.getTxt(), drvr2.getTxt() )
	return driver
	
	
	
'''
textScrollList functions that are reusable
'''



def addObj( tsl ):
	'''
	Function that adds selected attributes to the textScrollList
	
	try:	# run code, but catch errors
	'''
	
	# place selected items from the scene into list
	selItem = cmds.ls( sl=True )
	
	# place selected attributes into list
	selAttr = cmds.channelBox( 'mainChannelBox', q=True, sma=True )
	
	# run queryAll function to grab current items in TSL
	tslItems = dTSL.queryAll()
	
	# declare list
	objAttr = []
	
	if selItem:	# if an object is selected
		
		
		# loop based on items in selItem list
		for select in selItem:
			
			try:
				# loop based on items in selAttr list
				for sel in selAttr:
					
					# append concatenation into list
					objAttr.append( select + "." + sel )
					
			except TypeError:
				# print("Nothing selected in the channelbox")
				OpenMaya.MGlobal.displayWarning( "Please select an attribute from the channel box." )
				# OpenMaya.MGlobal.displayError( "Nothing selected in the channelbox" )
		
		
		# loop to check each element from objAttr list
		for obj in objAttr:
			
			try:	# run code, but catch errors
				
				# if element isn't already in TSL, append it
				if (obj not in tslItems):
					
					# add them to the textScrollList
					cmds.textScrollList( tsl, e=True, 
						append=obj )
						
			except TypeError:	# nothing is in TSL
				
				# add items into TSL if nothing exists
				cmds.textScrollList( tsl, e=True, append=obj )
				
				
	else:	# print warning when no object is selected
		
		OpenMaya.MGlobal.displayWarning( "Please select an object then attribute from the channel box." )
	
	
	

'''
end textScrollList functions
'''	



def loadAttrVal( fld, val, mult ):
	'''
	Load the value of the selected attr into the floatField
	'''
	
	try:	# run code, but catch errors
		
		# list first selected item into variable
		selItem = cmds.ls( sl=True )
			
		# list first selected attribute into variable
		selAttr = cmds.channelBox( 'mainChannelBox', q=True, sma=True )
		
		# query value of selected attr in channelBox
		attrVal = cmds.getAttr("%s.%s" %(selItem[0], selAttr[0]) )
		
		# edit the floatField to the attr value, multiplied by 1 or -1
		cmds.floatField( '%sFltFld%s' %( fld, val ), e=True, v=attrVal*mult )
	
	except TypeError:
		
		OpenMaya.MGlobal.displayWarning( "Please select an attribute from the channel box." )
		
	except IndexError:
		
		OpenMaya.MGlobal.displayWarning( "Please select an attribute from the channel box." )
	
	
	
def makeSdk( sdkOpt ):
	'''
	Function that queries from the GUI and loops the desired SDK values
	'''
	
	try:	# run code, but catch errors
	
		# query the textFields and optionMenu to use values in SDK process
		driver = queryDrvr()
		
		# query the items from TSL to use values in SDK process
		drivenList = dTSL.queryAll()
		
		# query the optionMenu to determine how many iterations to loop
		sdkNum = int( cmds.optionMenu( sdkOpt, q=True, v=True ) )
		
		drName = "drFltFld"
		dnName = "dnFltFld"
		
		#declare counters for loop
		i = 0
		
		while ( i < sdkNum ):
			
			drVal = cmds.floatField( drName + str(i+1), q=True, v=True )
			dnVal = cmds.floatField( dnName + str(i+1), q=True, v=True )
			
			for item in drivenList:
				
				cmds.setDrivenKeyframe( item, currentDriver=driver, 
					driverValue=drVal, value=dnVal )
			
			#increment counter
			i += 1
	
	except:
		
		OpenMaya.MGlobal.displayWarning( "Please load items into the driver and driven sections of the UI." )
	
	
	
def getAnimCurve( tsl ):
	'''
	Function that takes information from TSL to rename it to suit animation curve
	'''
	
	# query selected item from the textScrollList
	selItem = cmds.textScrollList( tsl, q=True, selectItem=True )
	
	# split the list based on a period
	splitSel = selItem[0].split( "." )
	
	
	# determine the longName of the attribute
	lName = cmds.attributeQuery( splitSel[1], node=splitSel[0], ln=True )
	
	
	# concatenate the object name + underscore + longName
	curveName = splitSel[0] + "_" + lName	
	
	return curveName
	
	
	
def changeAnim( tsl, kOut, kOutFr ):
	'''
	Function that loads an animation curve into the keyframeOutliner
	'''
	
	
	
	try:	# run code, but catch errors
		
		# call the getAnimCurve function and assign result to curveName
		curveName = getAnimCurve( tsl )
		
		
		
		# check if animation curve exists for the selected attr
		if ( cmds.objExists( curveName ) ):
			
			# edit the keyframeOutliner to load the animation curve 
			cmds.keyframeOutliner( kOut, e=True, 
				animCurve=curveName )
			
			# edit the text to specify the animation curve
			cmds.text( 'curveTxt', e=True, l="Current Curve: " 
				+ curveName )
				
			popAnimMenu( tsl )
			
		else:	# no curve exists
			
			OpenMaya.MGlobal.displayWarning( "This attribute lacks an animation curve." )
			
			
	except TypeError:	# white space of TSL is being selected
		
		OpenMaya.MGlobal.displayWarning( "You have clicked in a blank space, please select an item." )
	
		
	selObj( dTSL.getName(), 0 )
	
	
	
def delAnim( tsl ):
	'''
	Function that deletes the entire animation curve from the selected attribute
	'''
	
	try:	# run code, but catch errors
	
		# call the getAnimCurve function and assign result to curveName
		curveName = getAnimCurve( tsl )
		
		# delete the animation curve
		cmds.delete( curveName )
		
	except TypeError:	# curve doesn't exist
		
		OpenMaya.MGlobal.displayWarning( "No animation curve exists to delete." )
	
	
	
def revAnim( tsl ):
	'''
	Function that deletes the entire animation curve from the selected attribute
	'''
	

		
	# create list to append to
	keyVals = [ ]
	
	try:	# run code, but catch errors
	
	
		# call the getAnimCurve function and assign result to curveName
		curveName = getAnimCurve( tsl )
		
		# query the number keyframes on the animation curve
		numKeys = cmds.keyframe( curveName, q=True, keyframeCount=True )
		
		# declare counter
		i = 0
		
		while ( i < numKeys ):
			
			# query the values for each index on the animation curve
			keyVals.append( cmds.keyframe( curveName, q=True, index=(i,i), valueChange=True ) )
			
			# increment counter
			i += 1
			
		# reverse the values list
		keyVals.reverse()
		
		
		# declare counter
		i = 0
		
		while ( i < numKeys ):
			
			newVal = keyVals[i]
			
			#keyframe -index 1 -absolute -valueChange -15 pCylinder1_translateX ;
			cmds.keyframe( curveName, index=(i,i), absolute=True, valueChange=newVal[0] )
			
			# increment counter
			i += 1
	
			#keyframe -option over -index 1 -absolute -floatChange 15 pCylinder1_translateX
			
		
	except TypeError:	# curve doesn't exist
		
		OpenMaya.MGlobal.displayWarning( "No animation curve exists to reverse." )
	
	
	
def delAnimIndex( val, tsl ):
	'''
	Function that deletes an index number of the animation curve from the selected attribute
	'''
	
	# call the getAnimCurve function and assign result to curveName
	curveName = getAnimCurve( tsl )
	
	# deletes the desired index of animation curve
	cmds.cutKey( curveName, index=(val,val) ) 
	
	# call the popAnimMenu function to rebuild the popupMenu
	popAnimMenu( tsl )
	
	
	
def popAnimMenu( tsl ):
	'''
	Function that updates the popupMenu to list and delete only the current numer of indexes on an animation curve
	'''
	
	# query selected item from the textScrollList
	selItem = cmds.textScrollList( tsl, q=True, selectItem=True )
	
	# query number of keyframes in animation curve
	animSize = cmds.keyframe( selItem[0], query=True, keyframeCount=True )
	
	
	# delete all the items from the popupMenu
	cmds.popupMenu( animIndexMenu, e=True, deleteAllItems=True )
	
	# add the universal items to the popupMenu
	cmds.menuItem( label="Del Index:", parent=animIndexMenu )
	cmds.menuItem( divider=True, parent=animIndexMenu )
	
	# declare counter
	i=0
	
	# add the required number of items to the popupMenu based on the index numbers from the animation curve
	while ( i < animSize ):
		
		#cmds.menuItem( label=str(i), parent=animIndexMenu, c=scriptName + ".delAnimIndex(%s, '%s')" %(i, dTSL.getName() ) )
		cmds.menuItem( label=str(i), parent=animIndexMenu, c= Callback( delAnimIndex, i, tsl ) )
		
		# increment counter
		i+=1



'''
	
	Set Driven Key animation curve types:
		
		translate = animCurveUL
		
		rotate = animCurveUA
		
		scale = animCurveUU
		
		visibility = animCurveUU
		
		custom = animCurveUU
	
		
	Key Selected animation curve types:
		
		translate = animCurveTL
		
		rotate = animCurveTA
		
		scale = animCurveTU
		
		visibility = animCurveTU
		
		custom = animCurveTU
		
		
/*


// clear keyFrame selection
selectKey -clear ;

// adds selection of keyframe at -1 frame value 
selectKey -add -k -f -1 pSphere2_translateX ;


// select the zero index of animation curve
selectKey -index 0 pSphere2_translateX ;




// deletes the selected keyFrame
cutKey -animation keys -clear;

// deletes the first index of animation curve
cutKey -index 1 pSphere2_translateX ;

keyframe -q -keyframeCount "pSphere2.tx" ;
cmds.keyframe( 'pSphere2.tx', query=True, keyframeCount=True )

*/


# query number of keyframes in animation curve
cmds.keyframe( 'pSphere2.tx', query=True, keyframeCount=True )

# deletes the first index of animation curve
cmds.cutKey( 'pSphere2_translateX', index=(1,1) ) 
		

// toggle changing color of animation curve
setAttr "pSphere2_translateX.useCurveColor" 1;

// change color of animation curve
setAttr "pSphere2_translateX.curveColor" -type double3 0.41406 0.41406 0.41406 ;


'''
