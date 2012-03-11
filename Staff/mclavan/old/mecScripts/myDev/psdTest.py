

import maya.cmds as cmds

class Stuff():
	def __init__(self, name):
		self.name = name
		
	def __add__(self, stuffB):
		return self.name + stuffB
		
	def __eq__(self, stuffB):
		return self.name == stuffB
		
	def __str__(self):
		return self.name

		
def pyexecglobal():
	exec( 'foo = 5' ) in globals()
	exec( 'foob = 5' ) in locals()
	print foo
	print foob
