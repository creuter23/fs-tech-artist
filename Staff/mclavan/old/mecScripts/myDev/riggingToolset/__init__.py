

import rigTools
import ikFk

def gui(mode=1):
	if( mode==1 ):
		rigTools.gui()
	elif( mode==2 ):
		ikFk.gui()



def dev(mode=1):
	
	if( mode==1 ):
		reload(rigTools)
	elif( mode==2 ):
		reload(ikFk)	
