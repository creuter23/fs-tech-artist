import maya.cmds as cmds
import maya.OpenMaya as api

class Object(api.MObject, object):
	'''A wraper for maya.OpenMaya's MObject base class'''
	def __init__(self, mObject=None):
		'''Create a new Object based on maya's MObject Class'''
		if isinstance(mObject, basestring):
			#if it's a string, convert it to an MObject using an MSelectionList
			super(Object, self).__init__()
			selection = api.MSelectionList()
			selection.add(mObject)
			selection.getDependNode(0, self)
		else:
			#if it's an Object or MObject, create a new Object from it
			if mObject:
				super(Object, self).__init__(mObject)
			else:
				#if it's a null object, create an empty Object from it
				super(Object, self).__init__()
	
	def __str__(self):
		'''string representation of this object'''
		object = '<<Object %s %s>>'%(self.apiType, self.name)
		return object
	
	def __repr__(self):
		return str(self)
		
	def _getName(self):
		'''Return the current object name(unique) as a string'''
		if self.isNull():
			return 'None'
		selection = api.MSelectionList()
		selection.add(self)
		name = []
		selection.getSelectionStrings(0, name)
		return name[0]
	
	def _setName(self, newName):
		'''Set the name of the object to a new string'''
		cmds.rename(self.name, newName)
	
	name = property(_getName, _setName)
		
	@property
	def apiType(self):
		'''Return the base type of the object as a string (mostly for debug)'''
		return self.apiTypeStr()
	
	@property
	def isDagNode(self):
		'''Convenience function'''
		return self.hasFn('DagNode')
	
	def hasFn(self, fn):
		'''Test for Fn functionality for this MObject'''
		if not fn.startswith('k'):
			fn = 'k%s'%fn
		
		if hasattr(api.MFn, fn):
			fn = getattr(api.MFn, fn)
		else:
			raise Exception, 'Could not find MFn.%s'%fn
		return api.MObject.hasFn(self, fn)


'''
Usage example, select a few objects and run this
import API

objects = []
for item in cmds.ls(sl=True, l=True):
	objects.append(API.Object(item))
print objects
print '\n==Info for object %s=='%objects[0]
print objects[0].name
print objects[0].hasFn('DagNode')
print objects[0].apiType

#an example of renaming
print 'Renaming all objects'
for object in objects:
	oldName = object.name
	object.name = 'TestNewName'
	print '%s renamed to %s'%(oldName, object.name)
'''