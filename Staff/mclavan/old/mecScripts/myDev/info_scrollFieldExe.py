win = cmds.window()
pan = cmds.paneLayout( configuration='horizontal2', parent=win )
scrollGui = cmds.cmdScrollFieldExecuter(width=200, height=100, sourceType="python")
cmds.button( label="Execute", c=testScroll )
cmds.showWindow()

def testScroll( *args ):
	cmds.cmdScrollFieldExecuter( scrollGui, e=True,  executeAll=1 )	


# Copy elements and delete UI
cmds.cmdScrollFieldExecuter( scrollGui, e=True,  selectAll=1 )
cmds.cmdScrollFieldExecuter( scrollGui, e=True,  copySelection=1 )
cmds.deleteUI( pan )

# Regenerate UI (MEL) and paste elements
pan = cmds.paneLayout( configuration='horizontal2', parent=win )
scrollGui = cmds.cmdScrollFieldExecuter(width=200, height=100, sourceType="mel")
cmds.button( label="Execute", c=testScroll )
cmds.cmdScrollFieldExecuter( scrollGui, e=True,  pasteSelection=1 )


# Copy and then paste
# Must be selected
# Something has to be selected for this to work.
cmds.cmdScrollFieldExecuter( scrollGui, e=True,  selectAll=1 )
cmds.cmdScrollFieldExecuter( scrollGui, e=True,  copySelection=1 )
cmds.cmdScrollFieldExecuter( scrollGui, e=True,  pasteSelection=1 )

# Getting the Text
cmds.cmdScrollFieldExecuter( scrollGui, q=True, text=True )
# Adding Text to the end

# Replacing text
# Append to the end of the field
cmds.cmdScrollFieldExecuter( scrollGui, e=True,  appendText=guiLine )
# Inserting at current cursor position
cmds.cmdScrollFieldExecuter( scrollGui, e=True, insertText=guiLine)
# Completely over writes
cmds.cmdScrollFieldExecuter( scrollGui, e=True, text=guiLine)
 

# source Type is it going to be mel or python
cmds.cmdScrollFieldExecuter( scrollGui, q=True,  sourceType=1)
# Cannot switch types on the fly, GUI will have to be deleted and regenerated.
cmds.cmdScrollFieldExecuter( scrollGui, e=True,  sourceType="python")
cmds.cmdScrollFieldExecuter( scrollGui, e=True,  sourceType="mel")

# Executing present code
cmds.cmdScrollFieldExecuter( scrollGui, e=True,  executeAll=1 )	
cmds.cmdScrollFieldExecuter( scrollGui, e=True,  exc=1 )	



