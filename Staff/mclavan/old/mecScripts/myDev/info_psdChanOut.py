

cmds.window()
cmds.columnLayout()
psdWin = cmds.psdChannelOutliner(h=175, psdParent="mecMenu")
cmds.showWindow()

cmds.psdChannelOutliner( psdWin, e=True, psdParent="mecMenu", addChild=["MyScripts",""] )
cmds.psdChannelOutliner( psdWin, e=True, psdParent="mecMenu", addChild=["Rigging",""] )
cmds.psdChannelOutliner( psdWin, e=True, psdParent="mecMenu", addChild=["Modeling",""] )

cmds.psdChannelOutliner( psdWin, e=True, psdParent="Rigging", addChild=["Script1",""] )
cmds.psdChannelOutliner( psdWin, e=True, psdParent="Rigging", addChild=["Script2",""] )
cmds.psdChannelOutliner( psdWin, e=True, psdParent="Rigging", addChild=["Script3",""] )

cmds.psdChannelOutliner( psdWin, e=True, psdParent="MyScripts", addChild=["Script1",""] )
cmds.psdChannelOutliner( psdWin, e=True, psdParent="MyScripts", addChild=["Script2",""] )
cmds.psdChannelOutliner( psdWin, e=True, psdParent="MyScripts", addChild=["Script3",""] )


cmds.psdChannelOutliner( psdWin, e=True, psdParent="Script1", addChild=["Script1",""] )

# Getting selected element
cmds.psdChannelOutliner( psdWin, q=1, all=True )
# [u'MyScripts.Test1', u'MyScripts.Test2', u'MyScripts.Test3', u'Rigging.Script1', u'Rigging.Script2', u'Rigging.Script3', u'mecMenu.Modeling']
# Weird thing is that it has to be expanded to return the items.

# MyScripts was expanded on the first on while it wasn't on the second one.
cmds.psdChannelOutliner( psdWin, q=1, all=True )# Result: [u'MyScripts.Test1', u'MyScripts.Test2', u'MyScripts.Test3', u'Rigging.Script1', u'Rigging.Script2', u'Rigging.Script3', u'mecMenu.Modeling'] # 
cmds.psdChannelOutliner( psdWin, q=1, all=True )# Result: [u'Rigging.Script1', u'Rigging.Script2', u'Rigging.Script3', u'mecMenu.Modeling'] # 


selected = cmds.psdChannelOutliner( psdWin, q=1,  selectItem=True )
# # Result: [u'MyScripts.Test1', u'MyScripts.Test2', u'MyScripts.Test3', u'Rigging.Script1', u'Rigging.Script2', u'Rigging.Script3', u'mecMenu.Modeling']

cmds.psdChannelOutliner( psdWin, q=1, ni=True )

# There is an issue with this control
# selectItem will only return a leaf, if its a parent to something then it will be omitted.

class ChannelOutliner(object):
	'''
	Controls entries into the psdChannelOutliner.
	'''
	def __init__(self, rootName, width, height):
		self.gui = cmds.psdChannelOutliner( w=width, h=height, parent=rootName )
		self.root = rootName

		
		# self.items = {self.root:[None]}

	def addChild(self, name):
		
		
	def subChild

