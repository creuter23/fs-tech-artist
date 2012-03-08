#Tony Sakson
#SAL_GradingScript_Project_01_v4.py

#How to run:
#	import SAL_GradingScript_Project_01_v4
#	reload (SAL_GradingScript_Project_01_v4)
#
# This Script creates a window with 3 collapsable frames:
# 1.) File Info
# 2.) Grade Totals
# 3.) Grading


import maya.cmds as cmds

# Create the main scroll window with column layout
def windowGUI():
	window = cmds.window('TSakson SAL Grading Script Project 01 - Rendering 101')
	cmds.scrollLayout( 'Scroll Layout' )
	cmds.columnLayout()
	cmds.showWindow( window )

# Create the Open Scene File Button Function and grab the scene name
def openSceneButtonFunction(*args):
	import os
	global sceneFileName
	global selectedFileName
	selectedFileName=cmds.fileDialog()
	cmds.launchImageEditor(vif=selectedFileName)
	sceneFileName=os.path.basename(selectedFileName)
	cmds.textField('sceneName', w=400, e=1, fi=sceneFileName)

# Updates all the Grade IntFields anytime something is changed
def updateGradeTotal(*args):
	aanqGradeTotal=cmds.intFieldGrp( "aanqIntField", q=1, value1=1)
	cflGradeTotal=cmds.intFieldGrp( "cflIntField", q=1, value1=1)
	proGradeTotal=cmds.intFieldGrp( "proIntField", q=1, value1=1)
	
	cmds.intFieldGrp( "aanqGradeIntField", e=1, value1=(aanqGradeTotal))
	aangTotalGradeTotal=cmds.intFieldGrp( "aanqGradeIntField", q=1, value1=1)
	cmds.intFieldGrp( "cflGradeIntField", e=1, value1=(cflGradeTotal))
	cflTotalGradeTotal=cmds.intFieldGrp( "cflGradeIntField", q=1, value1=1)
	cmds.intFieldGrp( "proGradeIntField", e=1, value1=(proGradeTotal))
	proTotalGradeTotal=cmds.intFieldGrp( "proGradeIntField", q=1, value1=1)
	lateGradeTotal=cmds.intFieldGrp( "lateGradeIntField", q=1, value1=1)
	totalGradeTotal=cmds.intFieldGrp( "totalGradeIntField", e=1, value1=((aangTotalGradeTotal*.45)+(cflTotalGradeTotal*.45)+(proTotalGradeTotal*.1)-(lateGradeTotal)))

# Create the Output Grades and Comments to Text File Button Function
def textOutputButtonFunction(*args):
	lateGradeCheck=cmds.intFieldGrp( "lateGradeIntField", q=1, value1=1)
	if (lateGradeCheck==0):
		dialogCheck=cmds.confirmDialog( title='Confirm Output', message='Is this a late project?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='Yes' )
		if dialogCheck == 'Yes':
			print ("Output Cancelled")
		else:
			print ("Output Complete")
			continueOutputFunction()
	else:
		continueOutputFunction()
		
def continueOutputFunction():	
	aangGradeOutputTotal=cmds.intFieldGrp( "aanqGradeIntField", q=1, value1=1)
	cflGradeOutputTotal=cmds.intFieldGrp( "cflGradeIntField", q=1, value1=1)
	proGradeOutputTotal=cmds.intFieldGrp( "proGradeIntField", q=1, value1=1)
	lateGradeOutputTotal=cmds.intFieldGrp( "lateGradeIntField", q=1, value1=1)
	totalGradeOutputTotal=cmds.intFieldGrp( "totalGradeIntField", q=1, value1=1)
# Queries the Grade comments for output
	aanqTSListOutput=cmds.scrollField("aanqTSList", q=1, tx=1)
	cflTSListOutput=cmds.scrollField("cflTSList", q=1, tx=1)
	proTSListOutput=cmds.scrollField("proTSList", q=1, tx=1)
# Formats the comments for output	
	sceneFileOutput=open(selectedFileName+".txt", 'w')
	sceneFileOutput.write("Grading for: "+sceneFileName+"\r\n")
	sceneFileOutput.write("-----------------------------------\r\n")
	sceneFileOutput.write("Antialiasing & Noise Quality Comments: "+aanqTSListOutput+"\r\n")
	sceneFileOutput.write("\r\n")
	sceneFileOutput.write("Antialiasing & Noise Quality Grade Total(45%): "+str(aangGradeOutputTotal)+"\r\n")
	sceneFileOutput.write("-----------------------------------\r\n")
	sceneFileOutput.write("Composition & Focal Length Comments: "+cflTSListOutput+"\r\n")
	sceneFileOutput.write("\r\n")
	sceneFileOutput.write("Composition & Focal Length Grade Total(45%): "+str(cflGradeOutputTotal)+"\r\n")
	sceneFileOutput.write("-----------------------------------\r\n")
	sceneFileOutput.write("Professionalism Comments: "+proTSListOutput+"\r\n")
	sceneFileOutput.write("\r\n")
	sceneFileOutput.write("Professionalism Grade Total (10%): "+str(proGradeOutputTotal)+"\r\n")
	sceneFileOutput.write("-----------------------------------\r\n")
	sceneFileOutput.write("Late Deductions: -"+str(lateGradeOutputTotal)+"\r\n")
	sceneFileOutput.write("-----------------------------------\r\n")
	sceneFileOutput.write("Overall Grade Total: "+str(totalGradeOutputTotal)+"\r\n")
	sceneFileOutput.close()
	
# Creates the File Info Frame and uses formlayout to control positioning of the various elements
def fileFrame():
	cmds.frameLayout( label='File Info', cll=True, labelAlign='center', borderStyle='etchedIn', w=480 )
	cmds.columnLayout()
	fileFrm = cmds.formLayout()
	# Create the Scene Name label and text field
	nameLabel=cmds.text( label='Image Name' )
	nameField = cmds.textField('sceneName')
	cmds.formLayout( fileFrm, edit=1, attachForm=[[nameLabel, "top", 5 ], [nameLabel, "left", 5]])
	cmds.formLayout( fileFrm, edit=1, attachForm=[nameField, "left", 5 ], attachControl=[nameField, "left", 5, nameLabel])
	# Create the Open Scene File button
	openSceneButton=cmds.button( label='Open Image File', align='center', command=openSceneButtonFunction )
	cmds.formLayout( fileFrm, edit=1, attachForm=[openSceneButton, "left", 5], attachControl=[openSceneButton, "top", 5, nameLabel])
	cmds.setParent('..')
	cmds.setParent('..')
	cmds.setParent('..')
	
# Create the Grade Totals frame and uses formlayout to control positioning of the various elements
def gradeTotalsFrame():	
	cmds.frameLayout( label='Grade Totals', cll=True, labelAlign='center', borderStyle='etchedIn', w=480 )
	cmds.columnLayout()
	gradeFrm = cmds.formLayout()
	global aangTotalGradeTotal
	global cflTotalGradeTotal
	global proTotalGradeTotal
	global lateGradeTotal
	global totalGradeTotal
	# Create the Output Grades and Comments to Text File button
	textOutputButton=cmds.button( label='Output Grades and Comments to Text File', align='center', command=textOutputButtonFunction )
	cmds.formLayout( gradeFrm, edit=1, attachForm=[[textOutputButton, "left", 40], [textOutputButton, "top", 5]])
	# Create the Antialiasing/Noise Quality Grade Total label and intField
	aanqGradeField=cmds.intFieldGrp( "aanqGradeIntField", numberOfFields=1, label='Antialias/Noise Quality', changeCommand=updateGradeTotal)
	cmds.formLayout( gradeFrm, edit=1, attachOppositeControl=[[aanqGradeField, "top", 35, textOutputButton], [aanqGradeField, "right", 0, textOutputButton]])
	# Create the Composition/Focal Length Grade Total label and intField
	cflGradeField=cmds.intFieldGrp( "cflGradeIntField", numberOfFields=1, label='Composition/Focal Length', changeCommand=updateGradeTotal)
	cmds.formLayout( gradeFrm, edit=1, attachOppositeControl=[[cflGradeField, "top", 35, aanqGradeField], [cflGradeField, "left", 0, aanqGradeField]])
	# Create the Art Grade Total label and intField
	proGradeField=cmds.intFieldGrp( "proGradeIntField", numberOfFields=1, label='Professionalism', changeCommand=updateGradeTotal)
	cmds.formLayout( gradeFrm, edit=1, attachOppositeControl=[[proGradeField, "top", 35, cflGradeField], [proGradeField, "left", 0, cflGradeField]])
	# Create the Late Deductions Grade Total label and intField
	lateGradeField=cmds.intFieldGrp( "lateGradeIntField", numberOfFields=1, label='Late Deductions', changeCommand=updateGradeTotal)
	cmds.formLayout( gradeFrm, edit=1, attachOppositeControl=[[lateGradeField, "top", 35, proGradeField], [lateGradeField, "left", 0, proGradeField]])
	# Create the Overall Grade Total label and intField
	totalGradeField=cmds.intFieldGrp( "totalGradeIntField", numberOfFields=1, label='Grade Total')
	cmds.formLayout( gradeFrm, edit=1, attachOppositeControl=[[totalGradeField, "top", 35, lateGradeField], [totalGradeField, "left", 0, lateGradeField]])
	cmds.setParent('..')
	cmds.setParent('..')
	cmds.setParent('..')

# Create the Antialiasing Row 1 button, comments and grade functions	
def antiAliasButton1(*args):
	antiAliasA="No signs of aliasing, and shadow and/or material noise."
	antiAliasB="Small amount of aliasing, and shadow and/or material noise."
	antiAliasC="Moderate amount of aliasing, and shadow and/or material noise."
	antiAliasRow1=cmds.radioButtonGrp( "aanqRadButGrp1", q=1, sl=1)
	if (antiAliasRow1 ==1):
		cmds.intFieldGrp( "aanqIntField", e=1, value1=100)
		cmds.scrollField("aanqTSList", e=1, cl=1)
		cmds.scrollField("aanqTSList", e=1, insertText=antiAliasA)
		updateGradeTotal()
	elif (antiAliasRow1 ==2):
		cmds.intFieldGrp( "aanqIntField", e=1, value1=89)
		cmds.scrollField("aanqTSList", e=1, cl=1)
		cmds.scrollField("aanqTSList", e=1, insertText=antiAliasB)
		updateGradeTotal()
	else:
		cmds.intFieldGrp( "aanqIntField", e=1, value1=79)
		cmds.scrollField("aanqTSList", e=1, cl=1)
		cmds.scrollField("aanqTSList", e=1, insertText=antiAliasC)
		updateGradeTotal()
# Create the Antialiasing Row 2 button, comments and grade functions
def antiAliasButton2(*args):
	antiAliasD="Severe amount amount of aliasing, and shadow and/or material noise."
	antiAliasF="Unacceptable amount of aliasing, and shadow and/or material noise."
	antiAliasRow2=cmds.radioButtonGrp( "aanqRadButGrp2", q=1, sl=1)
	if (antiAliasRow2 ==1):
		cmds.intFieldGrp( "aanqIntField", e=1, value1=72)
		cmds.scrollField("aanqTSList", e=1, cl=1)
		cmds.scrollField("aanqTSList", e=1, insertText=antiAliasD)
		updateGradeTotal()
	else:
		cmds.intFieldGrp( "aanqIntField", e=1, value1=69)
		cmds.scrollField("aanqTSList", e=1, cl=1)
		cmds.scrollField("aanqTSList", e=1, insertText=antiAliasF)
		updateGradeTotal()
		
# Create the Comp Focal Length Row 1 button, comments and grade functions
def compFocalButton1(*args):
	compFocalA="Composition directs the viewers eye to the subject instantaniously. Focal length choice supports the composition."
	compFocalB="Composition directs the viewer's eye to the subject after a second of viewing. Focal length choice supports the composition."
	compFocalC="Composition directs the viewers eye to the subject after a few seconds on viewing. Focal length choice mildly supports the composition."
	compFocalRow1=cmds.radioButtonGrp( "cflButGrp1", q=1, sl=1)
	if (compFocalRow1 ==1):
		cmds.intFieldGrp( "cflIntField", e=1, value1=100)
		cmds.scrollField("cflTSList", e=1, cl=1)
		cmds.scrollField("cflTSList", e=1, insertText=compFocalA)
		updateGradeTotal()
	elif (compFocalRow1 ==2):
		cmds.intFieldGrp( "cflIntField", e=1, value1=89)
		cmds.scrollField("cflTSList", e=1, cl=1)
		cmds.scrollField("cflTSList", e=1, insertText=compFocalB)
		updateGradeTotal()
	else:
		cmds.intFieldGrp( "cflIntField", e=1, value1=79)
		cmds.scrollField("cflTSList", e=1, cl=1)
		cmds.scrollField("cflTSList", e=1, insertText=compFocalC)
		updateGradeTotal()
		
# Create the Comp Focal Length Row 2 button, comments and grade functions		
def compFocalButton2(*args):
	compFocalD="Composition does not direct the viewer's eye to subject for over 5 seconds of viewing. Focal length choice vaguely supports the composition. "
	compFocalF="Composition does not direct the viewer's eye to the subject. Focal length choice does not support the composition. "
	compFocalRow2=cmds.radioButtonGrp( "cflButGrp2", q=1, sl=1)
	if (compFocalRow2 ==1):
		cmds.intFieldGrp( "cflIntField", e=1, value1=72)
		cmds.scrollField("cflTSList", e=1, cl=1)
		cmds.scrollField("cflTSList", e=1, insertText=compFocalD)
		updateGradeTotal()
	else:
		cmds.intFieldGrp( "cflIntField", e=1, value1=69)
		cmds.scrollField("cflTSList", e=1, cl=1)
		cmds.scrollField("cflTSList", e=1, insertText=compFocalF)
		updateGradeTotal()

# Create the Professionalism Row 1 button, comments and grade functions
def proButton1(*args):
	proA="Student named their files correctly, image is correct resolution. Student could trouble shoot problems with little or no help from instructor."
	proB="Student named their files correctly, image is correct resolution. Student could trouble shoot problems with some help from instructor."
	proC="Student named their files poorly, image is correct resolution. Student had trouble problem solving without instructors help."
	proRow1=cmds.radioButtonGrp( "proButGrp1", q=1, sl=1)
	if (proRow1 ==1):
		cmds.intFieldGrp( "proIntField", e=1, value1=100)
		cmds.scrollField("proTSList", e=1, cl=1)
		cmds.scrollField("proTSList", e=1, insertText=proA)
		updateGradeTotal()
	elif (proRow1 ==2):
		cmds.intFieldGrp( "proIntField", e=1, value1=89)
		cmds.scrollField("proTSList", e=1, cl=1)
		cmds.scrollField("proTSList", e=1, insertText=proB)
		updateGradeTotal()
	else:
		cmds.intFieldGrp( "proIntField", e=1, value1=79)
		cmds.scrollField("proTSList", e=1, cl=1)
		cmds.scrollField("proTSList", e=1, insertText=proC)
		updateGradeTotal()
		
# Create the Professionalism Row 2 button, comments and grade functions		
def proButton2(*args):
	proD="Student did not name their files correctly, image is incorrect resolution. Student often had trouble problem solving without instructors help."
	proF="Student did not name their files correctly, image is incorrect resolution. Student had poor trouble shooting skills."
	proRow2=cmds.radioButtonGrp( "proButGrp2", q=1, sl=1)
	if (proRow2 ==1):
		cmds.intFieldGrp( "proIntField", e=1, value1=72)
		cmds.scrollField("proTSList", e=1, cl=1)
		cmds.scrollField("proTSList", e=1, insertText=proD)
		updateGradeTotal()
	else:
		cmds.intFieldGrp( "proIntField", e=1, value1=69)
		cmds.scrollField("proTSList", e=1, cl=1)
		cmds.scrollField("proTSList", e=1, insertText=proF)
		updateGradeTotal()
		
# Create the Art Frame and uses formlayout to control positioning of the various elements	
def gradeFrame():
#	cmds.frameLayout( label='Grade', cll=True, labelAlign='center', borderStyle='etchedIn', w=480 )
	cmds.frameLayout( label='Grade', cll=True, labelAlign='center', height= 880, borderStyle='etchedIn', w=480 )
	cmds.columnLayout()
	global gradeFrm
	gradeFrm = cmds.formLayout()
	global aanqGradeTotal
	global cflGradeTotal
	global proGradeTotal
	
# Antialiasing and Noise Quality radio button, textScrollList and intField Function
def antiAliasNoiseQual():
	global aanqSeparator
	aanqGroup1=cmds.radioButtonGrp( "aanqRadButGrp1", numberOfRadioButtons=3, label='Anitalias/Noise Qual (45%)', labelArray3=['A+ -A', 'B+ -B', 'C+ -C'], onCommand=antiAliasButton1)
	aanqGroup2=cmds.radioButtonGrp( "aanqRadButGrp2", numberOfRadioButtons=2, shareCollection=aanqGroup1, label='', labelArray2=['D', 'F'], onCommand=antiAliasButton2)
	cmds.formLayout( gradeFrm, edit=1, attachForm=[[aanqGroup1, "top", 5], [aanqGroup1, "left", 5]])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[aanqGroup2, "left", 5, ], attachControl=[aanqGroup2, "top", 5, aanqGroup1])
	aanqShapeField=cmds.intFieldGrp( "aanqIntField", numberOfFields=1, label='Grade', changeCommand=updateGradeTotal)
	aanqTextScrollList=cmds.scrollField("aanqTSList", w=200, h=150, wordWrap=1)
	aanqCommentsLabel=cmds.text( label='Comments' )
	cmds.formLayout( gradeFrm, edit=1, attachForm=[aanqShapeField, "top", 5], attachControl=[aanqShapeField, "top", 10, aanqGroup2])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[aanqTextScrollList, "left", 140], attachControl=[aanqTextScrollList, "top", 10, aanqShapeField])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[aanqCommentsLabel, "left", 60], attachControl=[aanqCommentsLabel, "top", 10, aanqShapeField])
	aanqSeparator=cmds.separator( height=15, width=460, style='in' )
	cmds.formLayout( gradeFrm, edit=1, attachForm=[aanqSeparator, "left", 5], attachControl=[aanqSeparator, "top", 5, aanqTextScrollList])
	
# Composition and Focal Length radio button, textScrollList and intField Function
def compFocalLength():
	global cflSeparator
	cflGroup1 = cmds.radioButtonGrp( "cflButGrp1", numberOfRadioButtons=3, label='Comp/Focal Length (45%)', labelArray3=['A+ -A', 'B+ -B', 'C+ -C'], onCommand=compFocalButton1 )
	cflGroup2 = cmds.radioButtonGrp( "cflButGrp2", numberOfRadioButtons=2, shareCollection=cflGroup1, label='', labelArray2=['D', 'F'], onCommand=compFocalButton2  )
	cmds.formLayout( gradeFrm, edit=1, attachForm=[cflGroup1, "left", 5], attachControl=[cflGroup1, "top", 5, aanqSeparator])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[cflGroup2, "left", 5, ], attachControl=[cflGroup2, "top", 5, cflGroup1])
	cflShapeField=cmds.intFieldGrp( "cflIntField", numberOfFields=1, label='Grade', changeCommand=updateGradeTotal)
	cflTextScrollList=cmds.scrollField("cflTSList", w=200, h=150, wordWrap=1)
	cflCommentsLabel=cmds.text( label='Comments' )
	cmds.formLayout( gradeFrm, edit=1, attachForm=[cflShapeField, "top", 5], attachControl=[cflShapeField, "top", 10, cflGroup2])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[cflTextScrollList, "left", 140], attachControl=[cflTextScrollList, "top", 10, cflShapeField])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[cflCommentsLabel, "left", 60], attachControl=[cflCommentsLabel, "top", 10, cflShapeField])
	cflSeparator=cmds.separator( height=15, width=460, style='in' )
	cmds.formLayout( gradeFrm, edit=1, attachForm=[cflSeparator, "left", 5], attachControl=[cflSeparator, "top", 5, cflTextScrollList])
	
# Professionalism radio button, textScrollList and intField Function
def professionalism():
	global proSeparator
	proGroup1 = cmds.radioButtonGrp( "proButGrp1", numberOfRadioButtons=3, label='Professionalism (10%)', labelArray3=['A+ -A', 'B+ -B', 'C+ -C'], onCommand=proButton1 )
	proGroup2 = cmds.radioButtonGrp( "proButGrp2", numberOfRadioButtons=2, shareCollection=proGroup1, label='', labelArray2=['D', 'F'], onCommand=proButton2  )
	cmds.formLayout( gradeFrm, edit=1, attachForm=[proGroup1, "left", 5], attachControl=[proGroup1, "top", 5, cflSeparator])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[proGroup2, "left", 5, ], attachControl=[proGroup2, "top", 5, proGroup1])
	proShapeField=cmds.intFieldGrp( "proIntField", numberOfFields=1, label='Grade', changeCommand=updateGradeTotal)
	proTextScrollList=cmds.scrollField("proTSList", w=200, h=150, wordWrap=1)
	proCommentsLabel=cmds.text( label='Comments' )
	cmds.formLayout( gradeFrm, edit=1, attachForm=[proShapeField, "top", 5], attachControl=[proShapeField, "top", 10, proGroup2])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[proTextScrollList, "left", 140], attachControl=[proTextScrollList, "top", 10, proShapeField])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[proCommentsLabel, "left", 60], attachControl=[proCommentsLabel, "top", 10, proShapeField])
#	proSeparator=cmds.separator( height=15, width=460, style='in' )
#	cmds.formLayout( gradeFrm, edit=1, attachForm=[proSeparator, "left", 5], attachControl=[proSeparator, "top", 5, proTextScrollList])
	cmds.setParent('..')
	cmds.setParent('..')
	cmds.setParent('..')
	
# Built the GUI	
windowGUI()
fileFrame()
gradeTotalsFrame()
gradeFrame()
antiAliasNoiseQual()
compFocalLength()
professionalism()
