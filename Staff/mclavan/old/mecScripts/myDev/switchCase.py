
aList = ['a', 'b', 'c']


items = {'a': "termA", 'b': "termB", 'c':"termC"}

items['a'] == 'termA'

	# RadioButtonSel, minCB, minVal, maxCB, maxVal, dv
attrValues = [1, 1, 0, 1, 10, 0]


# The alternative to a switch case.
attrs = { 'fk_ik': [1, 1, 0, 1, 10, 0], 'world_switch':[1, 1, 0, 1, 10, 0], 'vis_swt', [2, 1, 0, 1, 1, 1]}

key = 'fk_ik'
if( attrs.has_key( key ) ):
	return attrs[key]
else:
	print( "Attr doesn't exists" )
	
	

