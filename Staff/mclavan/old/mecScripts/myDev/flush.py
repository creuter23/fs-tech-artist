def flush():
	'''
	flushes all loaded modules from sys.modules which causes them to be reloaded
	when next imported...  super useful for developing crap within a persistent
	python environment
	'''
	dirsToFlush = filesystem.Path( 'd:/tools' ), filesystem.Path( 'd:/studio/maya' )

	keysToDelete = []
	for modName, mod in sys.modules.iteritems():
		try:
			modPath = filesystem.Path( mod.__file__ )
		except AttributeError: continue

		for flushDir in dirsToFlush:
			if modPath.isUnder( flushDir ):
				keysToDelete.append( modName )
				break

	for keyToDelete in keysToDelete:
		del( sys.modules[ keyToDelete] )

	gc.collect()
