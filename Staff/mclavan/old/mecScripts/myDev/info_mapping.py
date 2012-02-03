'''
Mapping in Python
info_mapping.py

Description:
	- Different examples on how to implement List Mapping into Maya
	
	
'''
# [selCB.remove(x) for x in newAttrs]

'''
Returning only keyed attributes (omitting locked)
'''
selected = cmds.ls(sl=True)
selCB = cmds.listAttr(sel, k=True)
# Creates a duplicate list
newAttrs = selCB[:]

'''
# Partial Map
# This one will remove all the elements in the list (still needs the if statment)
[selCB.remove(x) for x in newAttrs]

for x in newAttrs:
	selCB.remove(x)
'''
# Full Map
[selCB.remove(x) for x in newAttrs if x in cmds.listAttrs( selected, k=True, l=True )]

# Break down of the map.
for x in newAttrs:
	lockedAtts = cmds.listAttrs( selected, k=True, l=True )
	# in keyword
	if( x in lockedAttrs ):
		selCB.remove(x)
		
		
'''
Adding to elements inside of a list
'''
names = ["mike", "george", "susan"]
names = [name+"_geo" for name in names ]
