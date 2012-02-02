'''
Auto Toolkit
By: Michael Clavan

Version: v1.0

- Place your scripts and icons in the folders provided to you.
- Change the main folder name "autoToolkit" to what every you want your menu name to be.
- Update the xml file to add buttons to your menu.
- Place the entire folder inside Maya's scripts folder.
- Run the script by:

import autoToolkit  # Note this will change depending what you name the folder.
reload( autoToolkit ) # To instantly update the menus do to changes to the xml file. 

'''

'''
string $newIcon = `getenv XBMLANGPATH`;
print($newIcon)
$newIcon += ";C:/Users/mclavan/Desktop/icons"
putenv XBMLANGPATH $newIcon;
'''

import sys, os, os.path
import maya.cmds as cmds
import maya.mel as mel
import xml.etree.ElementTree as ET
import Callback

# folders icons, mel, python
pythonPath = os.path.join( __path__[0], "python").replace( '\\', '/')
iconsPath = os.path.join( __path__[0], "icons").replace( '\\', '/')
melPath = os.path.join( __path__[0], "mel").replace( '\\', '/')






# python folder adding to script folders
if( pythonPath not in sys.path ):
	sys.path.append( pythonPath )

# Icons folder added to the environment
# mel.eval( "putenv XBMLANGPATH %s" %(mel.eval( "getenv XBMLANGPATH" ) + ";" + iconsPath ) )
if iconsPath not in mel.eval( "getenv XBMLANGPATH" ).split(";"):
	newPath = mel.eval( "getenv XBMLANGPATH" ) + ";" + iconsPath
	print( iconsPath )
	print(newPath)
	putenvLine = 'putenv XBMLANGPATH "%s;"' %(newPath )
	print( putenvLine )
	mel.eval( putenvLine )
else:
	print("Icons path exists: " + iconsPath)
	
if(melPath not in os.environ['MAYA_SCRIPT_PATH'].split(";")):
	# Scripts folder
	os.environ['MAYA_SCRIPT_PATH'] += ";" + melPath
	print( melPath )
else:
	print("MEL Environ Path Exists: %s" %melPath )
	
if(pythonPath not in os.environ['MAYA_SCRIPT_PATH'].split(";")):
	os.environ['MAYA_SCRIPT_PATH'] += ";" + pythonPath
	print( pythonPath )
else:
	print("Python Environ Path Exists: %s" %pythonPath )
	
mel.eval('rehash')

def melRun( sourceLine, melProc="" ):
	mel.eval( sourceLine )
	print("Sourcing: %s" %sourceLine)
	if( melProc ):
		mel.eval( melProc )
		print("Calling: %s" %melProc)


def gui():
	'''
	Generates a menu gui.
	'''
	
	cmds.window(menuBar=True)
	cmds.menu( label="scripts" )
	cmds.menuItem( label="CometScripts",
		c=(lambda *args: melRun( "source cometMenu.mel;") ))  # )"source cometMenu.mel; cometMenu();")
	cmds.menuItem( label="icons",
		c=(lambda *args: melRun( "source kk_controllers;") ))
	cmds.menuItem( subMenu=True, label="Rigging 101" )
	cmds.menuItem( label="Lock and Hide",
		c=(lambda *args: melRun( "source rig101locknHide;", "rig101locknHide")))
	cmds.columnLayout()
	
	cmds.showWindow()

	
def readXML():
	'''
	Reads the provided xml to load the menu items.
	'''	
	filePath = os.path.join(__path__[0], "menu.xml")
	xmlFile = open( filePath, "r")
	
	# Parse xml file
	xmlInfo = ET.parse(xmlFile)
	# Get root
	root = xmlInfo.getroot()	
	# close file
	xmlFile.close()
	
	scriptName = "mecScripts"
# print("ScriptName: " + scriptName)
	# Create top menus
	for mainMenu in root:
		cmds.menuItem( label=mainMenu.text.rstrip().lstrip(), subMenu=True, to=int(mainMenu.attrib['tearoff']) )
# print( int(mainMenu.attrib['tearoff']) )
		for subMenu in mainMenu:
			if( subMenu.tag == "script" ):
				line1 = subMenu[0].text
# print(line1)
				line2 = subMenu[1].text
				if( int(subMenu.attrib['type']) ):
					cmds.menuItem( label=subMenu.text.rstrip().lstrip(),
						ann=subMenu[2].text,
						c="%s;%s" %(line1, line2))	
				else:
					cmds.menuItem( label=subMenu.text.rstrip().lstrip(),
						ann=subMenu[2].text,
						c=Callback.Callback(melRun, line1, line2 ))
						#"mecScripts.melRun('%s','%s')" %(line1,line2))				
			else:
				cmds.menuItem( label=subMenu.text.rstrip().lstrip(), subMenu=True, to=int(subMenu.attrib['tearoff']) )
			
				for scriptName in subMenu:
					line1 = scriptName[0].text
# print(line1)
					line2 = scriptName[1].text
					if( int(scriptName.attrib['type']) ):
						cmds.menuItem( label=scriptName.text.rstrip().lstrip(),
							ann=scriptName[2].text,
							c=Callback.Callback(melRun, line1, line2 ))
							# c="%s;%s" %(line1, line2))	
					else:
						cmds.menuItem( label=scriptName.text.rstrip().lstrip(),
							ann=scriptName[2].text,
							c=Callback.Callback(melRun, line1, line2 ))							
							# c="mecScripts.melRun('%s','%s')" %(line1,line2))
				'''
				cmds.menuItem( label=scriptName.text.rstrip().lstrip(),
					ann=scriptName[2].text,
					c=(lambda *args: eval( 'melRun( "%s", "%s")' %(line1, line2))))
				'''
				cmds.setParent("..", menu=True)
		cmds.setParent("..", menu=True)	
	# Create submenu
	
	# Create script button
	
# gui()

def returnEnvVar( envVar = "$gMainWindow" ):
	return mel.eval( "global string %s; $temp = %s" %(envVar, envVar) )

mayaMainWin = returnEnvVar()

menuName = __name__ + "_menu"

if( cmds.menu( menuName, q=True, ex=True )) :
	cmds.menu( menuName, e=True, dai=True )
else:
	cmds.menu( menuName, label=__name__, to=True, p=mayaMainWin )

cmds.setParent( menuName, menu=True )
readXML()

print("Script Name: " + __name__)
'''
cmds.menuItem( label="CometScripts",
	c=(lambda *args: melRun( "source cometMenu.mel;") ))  # )"source cometMenu.mel; cometMenu();")
cmds.menuItem( label="icons",
	c=(lambda *args: melRun( "source kk_controllers;") ))
cmds.menuItem( subMenu=True, label="Rigging 101" )
mnu = cmds.menuItem( label="Lock and Hide",
	c=(lambda *args: melRun( "source rig101locknHide;", "rig101locknHide")))
'''


	

'''	
	# cmds.menuItem(  divider=True )
cmds.popupMenu( p=mnu, b=2 )
cmds.menuItem( label="Help" )
cmds.menuItem( label="Info" )


// --------------------------------------------------------------------------
    
    // Get rid of existing menu in case it exists already...
    //
if (`menu -q -exists ccCometMenu`)
    {
    menu -e -dai ccCometMenu;
    }
else
    {
	setParent $gMainWindow ;
    menu -l "Comet" -p MayaWindow -to true ccCometMenu ;
    }

setParent -menu ccCometMenu ;
'''
