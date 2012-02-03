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