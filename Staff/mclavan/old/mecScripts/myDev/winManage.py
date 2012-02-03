import maya.cmds as cmds
import maya.mel as mel

mel.eval( 'python("import sys")' )


class Callback():
	_callData = None
	def __init__(self,func,*args,**kwargs):
		self.func = func
		self.args = args
		self.kwargs = kwargs
	
	def __call__(self, *args):
		Callback._callData = (self.func, self.args, self.kwargs)
		mel.eval('global proc py_%s(){python("sys.modules[\'%s\'].Callback._doCall()");}'%(self.func.__name__, __name__))
		try:
			mel.eval('py_%s()'%self.func.__name__)
		except RuntimeError:
			pass
		
		if isinstance(Callback._callData, Exception):
			raise Callback._callData
		return Callback._callData 
	
	@staticmethod
	def _doCall():
		(func, args, kwargs) = Callback._callData
		Callback._callData = func(*args, **kwargs)

class MyWin(object):
	windows = []

	def __init__(self):
		self.win = cmds.window()
		
		# MyWin.windows = MyWin.windows + 1
		MyWin.windows.append(self.win)
		
		# cmds.scriptJob( uiDeleted=[self.win, self.updateAttr ])
		cmds.scriptJob( uiDeleted=[self.win, Callback( self.updateAttr2, self.win ) ])

	@staticmethod
	def killAll():
		print("All windows ternminated")
		for win in MyWin.windows:
			cmds.deleteUI(win)
			
	def updateAttr(self):
		MyWin.windows = MyWin.windows - 1

	def updateAttr2(self, winName):
		# MyWin.windows = MyWin.windows - 1
		print( "Deleting %s" %winName )
		MyWin.windows.remove(winName)
		
	def showWin(self):
		cmds.showWindow(self.win)
		
		
