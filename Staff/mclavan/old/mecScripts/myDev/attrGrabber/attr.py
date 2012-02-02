'''
attr.py

How to Run:
import attr
reload(attr)
'''
import os.path
import maya.cmds as cmds
import maya.mel as mel
from callback import Callback
import cPickle as pickle


# I might have to rethink this.  I might want a separate attribute class.
class Attr(object):
	'''
	Gets and stores the common information for an attribute.
	'''
	
	def __init__(self, attr, check=False):
		self.obj, self.attr = attr.split(".")
		self.fullObj = attr
		self.min = None
		self.max = None
		self.defValue = None
		self.offset = None
		self.dataType = None
		# self.enum
		self._standardAttrs = ['tx', 'translateX', 'ty', 'translateY', 'tz', 'translateZ', 
					'rx', 'rotateX', 'ry', 'rotateY', 'rz', 'rotateX', 
					'sx','scaleX', 'sy', 'scaleY', 'sz', 'scaleZ', 'v', 
					'visibility']

		self.gatherInfo()
		if(check):
			print( "Object: %s Attr: %s \n\t\tMin: %s Max: %s DefValue: %s Offset: %s DataType: %s" %(self.obj, self.attr, self.min, self.max, self.defValue, self.offset, self.dataType))
		
	
	def gatherInfo(self):
		if( self.attr in self._standardAttrs ):  # Attribute is apart of the main translates.
			# if there is a 
			attrTemp = cmds.attributeName( self.fullObj, short=True)
			if( attrTemp == 'v'):
				self.defValue = cmds.attributeQuery( 'v', node=self.obj, ld=True)[0]
				self.min = cmds.attributeQuery( 'v', node=self.obj, min=True)[0]
				self.max = cmds.attributeQuery( 'v', node=self.obj, max=True)[0]
				self.dataType = "long"
			else:
				enabledLimits = eval( "cmds.transformLimits( self.obj, q=True, e%s=True)" %attrTemp)
				if( enabledLimits[0] ):
					self.min = eval( "cmds.transformLimits( self.obj, q=True, %s=True)" %attrTemp)[0]
				if( enabledLimits[1] ):	
					self.max = eval( "cmds.transformLimits( self.obj, q=True, %s=True)" %attrTemp)[1]
				
				if( "s" in self.attr ): # Then we are at scale
					self.defValue = 1
				else:
					self.defValue = 0
				
				self.dataType = "double"
			# current value will be the offset			
			
			
		# What about a enum values?
		else: # Custom attributes
			if( cmds.attributeQuery( self.attr, node=self.obj, minExists=True) ):
				self.min = cmds.attributeQuery( self.attr, node=self.obj, min=True)[0]
			if( cmds.attributeQuery( self.attr, node=self.obj, maxExists=True) ):
				self.max = cmds.attributeQuery( self.attr, node=self.obj, max=True)[0]
			
			self.defValue = cmds.attributeQuery( self.attr, node=self.obj, listDefault=True)[0] 
			
			self.dataType = cmds.addAttr( self.fullObj, q=True, at=True)
			
		self.offset = cmds.getAttr( self.fullObj )
	
	def getValue( self ):
		return cmds.getAttr( self.fullObj )
		
	def setValue( self, value ):
		cmds.setAttr( self.fullObj, value )
		
	def keyframe( self ):
		cmds.setKeyframe( self.fullObj )
	def setOffset(self):
		self.offset = cmds.getAttr( self.fullObj )
	def getOffset(self):
		return self.offset
	def resetOffset(self):
		cmds.setAttr( self.fullObj, self.offset )
		
	def reset(self):
		cmds.setAttr( self.fullObj, self.defValue )
	def getReset(self):
		return self.defValue
		

class AttrGUI(object):
	'''
	Creates an interface to connect to attributes.
	Optional button include:
		keyframming attributes
		resetting back to default value
		creating a offset
		resetting back to offset
	'''

	# def __init__(self, text, parent=None, attrs=[]):  #, key=True, reset=True, offset=True, resetOffset=True
	def __init__(self, text, attrs, parent=None):  #, key=True, reset=True, offset=True, resetOffset=True
		self.attrNames = attrs
		self.parent = parent
		self.text = text
		# self.attrs = [Attr(attr) for attr in attrs ]
		self.attrs = Attr(self.attrNames)
	"""
	def gui(self):
		
		self._ctrls = []
		self.mainLayout = cmds.formLayout()
		
		# Determine if it needs a slider or field
		# One of Multiple fields.
		
		'''
		# Is it going to be a float or intSliderGrp
		if( attrs[0].dataType == "long"):
			# self.slider = cmds.intSliderGrp( 
		elif( attrs[0].dataType == "double"):  # Its a float control
			# self.slider = cmds.floatSliderGrp( label=self.text
		# elif( attrs[0].dataType == "enum")
		cmds.button( label="Reset", 
			command= Callback( attrs[0].reset ) )
		cmds.button( label="Offset",
			command= Callback( attrs[0].setOffset, cmds.getAttr(attrs[0].fullObj) ))
		cmds.button( label="OffReset",
			command= Callback( attrs[0].resetOffset() )
		cmds.connectControl( self.slider, self.attrNames )
		'''
	"""
	# What type of gui component are we to make.
	
		
class AttrGroup(object):
	'''
	This class groups together attributes using the AttrGUISingle class.
	By default this group starts out with no attributes but is added as the user wills it.
	attrs (groups of instances from the AttrGUISingle class)
	mainLayout (name of the main layout for the gui)
	layouts (all the layouts being controlled by this class)
	Arguments:
		attrNames(string list) contains attr name and its text
			[ [attrName, attrText],[attrName2, attrText] ]
			or
			[attrName1, attrName2, etc...]
			attrName will be the object.attr
		parent (string) object to parent this system to.
		
	attrs = AttrGroup( ["object.attr", "object.attr", "object.attr", etc...], "layoutName" )
	or
	attrs = AttrGroup( [["object.attr", "attrName"],["object.attr", "attrName"], etc...], "layoutName" )
	'''
	def __init__(self, parent):  # attrs,
		self.parent = parent
		# self.attrs = attrs
		# list of attribute names ["object.attr"]
		self.attrs = []
		# list of AttrGUISingle object
		self.attrObj = []
		# self.layouts = []
		self.mainLayout = cmds.formLayout( parent=self.parent )


	
	
	def removeAll( self ):
		for attr in self.attrObj:
			attr.remove()
		
		self.attrs = []
		self.attrObj = []
	
	# Reset All, Key All, 	
	
	def offsetValue( self, value ):
		for attr in self.attrObj:
			attr.offsetVal(value)

	def setCurOffset( self ):
		for attr in self.attrObj:
			attr.setCurOffset()			
			
	def resetAll( self ):
		for attr in self.attrObj:
			attr.reset()
	
	def keyAll( self ):
		for attr in self.attrObj:
			attr.key()
			
	def setOffset( self ):
		for attr in self.attrObj:
			attr.setOffset()
	
	def resetOffset( self ):
		for attr in self.attrObj:
			attr.resetOffset()
			
	def addAttr(self, attr):
		'''
		Adds an attribute to the system
		'''
		self.attrs.append( attr )
		attrObj = AttrGUISingle( attr, attr, self.mainLayout )
		# Positioning in formLayout
		if( self.attrObj ):
			cmds.formLayout( self.mainLayout, edit=1, af=[attrObj.mainLayout, "left", 0],
				ac=[attrObj.mainLayout, "top", 0, self.attrObj[-1].mainLayout])	
		else:		
			cmds.formLayout( self.mainLayout, edit=1, af=[[attrObj.mainLayout, "top", 0],[attrObj.mainLayout, "left", 0]])
		
		self.attrObj.append( attrObj )
		
	def addAttrs(self, attrs):
		'''
		Adds multiple attributes to the system
		'''
		self.attrs.extend( attrs )
		
		for i, attr in enumerate(attrs):
			attrObj = AttrGUISingle( attr, attr, self.mainLayout )
					
			# Positioning in formLayout
			if( self.attrObj ):
				cmds.formLayout( self.mainLayout, edit=1, af=[attrObj.mainLayout, "left", 0],
					ac=[attrObj.mainLayout, "top", 0, self.attrObj[-1].mainLayout])	
			else:
				cmds.formLayout( self.mainLayout, edit=1, af=[[attrObj.mainLayout, "top", 0],[attrObj.mainLayout, "left", 0]])
			
			self.attrObj.append( attrObj )
	
			
	def guiInfo(self):
		radioChoice = cmds.radioButtonGrp( self.rbtn, q=True, sl=True)
		txt = cmds.textFieldGrp( self.txt, q=True, tx=True)
		
		if( radioChoice == 1 ):  # ChannelBox
			sma = cmds.channelBox("mainChannelBox", q=True, sma=True)
			ssa = cmds.channelBox("mainChannelBox", q=True, selectedShapeAttributes=True)
			sha = cmds.channelBox("mainChannelBox", q=True, selectedHistoryAttributes=True)
			selected = cmds.ls(sl=True)
			
			allAttrs = []
			if( sma ):
				allAttrs.extend(sma)
			if( ssa ):
				allAttrs.extend(ssa)
			if( sha ):
				allAttrs.extend(sha)

			curAttrs = []
			for sel in selected:
				for attr in allAttrs:
					obj = "%s.%s" %(sel, attr)
					if( cmds.objExists( obj ) ):
						# print( "Object: %s" %(obj))
						curAttrs.append( obj )
			
			self.addAttrs( curAttrs )
		else:
			if( cmds.objExists(txt) ):
				self.addAttr( txt )
			
			
			
	def addAttrGUI(self):
		win = "attrInfoWin"
		
		if( cmds.window(win, ex=True) ):
			cmds.deleteUI(win)
		if( cmds.windowPref(win, ex=True) ):
			cmds.windowPref( win, r=True )
			
		cmds.window(win, title="Add Attribute", w=300, h=87)
		
		# mainCol = cmds.columnLayout(rs=5)
		mainFrm = cmds.formLayout()
		# cmds.rowColumnLayout(nc=2, cw=[[1,175],[2,100]])
		self.rbtn = cmds.radioButtonGrp( nrb=2, labelArray2=["ChannelBox","Custom"],
			cw=[[1,100],[2,75]], sl=1)
		self.txt = cmds.textFieldGrp( w=100, text="object.attribute" )
		btn = cmds.button(label="Apply", w=275,
			c=Callback( self.guiInfo ))
		cmds.formLayout( mainFrm, e=1, af=[[self.rbtn, "left", 5],[self.rbtn, "top", 5]] )
		cmds.formLayout( mainFrm, e=1, af=[self.txt, "top", 3], ac=[self.txt , "left", 0, self.rbtn] )
		cmds.formLayout( mainFrm, e=1, af=[btn, "left", 5], ac=[btn , "top", 3, self.rbtn] )
		
		cmds.showWindow(win)

		
'''
import characterGUI.attr as attr
reload(attr)

win = cmds.window()
mainCol = cmds.columnLayout()
attrGUI = attr.AttrGroup(mainCol)
cmds.showWindow(win)


attrGUI.addAttrGUI()
attrGUI.offsetValue( 2 )
attrGUI.removeAll()
attrGUI.resetAll()

cmds.window()
cmds.columnLayout()
slider = cmds.floatSliderGrp( label="Main Offset", field=1,
	cc=changeVal, dc=changeVal, min=-10, max=10 )

cmds.showWindow()

def changeVal(*args):
	value = cmds.floatSliderGrp( slider, q=True, value=True)
	attrGUI.offsetValue( value )

def resetSlider():
	attrGUI.setCurOffset()
	cmds.floatSliderGrp( slider, e=True, value=0)
'''
		
'''
cmds.window()
mainCol = cmds.columnLayout()
attrs =  attr.AttrGroup(mainCol )
cmds.showWindow()
attrs.addAttr( 'pSphere1.ty' )
attrs.addAttrs(["blendShape1.pSphere2", "blendShape1.pSphere3", "blendShape1.pSphere4"] )
'''

class FrameGroup(AttrGroup):
	def __init__(self, parent, name="Attr Info", mixer=1, attrs=[]):
	
		self.frameName = name
		self.mainFrame = cmds.frameLayout( parent=parent, cll=True, label=name )
		# self.mainScroll = cmds.scrollLayout()
		self.mainFrm = cmds.formLayout( parent=self.mainFrame )
		
		topWidgit = self._manipWidgit(self.mainFrm)
		
		AttrGroup.__init__(self, self.mainFrm)
		
		
		# Creating the gui elements above the attributes
		# Add & Remove
		
		# self.attrGrp = AttrGroup( self.mainFrm )
		
		# Mixer elements at the bottom
		# bottomWidgit = self._mixerWidgit( self.mainFrm )
		
		# Positioning the widgits
		cmds.formLayout( self.mainFrm, e=1, af=[[topWidgit, "top", 2],[topWidgit, "left", 5]])
		cmds.formLayout( self.mainFrm, e=1, af=[self.mainLayout, "left", 5], 
		                 ac=[self.mainLayout, "top", 5, topWidgit])
		
		if( mixer ):
			mixer = self._mixerGUI(self.mainFrm)
			cmds.formLayout( self.mainFrm, e=1, af=[mixer, "left", 5], 
						 ac=[mixer, "top", 5, self.mainLayout])
        
	def _manipWidgit(self, curParent):
		'''
		This gui widgit contains the buttons to add & remove attributes
		Overall adjusts for all the attribute contained inside.
		'''
		frame = cmds.frameLayout(parent=curParent, labelVisible=False, marginWidth=5, marginHeight=3)
		frm = cmds.formLayout( parent=frame, w=415 )

		path = os.path.split(__file__)[0]
		fullPath = lambda x : os.path.join( path, "icons", x )
		
		btn1 = cmds.symbolButton( image=fullPath('plus_16b.xpm'), h=20, 
		                    command=Callback(self.addAttrGUI)) # self._attrGUI )
		
		btn2 = cmds.symbolButton( image=fullPath('delete_16b.xpm'), h=20, 
		                    command=Callback(self.removeAll ))#command=self._removeAttrs )
		                 
		btn2a = cmds.symbolButton( image=fullPath('save_16.xpm'), h=20, 
		                    command=Callback(self.addAttrGUI)) # self._attrGUI )
		btn2b = cmds.symbolButton( image=fullPath('folder_16b.xpm'), h=20, 
		                    command=Callback(self.addAttrGUI)) # self._attrGUI )	
		                    
		cmds.formLayout( frm, e=1, af=[[btn1, "left", 5],[btn1, "top", 0]])
		cmds.formLayout( frm, e=1, ac=[btn2, "left", 5, btn1], af=[btn2, "top", 0])		                    
		cmds.formLayout( frm, e=1, ac=[btn2a, "left", 5, btn2], af=[btn2a, "top", 0])	
		cmds.formLayout( frm, e=1, ac=[btn2b, "left", 5, btn2a], af=[btn2b, "top", 0])	
		
		'''		                    
		btn1 = cmds.button( label="Add Attr", w=100,
		                    command=Callback(self.addAttrGUI)) # self._attrGUI )
		
		btn2 = cmds.button( label="Remove Attrs", w=100,
		                    command=Callback(self.removeAll ))#command=self._removeAttrs )
		'''
		
		btn3 = cmds.symbolButton(image='MENUICONKEYS.XPM', h=20,
			ann="Keyframe", command=Callback(self.keyAll))
		'''		
		btn3 = cmds.button( label="Keyframe",
						    command=Callback(self.keyAll))
		'''				    
		btn4 = cmds.symbolButton(image='REDRAWPAINTEFFECTS.XPM', h=20,
			ann="Reset to Default", 
			command=Callback(self.resetAll))
		
		btn5 = cmds.symbolCheckBox( image='ONRADIOBTNICON.XPM', h=20,
			oni='ONRADIOBTNICON.XPM',
			ofi='OFFRADIOBTNICON.XPM',
			ann="Set Offset", 
			onc=Callback(self.setOffset))
		
		btn6 = cmds.symbolButton(image='AUTOLOAD.XPM', h=20,
			ann="Reset Offset", 
			command=Callback(self.resetOffset))
		


		'''
		cmds.formLayout( frm, e=1, ac=[btn3, "left", 5, btn2], af=[btn3, "top", 0])
		cmds.formLayout( frm, e=1, ac=[btn4, "left", 5, btn3], af=[btn4, "top", 0])
		cmds.formLayout( frm, e=1, ac=[btn5, "left", 5, btn4], af=[btn5, "top", 0])
		cmds.formLayout( frm, e=1, ac=[btn6, "left", 5, btn5], af=[btn6, "top", 0])
		'''
		cmds.formLayout( frm, e=1, af=[[btn6, "top", 0], [btn6, "right", 5]])
		cmds.formLayout( frm, e=1, ac=[btn5, "right", 5, btn6], af=[btn5, "top", 0])
		cmds.formLayout( frm, e=1, ac=[btn4, "right", 5, btn5], af=[btn4, "top", 0])
		cmds.formLayout( frm, e=1, ac=[btn3, "right", 5, btn4], af=[btn3, "top", 0])
		
		return frame
	
	def _mixerGUI(self, currParent):
	
		frame = cmds.frameLayout( parent=currParent, lv=0, marginWidth=5, marginHeight=3 )
		frm = cmds.formLayout( parent=frame )
		self.mSlider = cmds.floatSliderGrp( field=1, label="Attribute Mixer", cw=[1,75],
						cc=self.changeVal, dc=self.changeVal, min=-10, max=10, step=.1 )
		btn1 = cmds.button( label="Reset", w=50,
					    c=Callback(self.resetSlider))
		# btn2 = cmds.button( label="Offset", w=50)
		
		cmds.formLayout( frm, e=1, af=[[self.mSlider, "left", 5],[self.mSlider, "top", 0]])
		cmds.formLayout( frm, e=1, ac=[btn1, "left", 5, self.mSlider], af=[btn1, "top", 0])
		# cmds.formLayout( frm, e=1, ac=[btn2, "left", 5, btn1], af=[btn2, "top", 0])
		
		return frame
		
	def changeVal(self, *args):
		value = cmds.floatSliderGrp( self.mSlider, q=True, value=True)
		self.offsetValue( value )
	
	def resetSlider(self, *args):
		self.setCurOffset()
		cmds.floatSliderGrp( self.mSlider, e=True, value=0) 
		
	def _attrGUI(self, *args):
		self.attrGrp.addAttrGUI()
	
	def _removeAttrs(self, *args):
		self.attrGrp.removeAll()
	    
	def _mixerWidgit(self, curParent):
		'''
		This gui widgit contain the mixer elements.
		Adjusting all the attributes from one slider
		Options such as keyframe All, Reset Offset All, & Reset All exist
		'''
		frm = cmds.formLayout( parent=curParent)
		
		
		return frm
        
class FrameGroupOld(object):
	def __init__(self, parent, name="Attr Info", mixer=1, attrs=[]):
	
		self.mainFrame = cmds.frameLayout( parent=parent, cll=True, label=name )
		# self.mainScroll = cmds.scrollLayout()
		self.mainFrm = cmds.formLayout( parent=self.mainFrame )
		
		topWidgit = self._manipWidgit(self.mainFrm)
		# Creating the gui elements above the attributes
		# Add & Remove
		
		self.attrGrp = AttrGroup( self.mainFrm )
		
		# Mixer elements at the bottom
		# bottomWidgit = self._mixerWidgit( self.mainFrm )
		
		# Positioning the widgits
		cmds.formLayout( self.mainFrm, e=1, af=[[topWidgit, "top", 2],[topWidgit, "left", 5]])
		cmds.formLayout( self.mainFrm, e=1, af=[self.attrGrp.mainLayout, "left", 5], 
		                 ac=[self.attrGrp.mainLayout, "top", 5, topWidgit])
		
		if( mixer ):
			mixer = self._mixerGUI(self.mainFrm)
			cmds.formLayout( self.mainFrm, e=1, af=[mixer, "left", 5], 
						 ac=[mixer, "top", 5, self.attrGrp.mainLayout])
        
	def _manipWidgit(self, curParent):
		'''
		This gui widgit contains the buttons to add & remove attributes
		Overall adjusts for all the attribute contained inside.
		'''
		frame = cmds.frameLayout(parent=curParent, labelVisible=False, marginWidth=5, marginHeight=3)
		frm = cmds.formLayout( parent=frame )
		btn1 = cmds.button( label="Add Attr", w=100,
		                    command=self._attrGUI )
		btn2 = cmds.button( label="Remove Attrs", w=100,
		                    command=self._removeAttrs )
		btn3 = cmds.button( label="Keyframe")
		btn4 = cmds.button( label="Reset")
		btn5 = cmds.button( label="Offset")
		btn6 = cmds.button( label="Reset Offset")
		
		cmds.formLayout( frm, e=1, af=[[btn1, "left", 5],[btn1, "top", 0]])
		cmds.formLayout( frm, e=1, ac=[btn2, "left", 5, btn1], af=[btn2, "top", 0])
		cmds.formLayout( frm, e=1, ac=[btn3, "left", 5, btn2], af=[btn3, "top", 0])
		cmds.formLayout( frm, e=1, ac=[btn4, "left", 5, btn3], af=[btn4, "top", 0])
		cmds.formLayout( frm, e=1, ac=[btn5, "left", 5, btn4], af=[btn5, "top", 0])
		cmds.formLayout( frm, e=1, ac=[btn6, "left", 5, btn5], af=[btn6, "top", 0])
		
		return frame
	
	def _mixerGUI(self, currParent):
	
		frame = cmds.frameLayout( parent=currParent, lv=0, marginWidth=5, marginHeight=3 )
		frm = cmds.formLayout( parent=frame )
		self.mSlider = cmds.floatSliderGrp( field=1, label="Attribute Mixer", cw=[1,75],
						cc=self.changeVal, dc=self.changeVal, min=-10, max=10, step=.1 )
		btn1 = cmds.button( label="Reset", w=50,
					    c=self.resetSlider)
		btn2 = cmds.button( label="Offset", w=50)
		
		cmds.formLayout( frm, e=1, af=[[self.mSlider, "left", 5],[self.mSlider, "top", 0]])
		cmds.formLayout( frm, e=1, ac=[btn1, "left", 5, self.mSlider], af=[btn1, "top", 0])
		cmds.formLayout( frm, e=1, ac=[btn2, "left", 5, btn1], af=[btn2, "top", 0])
		
		return frame
		
	def changeVal(self, *args):
		value = cmds.floatSliderGrp( self.mSlider, q=True, value=True)
		self.attrGrp.offsetValue( value )
	
	def resetSlider(self, *args):
		self.attrGrp.setCurOffset()
		cmds.floatSliderGrp( self.mSlider, e=True, value=0) 
		
	def _attrGUI(self, *args):
		self.attrGrp.addAttrGUI()
	
	def _removeAttrs(self, *args):
		self.attrGrp.removeAll()
	    
	def _mixerWidgit(self, curParent):
		'''
		This gui widgit contain the mixer elements.
		Adjusting all the attributes from one slider
		Options such as keyframe All, Reset Offset All, & Reset All exist
		'''
		frm = cmds.formLayout( parent=curParent)
		
		
		return frm
	  
class TabGroup(object):
    def __init__(self, parent):
        self.parent = parent
        self.mainTab = cmds.tabLayout( parent=self.parent)
                
        self.tabNames = []
        self.tabs = {}
        
        
        # 
        
    '''
    Tab info should be able to be save ether by selected tab or all tabs
    '''
    
    '''
    Tabs should be able to be created by file 
    
    File
        - Load Tabs (Clears Current adds from File)
        - Add Tab(s) (from File)
        - Add Tab (blank)
        - Add Frame (from File)
        - Add Frame (blank)
        - Save Tab (to File)
        - Save All Tabs (to File)
        - Remove Selected Tabs
        - Remove All Tabs
        
    '''
    def addTabPrompt(self):
    	
		result = cmds.promptDialog(
				title='Add Tab',
				message='Enter Tab Name:',
				button=['OK', 'Cancel'],
				defaultButton='OK',
				cancelButton='Cancel',
				dismissString='Cancel')
		
		if result == 'OK':
			text = cmds.promptDialog(query=True, text=True)
	    	self._addTab(text)

    def addFramePrompt(self):
    	if(self.tabNames):
			result = cmds.promptDialog(
					title='Add Frame',
					message='Enter Frame Name:',
					button=['OK', 'Cancel'],
					defaultButton='OK',
					cancelButton='Cancel',
					dismissString='Cancel')
			
			if( result == 'OK' ):
				text = cmds.promptDialog(query=True, text=True)
		    	self._addFrame(text)
    	else:
    		print( "Base Tab doesn't exist.")
    		
    def _removeTab(self):
    	currTab = cmds.tabLayout( self.mainTab, q=True, selectTab=True)
    	tabIndex = cmds.tabLayout( self.mainTab, q=True, selectTabIndex=True) - 1 # tab index are 1 based.
    	# Find list item for tab
    	# Remove from list
    	# Remove from dictionary
    	# Remove ui
    	print( "Deleting: %s %s" %(currTab, tabIndex))
    	print( self.tabNames )
    	print( self.tabs )
    	cmds.deleteUI(self.tabNames[tabIndex] )
	del self.tabs[self.tabNames[tabIndex]]
	self.tabNames.pop(tabIndex)
    '''	
    def _saveFrame(self):
	
    def _loadFrame(self):
    '''	
    def _saveTab(self):
	'''
	The name of the tab 
	The frames included
	the attributes for each frame
	'''
	
	# Prompt where to save the file.

	# pack data
	

    	currTab = cmds.tabLayout( self.mainTab, q=True, selectTab=True)
    	tabIndex = cmds.tabLayout( self.mainTab, q=True, selectTabIndex=True) - 1 # tab index are 1 based.
	tabLabels = cmds.tabLayout( self.mainTab, q=True, tl=True )
	
	tabName = tabLabels[tabIndex]
	frameNames = []	
	frames = {}

	
	for frameInfo in self.tabs[self.tabNames[tabIndex]]:
		frameNames.append([frameInfo.frameName, frameInfo.mainLayout])
		frames[frameInfo.mainLayout] = frameInfo.attrs
	
	path = cmds.fileDialog(mode=1)
	if(path):
		fileInfo = open( path, "w" )
		pickle.dump( tabName, fileInfo  )
		pickle.dump( frameNames, fileInfo )
		pickle.dump( frames, fileInfo )
		fileInfo.close()
	else:
		print("Save Cancelled.")
	
    def _loadTab(self):
    	    
    	    print("Load Tab")
    	    
    	    path = cmds.fileDialog( mode=0)
    	    # load
    	    if( path ):
    	    	    # Reading fileInfo
		    fileInfo = open( path, "r" )
		    tabName = pickle.load( fileInfo )
		    frameNames = pickle.load( fileInfo )
		    frames = pickle.load( fileInfo )
		    fileInfo.close()
		        
		    # Create Tab with tabname
		    tab = self._addTab( tabName )
		    for frame in frameNames:
		    	# frame[0]  the name of the frame
		    	# frame[1] is the layoutName (this is done so the dictionary doesn't get overlap)
		   	# frameGrp = self._addFrame( frame[0] )
		   	
		   	newAttr = FrameGroup( tab , frame[0] )
		   	self.tabs[self.tabNames[-1]].append( newAttr )
		   	
			for attrItem in frames[frame[1]]:
		   		if( cmds.objExists(attrItem) ):
		   			newAttr.addAttr( attrItem )
		    '''
		    print(tabName)
		    print(frameNames)
		    print(frames)
		    '''
    	    else:
    	    	    print("Load Cancelled.")
    	    	    

	    
    def _addTab(self, name):
        '''
        Adds an additional tab to the system.
        '''
        
        # Make sure that a tab exists!
        # scroll = cmds.scrollLayout( h=450, parent=self.mainTab )       
        col = cmds.columnLayout(parent=self.mainTab)

        frm = cmds.formLayout( w=450 )
        path = os.path.split(__file__)[0]
	fullPath = lambda x : os.path.join( path, "icons", x )
	
	btn1 = cmds.symbolButton( image=fullPath('plus_16b.xpm'), h=20, 
			    command=Callback(self.addFramePrompt)) # self._attrGUI )
	
	btn2 = cmds.symbolButton( image=fullPath('delete_16b.xpm'), h=20, 
			    command=Callback(self._removeTab ))#command=self._removeAttrs )
			 
	btn3 = cmds.symbolButton( image=fullPath('save_16.xpm'), h=20, 
			    command=Callback(self._saveTab)) # self._attrGUI )
        
	txt = cmds.text( l="" )
	
	cmds.formLayout( frm, e=1, af=[[btn1, "top", 5],[btn1, "left", 5], [btn2, "top", 5],[btn3, "top", 5], [txt, "top", 5], [txt, "right", 0]],
		ac=[[btn2, "left", 0, btn1],[btn3, "left", 0, btn2]])
        cmds.setParent( col )
        # frm = cmds.formLayout( parent=self.mainTab, w=300, h=300 )
        
        
        cmds.tabLayout( self.mainTab, e=1, tl=[col, name])
        self.tabs[col] = []
        self.tabNames.append(col)
        return col
        
    
    def _addFrame(self, name, mixer=1):
        '''
        Adds a attrframe into the tab system. 
        '''   
        if( self.tabNames ):     
	        # Adds under the current tab selected
	        
	        # Tab index is starts at 1
	        tabIndex = cmds.tabLayout( self.mainTab, q=1, selectTabIndex=True) - 1
	        
	        currentTab = self.tabNames[tabIndex]
	        
	        attr = FrameGroup( currentTab , name, mixer )
	        self.tabs[currentTab].append( attr )
        
        # frm = cmds.formLayout( parent=currentTab)
        # attr = FrameGroup(frm, "TestAttr")
        
        
        
        return attr
      
class AttrGroupGUI(AttrGroup):
	'''
	This class groups together attributes provided by the user.
	attrs (groups of instances from the AttrGUISingle class)
	mainLayout (name of the main layout for the gui)
	layouts (all the layouts being controlled by this class)
	Arguments:
		attrNames(string list) contains attr name and its text
			[ [attrName, attrText],[attrName2, attrText] ]
			or
			[attrName1, attrName2, etc...]
			attrName will be the object.attr
		parent (string) object to parent this system to.
		
	attrs = AttrGroup( ["object.attr", "object.attr", "object.attr", etc...], "layoutName" )
	or
	attrs = AttrGroup( [["object.attr", "attrName"],["object.attr", "attrName"], etc...], "layoutName" )
	'''
	def __init__(self, attrs, parent):
		AttrGroup.__init__(self, parent)
		self.attrs = attrs
		self.attrGUI()		

	
	def attrGUI(self):
		
		# Create the component and position it in the layout
		for i, attr in enumerate(self.attrs):
			attrObj = ""
			if( type(attr) is list ):
				attrObj = AttrGUISingle( attr[1], attr[0], self.mainLayout )
			else:
				attrObj = AttrGUISingle( attr, attr, self.mainLayout )
			
			# Positioning in formLayout
			if( i == 0 ):
				cmds.formLayout( self.mainLayout, edit=1, af=[[attrObj.mainLayout, "top", 0],[attrObj.mainLayout, "left", 0]])
			else:
				cmds.formLayout( self.mainLayout, edit=1, af=[attrObj.mainLayout, "left", 0],
					ac=[attrObj.mainLayout, "top", 0, self.attrObj[-1].mainLayout])
			
			self.attrObj.append( attrObj )	
			
'''

import maya.cmds as cmds
import characterGUI.attr as attr
reload( attr )

cmds.window()
mainCol = cmds.columnLayout()
attrs = attr.AttrGroupGUI( [["blendShape1.pSphere2",'Smile'], ["blendShape1.pSphere3", 'Frown'], "blendShape1.pSphere4"], mainCol )
cmds.showWindow()

attrs.addAttr( "polySphere1.subdivisionsAxis" )
attrs.addAttrGUI()

attrs2 = attr.AttrGroup( ['pSphere1.tx', 'pSphere1.ty'], mainCol )

'''


	
class AttrGUISingle(AttrGUI):
	def __init__(self, text, attrs, parent=None, offsetValue=0, offsetState=0):
		'''
		Inherited from AttrGUI
		self.attrNames = attrs
		self.parent = parent
		self.text = text
		# self.attrs = [Attr(attr) for attr in attrs ]
		self.attrs = Attr(self.attrNames)
		'''
		
		AttrGUI.__init__(self, text, attrs, parent )
		self.offsetValue = offsetValue
		self.offsetState = offsetState
		self.gui()
	
	
	def gui(self):
		'''
		Generates the interface for the AttrGUISingle object.
		'''
				
		btnWidth = 30
		btnSep = 2
		# textWidth = 70
		# fieldWidth
		# if( cmds.about( os=True ) == "mac" ):
			
		self.mainLayout = cmds.rowColumnLayout(parent=self.parent, nc=7, h=20, 
			rat=[[1,"both", btnSep ],[2,"both", btnSep ],[3,"both", btnSep ],[4,"both", btnSep ],[5,"both", btnSep ],[6,"both", btnSep ],[7,"both", btnSep ]],
			cw=[[1,100],[2,70],[3,125],[4, btnWidth ],[5,btnWidth ],[6,btnWidth ],[7,btnWidth ]])
		cmds.text(label=self.text, w=70, al="center")
		self.fieldGui = cmds.floatField( w=100, pre=2 )	
		pop = cmds.popupMenu(parent=self.fieldGui)
		cmds.menuItem(parent=pop, label="0 - 1", c=Callback( self.setMinMax, 0, 1))
		cmds.menuItem(parent=pop, label="0 - 10", c=Callback( self.setMinMax, 0, 10))
		cmds.menuItem(parent=pop, label="-10 - 10", c=Callback( self.setMinMax, -10, 10))		
		cmds.menuItem(parent=pop, label="Set Min/Max")
		cmds.menuItem( divider=1)
		cmds.menuItem(label="Step 1", c=Callback( self.setStep, 1 ))
		cmds.menuItem(label="Step .1", c=Callback( self.setStep, .1 ))
		cmds.menuItem(label="Step .01", c=Callback( self.setStep, .01 ))

		
		self.sliderGui = cmds.floatSlider( w=100, h=20)

		cmds.popupMenu(parent=self.sliderGui)
		cmds.menuItem(label="0 - 1", c=Callback( self.setMinMax, 0, 1))
		cmds.menuItem(label="0 - 10", c=Callback( self.setMinMax, 0, 10))
		cmds.menuItem(label="-10 - 10", c=Callback( self.setMinMax, -10, 10))		
		cmds.menuItem(label="Set Min/Max")
		cmds.menuItem( divider=1)
		cmds.menuItem(label="Step 1", c=Callback( self.setStep, 1 ))
		cmds.menuItem(label="Step .1", c=Callback( self.setStep, .1 ))
		cmds.menuItem(label="Step .01", c=Callback( self.setStep, .01 ))

		
		if( self.attrs.min != None ):
			cmds.floatField( self.fieldGui, e=1, min=self.attrs.min )
			cmds.floatSlider( self.sliderGui, e=1, min=self.attrs.min )
		if( self.attrs.max != None ):
			cmds.floatField( self.fieldGui, e=1, max=self.attrs.max )
			cmds.floatSlider( self.sliderGui, e=1, max=self.attrs.max )
			
		cmds.connectControl( self.fieldGui, self.attrNames )
		cmds.connectControl( self.sliderGui, self.attrNames )
		
		cmds.symbolButton(image='MENUICONKEYS.XPM', h=20,
			ann="Keyframe",
			command=Callback(self.key))
		cmds.symbolButton(image='REDRAWPAINTEFFECTS.XPM', h=20,
			ann="Reset to Default",
			command=Callback(self.reset))
		self.symGUI = cmds.symbolCheckBox( image='ONRADIOBTNICON.XPM', h=20,
			oni='ONRADIOBTNICON.XPM',
			ofi='OFFRADIOBTNICON.XPM',
			ann="Set Offset",
			onc=Callback(self.setOffset))
		self.resOffName = cmds.symbolButton(image='AUTOLOAD.XPM', h=20,
			ann="Reset Offset", 
			command=Callback( self.resetOffset ) )
		
		cmds.setParent(self.parent)

	def remove(self):
		cmds.deleteUI(self.mainLayout)
		
	def setCurOffset(self):
		self.offsetValue = self.attrs.getValue()
		
	def offsetVal(self, value):	
		self.attrs.setValue( value + self.offsetValue )
		
	def reset(self):
		self.attrs.reset()
		
	def key(self):
		self.attrs.keyframe()
		
	def setOffset(self):
		self.attrs.setOffset()
		cmds.symbolCheckBox( self.symGUI, e=1, v=1 )
	
	def resetOffset(self):
		self.attrs.resetOffset()
		
		
	def setMin(self, value):
		cmds.floatField( self.fieldGui, e=1, min=value)
		cmds.floatSlider( self.sliderGui, e=1, min=value)
		
	def setMax(self, value):
		cmds.floatField( self.fieldGui, e=1, max=value)
		cmds.floatSlider( self.sliderGui, e=1, max=value)	
	
	def setMinMax(self, valueMin, valueMax):
		self.setMin(valueMin)
		self.setMax(valueMax)
	
	def setStep(self, stepValue):
		cmds.floatField( self.fieldGui, e=1, step=stepValue)
		cmds.floatSlider( self.sliderGui, e=1, step=stepValue)			
		
	
			
'''
import characterGUI.attr as attr
reload( attr )

cmds.window()
mainCol = cmds.columnLayout()

btn1 = attr.AttrGUISingle( "transX", 'pSphere1.tx', mainCol )
btn1 = attr.AttrGUISingle( "transY", 'pSphere1.ty', mainCol )
btn1 = attr.AttrGUISingle( "Vis", 'pSphere1.v', mainCol )
btn1 = attr.AttrGUISingle( "polySphere1.subdivisionsAxis", "polySphere1.subdivisionsAxis", mainCol )
btn1 = attr.AttrGUISingle( "Vis", "pointLightShape1.intensity", mainCol )

cmds.showWindow()
'''


'''
cmds.window()
cmds.columnLayout()
slider = cmds.floatSliderGrp( label="trans", field=True, v=0 )
cmds.connectControl( slider, ["joint1.tx", "joint1.ty", "joint1.tz"])
cmds.showWindow()
'''