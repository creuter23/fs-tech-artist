#Tony Sakson
#SAL_GradingScript_Project_03_v3.py

#How to run:
#	import SAL_GradingScript_Project_03_v3
#	reload (SAL_GradingScript_Project_03_v3)
#
# This Script creates a window with 3 collapsable frames:
# 1.) File Info
# 2.) Grade Totals
# 3.) Grading


import maya.cmds as cmds

# Create the main scroll window with column layout
def windowGUI():
	window = cmds.window('TSakson SAL Grading Script Project 03 - Soft Lighting')
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
	global lightGradeTotal
	global cflGradeTotal
	global aanqGradeTotal
	global proGradeTotal
	global cflDisplayGradeTotal
	global aanqDisplayGradeTotal
	global proDisplayGradeTotal
	lightGradeTotal=cmds.intFieldGrp( "lightIntField", q=1, value1=1)
	cflGradeTotal=cmds.intFieldGrp( "cflIntField", q=1, value1=1)
	aanqGradeTotal=cmds.intFieldGrp( "aanqIntField", q=1, value1=1)
	proGradeTotal=cmds.intFieldGrp( "proIntField", q=1, value1=1)
	
	cmds.intFieldGrp( "gradeIntField", e=1, value1=(lightGradeTotal))
	gradeTotal=cmds.intFieldGrp( "gradeIntField", q=1, value1=1)
	cflDeductGradeTotal=cmds.intFieldGrp( "cflDeductGradeIntField", e=1, value1=(cflGradeTotal*.15))
	cflDisplayGradeTotal=cmds.intFieldGrp( "cflDeductGradeIntField", q=1, value1=1)
	aanDeductGradeTotal=cmds.intFieldGrp( "aanDeductGradeIntField", e=1, value1=(aanqGradeTotal*.15))
	aanqDisplayGradeTotal=cmds.intFieldGrp( "aanDeductGradeIntField", q=1, value1=1)
	proDeductGradeTotal=cmds.intFieldGrp( "proDeductGradeIntField", e=1, value1=(proGradeTotal*.1))
	proDisplayGradeTotal=cmds.intFieldGrp( "proDeductGradeIntField", q=1, value1=1)
	lateGradeTotal=cmds.intFieldGrp( "lateGradeIntField", q=1, value1=1)
	totalGradeTotal=cmds.intFieldGrp( "totalGradeIntField", e=1, value1=((gradeTotal)-cflDisplayGradeTotal-aanqDisplayGradeTotal-proDisplayGradeTotal-lateGradeTotal))

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
	gradeOutputTotal=cmds.intFieldGrp( "gradeIntField", q=1, value1=1)
	lateGradeOutputTotal=cmds.intFieldGrp( "lateGradeIntField", q=1, value1=1)
	totalGradeOutputTotal=cmds.intFieldGrp( "totalGradeIntField", q=1, value1=1)
# Queries the Grade comments for output
	aanqTSListOutput=cmds.scrollField("aanqTSList", q=1, tx=1)
	cflTSListOutput=cmds.scrollField("cflTSList", q=1, tx=1)
	lightTSTSListOutput=cmds.scrollField("lightTSList", q=1, tx=1)
	proTSListOutput=cmds.scrollField("proTSList", q=1, tx=1)
# Formats the comments for output	
	sceneFileOutput=open(selectedFileName+".txt", 'w')
	sceneFileOutput.write("Grading for: "+sceneFileName+"\r\n")
	sceneFileOutput.write("-----------------------------------\r\n")
	sceneFileOutput.write("Lighting Comments: "+lightTSTSListOutput+"\r\n")
	sceneFileOutput.write("Lighting Grade: "+str(lightGradeTotal)+"\r\n")
	sceneFileOutput.write("\r\n")
	sceneFileOutput.write("Grade Total: "+str(gradeOutputTotal)+"\r\n")
	sceneFileOutput.write("-----------------------------------\r\n")
	sceneFileOutput.write("Deduction Comments:\r\n")
	sceneFileOutput.write("Composition & Focal Length Comments: "+cflTSListOutput+"\r\n")
	sceneFileOutput.write("Antialiasing & Noise Quality Comments: "+aanqTSListOutput+"\r\n")
	sceneFileOutput.write("Professionalism Comments: "+proTSListOutput+"\r\n")
	sceneFileOutput.write("-----------------------------------\r\n")
	sceneFileOutput.write("Comp/Focal Len Deductions (15%): -"+str(cflDisplayGradeTotal)+"\r\n")
	sceneFileOutput.write("Alias/Noise Deductions (15%): -"+str(aanqDisplayGradeTotal)+"\r\n")
	sceneFileOutput.write("Prof Deductions (10%): -"+str(proDisplayGradeTotal)+"\r\n")
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
	global gradeTotal
	global cflDeductGradeTotal
	global aanDeductGradeTotal
	global proDeductGradeTotal
	global lateGradeTotal
	global totalGradeTotal
	# Create the Output Grades and Comments to Text File button
	textOutputButton=cmds.button( label='Output Grades and Comments to Text File', align='center', command=textOutputButtonFunction )
	cmds.formLayout( gradeFrm, edit=1, attachForm=[[textOutputButton, "left", 5], [textOutputButton, "top", 5]])
	# Create the Art Grade Total label and intField
	gradeGradeField=cmds.intFieldGrp( "gradeIntField", numberOfFields=1, label='Grade Total', changeCommand=updateGradeTotal)
	cmds.formLayout( gradeFrm, edit=1, attachOppositeControl=[[gradeGradeField, "top", 35, textOutputButton], [gradeGradeField, "left", 0, textOutputButton]])
	# Create the Comp/Focal Length Deductions Grade Total label and intField
	cflDeductGradeField=cmds.intFieldGrp( "cflDeductGradeIntField", numberOfFields=1, label='Comp/Focal Len Deductions', changeCommand=updateGradeTotal)
	cmds.formLayout( gradeFrm, edit=1, attachOppositeControl=[[cflDeductGradeField, "top", 35, gradeGradeField], [cflDeductGradeField, "left", 0, gradeGradeField]])
	# Create the Antialias/Noise Deductions Grade Total label and intField
	aanDeductGradeField=cmds.intFieldGrp( "aanDeductGradeIntField", numberOfFields=1, label='Alias/Noise Deductions', changeCommand=updateGradeTotal)
	cmds.formLayout( gradeFrm, edit=1, attachOppositeControl=[[aanDeductGradeField, "top", 35, cflDeductGradeField], [aanDeductGradeField, "left", 0, cflDeductGradeField]])
	# Create the Professionalism Deductions Grade Total label and intField
	proDeductGradeField=cmds.intFieldGrp( "proDeductGradeIntField", numberOfFields=1, label='Prof Deductions', changeCommand=updateGradeTotal)
	cmds.formLayout( gradeFrm, edit=1, attachOppositeControl=[[proDeductGradeField, "top", 35, aanDeductGradeField], [proDeductGradeField, "left", 0, aanDeductGradeField]])
	# Create the Late Deductions Grade Total label and intField
	lateGradeField=cmds.intFieldGrp( "lateGradeIntField", numberOfFields=1, label='Late Deductions', changeCommand=updateGradeTotal)
	cmds.formLayout( gradeFrm, edit=1, attachOppositeControl=[[lateGradeField, "top", 35, proDeductGradeField], [lateGradeField, "left", 0, proDeductGradeField]])
	# Create the Overall Grade Total label and intField
	totalGradeField=cmds.intFieldGrp( "totalGradeIntField", numberOfFields=1, label='Grade Total')
	cmds.formLayout( gradeFrm, edit=1, attachOppositeControl=[[totalGradeField, "top", 35, lateGradeField], [totalGradeField, "left", 0, lateGradeField]])
	cmds.setParent('..')
	cmds.setParent('..')
	cmds.setParent('..')

# Create the Antialiasing Row 1 button, comments and grade functions	
def antiAliasButton1(*args):
	antiAliasA="No Deduction."
	antiAliasB="Small amount of aliasing, and shadow and/or material noise."
	antiAliasC="Moderate amount of aliasing, and shadow and/or material noise."
	antiAliasRow1=cmds.radioButtonGrp( "aanqRadButGrp1", q=1, sl=1)
	if (antiAliasRow1 ==1):
		cmds.intFieldGrp( "aanqIntField", e=1, value1=0)
		cmds.scrollField("aanqTSList", e=1, cl=1)
		cmds.scrollField("aanqTSList", e=1, insertText=antiAliasA)
		updateGradeTotal()
	elif (antiAliasRow1 ==2):
		cmds.intFieldGrp( "aanqIntField", e=1, value1=25)
		cmds.scrollField("aanqTSList", e=1, cl=1)
		cmds.scrollField("aanqTSList", e=1, insertText=antiAliasB)
		updateGradeTotal()
	else:
		cmds.intFieldGrp( "aanqIntField", e=1, value1=50)
		cmds.scrollField("aanqTSList", e=1, cl=1)
		cmds.scrollField("aanqTSList", e=1, insertText=antiAliasC)
		updateGradeTotal()
# Create the Antialiasing Row 2 button, comments and grade functions
def antiAliasButton2(*args):
	antiAliasD="Severe amount amount of aliasing, and shadow and/or material noise."
	antiAliasF="Unacceptable amount of aliasing, and shadow and/or material noise."
	antiAliasRow2=cmds.radioButtonGrp( "aanqRadButGrp2", q=1, sl=1)
	if (antiAliasRow2 ==1):
		cmds.intFieldGrp( "aanqIntField", e=1, value1=75)
		cmds.scrollField("aanqTSList", e=1, cl=1)
		cmds.scrollField("aanqTSList", e=1, insertText=antiAliasD)
		updateGradeTotal()
	else:
		cmds.intFieldGrp( "aanqIntField", e=1, value1=100)
		cmds.scrollField("aanqTSList", e=1, cl=1)
		cmds.scrollField("aanqTSList", e=1, insertText=antiAliasF)
		updateGradeTotal()
		
# Create the Comp Focal Length Row 1 button, comments and grade functions
def compFocalButton1(*args):
	compFocalA="No Deduction."
	compFocalB="Composition directs the viewer's eye to the subject after a second of viewing. Focal length choice supports the composition."
	compFocalC="Composition directs the viewers eye to the subject after a few seconds on viewing. Focal length choice mildly supports the composition."
	compFocalRow1=cmds.radioButtonGrp( "cflButGrp1", q=1, sl=1)
	if (compFocalRow1 ==1):
		cmds.intFieldGrp( "cflIntField", e=1, value1=0)
		cmds.scrollField("cflTSList", e=1, cl=1)
		cmds.scrollField("cflTSList", e=1, insertText=compFocalA)
		updateGradeTotal()
	elif (compFocalRow1 ==2):
		cmds.intFieldGrp( "cflIntField", e=1, value1=25)
		cmds.scrollField("cflTSList", e=1, cl=1)
		cmds.scrollField("cflTSList", e=1, insertText=compFocalB)
		updateGradeTotal()
	else:
		cmds.intFieldGrp( "cflIntField", e=1, value1=50)
		cmds.scrollField("cflTSList", e=1, cl=1)
		cmds.scrollField("cflTSList", e=1, insertText=compFocalC)
		updateGradeTotal()
		
# Create the Comp Focal Length Row 2 button, comments and grade functions		
def compFocalButton2(*args):
	compFocalD="Composition does not direct the viewer's eye to subject for over 5 seconds of viewing. Focal length choice vaguely supports the composition. "
	compFocalF="Composition does not direct the viewer's eye to the subject. Focal length choice does not support the composition. "
	compFocalRow2=cmds.radioButtonGrp( "cflButGrp2", q=1, sl=1)
	if (compFocalRow2 ==1):
		cmds.intFieldGrp( "cflIntField", e=1, value1=75)
		cmds.scrollField("cflTSList", e=1, cl=1)
		cmds.scrollField("cflTSList", e=1, insertText=compFocalD)
		updateGradeTotal()
	else:
		cmds.intFieldGrp( "cflIntField", e=1, value1=100)
		cmds.scrollField("cflTSList", e=1, cl=1)
		cmds.scrollField("cflTSList", e=1, insertText=compFocalF)
		updateGradeTotal()

# Create the Lighting Row 1 button, comments and grade functions
def lightingButton1(*args):
	lightingA="Renders show exemplary understanding of soft light and shadows. The lighting directs the viewers eye to the subject matter instantaneously. The lighting has a strong style based on cinema reference."
	lightingB="Renders show an acceptable understanding of soft lighting.  The lighting directs the viewer's eye to the subject after a few seconds of viewing the image. The lighting has a style based on a cinema reference."
	lightingC="Renders show a basic understanding of soft lighting. The lighting directs the views eye to the subject after a 5 seconds of viewing the image. The lighting has a vague style based on a cinema reference."
	lightingRow1=cmds.radioButtonGrp( "lightButGrp1", q=1, sl=1)
	if (lightingRow1 ==1):
		cmds.intFieldGrp( "lightIntField", e=1, value1=100)
		cmds.scrollField("lightTSList", e=1, cl=1)
		cmds.scrollField("lightTSList", e=1, insertText=lightingA)
		updateGradeTotal()
	elif (lightingRow1 ==2):
		cmds.intFieldGrp( "lightIntField", e=1, value1=89)
		cmds.scrollField("lightTSList", e=1, cl=1)
		cmds.scrollField("lightTSList", e=1, insertText=lightingB)
		updateGradeTotal()
	else:
		cmds.intFieldGrp( "lightIntField", e=1, value1=79)
		cmds.scrollField("lightTSList", e=1, cl=1)
		cmds.scrollField("lightTSList", e=1, insertText=lightingC)
		updateGradeTotal()
		
# Create the Lighting Row 2 button, comments and grade functions		
def lightingButton2(*args):
	lightingD="Renders show below average understanding of soft lighting.  The lighting does not direct the viewer's eye to the subject. No lighting style based on cinema reference."
	lightingF="Renders show unsatisfactory understanding of soft lighting.  A strong lack of appeal of lighting direction and complete lack of style based on cinema reference."
	lightingRow2=cmds.radioButtonGrp( "lightButGrp2", q=1, sl=1)
	if (lightingRow2 ==1):
		cmds.intFieldGrp( "lightIntField", e=1, value1=72)
		cmds.scrollField("lightTSList", e=1, cl=1)
		cmds.scrollField("lightTSList", e=1, insertText=lightingD)
		updateGradeTotal()
	else:
		cmds.intFieldGrp( "lightIntField", e=1, value1=69)
		cmds.scrollField("lightTSList", e=1, cl=1)
		cmds.scrollField("lightTSList", e=1, insertText=lightingF)
		updateGradeTotal()

# Create the Professionalism Row 1 button, comments and grade functions
def proButton1(*args):
	proA="No Deduction."
	proB="Student named their files correctly, image is correct resolution. Student could trouble shoot problems with some help from instructor."
	proC="Student named their files poorly, image is correct resolution. Student had trouble problem solving without instructors help."
	proRow1=cmds.radioButtonGrp( "proButGrp1", q=1, sl=1)
	if (proRow1 ==1):
		cmds.intFieldGrp( "proIntField", e=1, value1=0)
		cmds.scrollField("proTSList", e=1, cl=1)
		cmds.scrollField("proTSList", e=1, insertText=proA)
		updateGradeTotal()
	elif (proRow1 ==2):
		cmds.intFieldGrp( "proIntField", e=1, value1=25)
		cmds.scrollField("proTSList", e=1, cl=1)
		cmds.scrollField("proTSList", e=1, insertText=proB)
		updateGradeTotal()
	else:
		cmds.intFieldGrp( "proIntField", e=1, value1=50)
		cmds.scrollField("proTSList", e=1, cl=1)
		cmds.scrollField("proTSList", e=1, insertText=proC)
		updateGradeTotal()
		
# Create the Professionalism Row 2 button, comments and grade functions		
def proButton2(*args):
	proD="Student did not name their files correctly, image is incorrect resolution. Student often had trouble problem solving without instructors help."
	proF="Student did not name their files correctly, image is incorrect resolution. Student had poor trouble shooting skills."
	proRow2=cmds.radioButtonGrp( "proButGrp2", q=1, sl=1)
	if (proRow2 ==1):
		cmds.intFieldGrp( "proIntField", e=1, value1=75)
		cmds.scrollField("proTSList", e=1, cl=1)
		cmds.scrollField("proTSList", e=1, insertText=proD)
		updateGradeTotal()
	else:
		cmds.intFieldGrp( "proIntField", e=1, value1=100)
		cmds.scrollField("proTSList", e=1, cl=1)
		cmds.scrollField("proTSList", e=1, insertText=proF)
		updateGradeTotal()
		
# Create the Art Frame and uses formlayout to control positioning of the various elements	
def gradeFrame():
	cmds.frameLayout( label='Grade', cll=True, labelAlign='center', borderStyle='etchedIn' )
	cmds.columnLayout()
	global gradeFrm
	gradeFrm = cmds.formLayout()
	global lightGradeTotal
	global cflGradeTotal
	global aanqGradeTotal
	global proGradeTotal
	
# Lighting radio button, textScrollList and intField Function
def lightingFunction():
	global lightSeparator
	lightGroup1 = cmds.radioButtonGrp( "lightButGrp1", numberOfRadioButtons=3, label='Lighting (60%)', labelArray3=['A+ -A', 'B+ -B', 'C+ -C'], onCommand=lightingButton1 )
	lightGroup2 = cmds.radioButtonGrp( "lightButGrp2", numberOfRadioButtons=2, shareCollection=lightGroup1, label='', labelArray2=['D', 'F'], onCommand=lightingButton2  )
	cmds.formLayout( gradeFrm, edit=1, attachForm=[[lightGroup1, "top", 5], [lightGroup1, "left", 5]])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[lightGroup2, "left", 5, ], attachControl=[lightGroup2, "top", 5, lightGroup1])
	lightShapeField=cmds.intFieldGrp( "lightIntField", numberOfFields=1, label='Grade', changeCommand=updateGradeTotal)
	lightTextScrollList=cmds.scrollField("lightTSList", w=200, h=150, wordWrap=1)
	lightCommentsLabel=cmds.text( label='Comments' )
	cmds.formLayout( gradeFrm, edit=1, attachForm=[lightShapeField, "top", 5], attachControl=[lightShapeField, "top", 10, lightGroup2])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[lightTextScrollList, "left", 140], attachControl=[lightTextScrollList, "top", 10, lightShapeField])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[lightCommentsLabel, "left", 60], attachControl=[lightCommentsLabel, "top", 10, lightShapeField])
	lightSeparator=cmds.separator( height=15, width=460, style='in' )
	cmds.formLayout( gradeFrm, edit=1, attachForm=[lightSeparator, "left", 5], attachControl=[lightSeparator, "top", 5, lightTextScrollList])

# Composition and Focal Length radio button, textScrollList and intField Function
def compFocalLength():
	global cflSeparator
	cflGroup1 = cmds.radioButtonGrp( "cflButGrp1", numberOfRadioButtons=3, label='Comp/Focal Length (15%)', labelArray3=['A+ -A', 'B+ -B', 'C+ -C'], onCommand=compFocalButton1 )
	cflGroup2 = cmds.radioButtonGrp( "cflButGrp2", numberOfRadioButtons=2, shareCollection=cflGroup1, label='', labelArray2=['D', 'F'], onCommand=compFocalButton2  )
	cmds.formLayout( gradeFrm, edit=1, attachForm=[cflGroup1, "left", 5], attachControl=[cflGroup1, "top", 5, lightSeparator])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[cflGroup2, "left", 5, ], attachControl=[cflGroup2, "top", 5, cflGroup1])
	cflShapeField=cmds.intFieldGrp( "cflIntField", numberOfFields=1, label='Grade', changeCommand=updateGradeTotal)
	cflTextScrollList=cmds.scrollField("cflTSList", w=200, h=150, wordWrap=1)
	cflCommentsLabel=cmds.text( label='Comments' )
	cmds.formLayout( gradeFrm, edit=1, attachForm=[cflShapeField, "top", 5], attachControl=[cflShapeField, "top", 10, cflGroup2])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[cflTextScrollList, "left", 140], attachControl=[cflTextScrollList, "top", 10, cflShapeField])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[cflCommentsLabel, "left", 60], attachControl=[cflCommentsLabel, "top", 10, cflShapeField])
	cflSeparator=cmds.separator( height=15, width=460, style='in' )
	cmds.formLayout( gradeFrm, edit=1, attachForm=[cflSeparator, "left", 5], attachControl=[cflSeparator, "top", 5, cflTextScrollList])
	
# Antialiasing and Noise Quality radio button, textScrollList and intField Function
def antiAliasNoiseQual():
	global aanqSeparator
	aanqGroup1=cmds.radioButtonGrp( "aanqRadButGrp1", numberOfRadioButtons=3, label='Anitalias/Noise Qual (15%)', labelArray3=['A+ -A', 'B+ -B', 'C+ -C'], onCommand=antiAliasButton1)
	aanqGroup2=cmds.radioButtonGrp( "aanqRadButGrp2", numberOfRadioButtons=2, shareCollection=aanqGroup1, label='', labelArray2=['D', 'F'], onCommand=antiAliasButton2)
	cmds.formLayout( gradeFrm, edit=1, attachForm=[aanqGroup1, "left", 5], attachControl=[aanqGroup1, "top", 5, cflSeparator])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[aanqGroup2, "left", 5, ], attachControl=[aanqGroup2, "top", 5, aanqGroup1])
	aanqShapeField=cmds.intFieldGrp( "aanqIntField", numberOfFields=1, label='Grade', changeCommand=updateGradeTotal)
	aanqTextScrollList=cmds.scrollField("aanqTSList", w=200, h=150, wordWrap=1)
	aanqCommentsLabel=cmds.text( label='Comments' )
	cmds.formLayout( gradeFrm, edit=1, attachForm=[aanqShapeField, "top", 5], attachControl=[aanqShapeField, "top", 10, aanqGroup2])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[aanqTextScrollList, "left", 140], attachControl=[aanqTextScrollList, "top", 10, aanqShapeField])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[aanqCommentsLabel, "left", 60], attachControl=[aanqCommentsLabel, "top", 10, aanqShapeField])
	aanqSeparator=cmds.separator( height=15, width=460, style='in' )
	cmds.formLayout( gradeFrm, edit=1, attachForm=[aanqSeparator, "left", 5], attachControl=[aanqSeparator, "top", 5, aanqTextScrollList])
	
# Professionalism radio button, textScrollList and intField Function
def professionalism():
	global proSeparator
	proGroup1 = cmds.radioButtonGrp( "proButGrp1", numberOfRadioButtons=3, label='Professionalism (10%)', labelArray3=['A+ -A', 'B+ -B', 'C+ -C'], onCommand=proButton1 )
	proGroup2 = cmds.radioButtonGrp( "proButGrp2", numberOfRadioButtons=2, shareCollection=proGroup1, label='', labelArray2=['D', 'F'], onCommand=proButton2  )
	cmds.formLayout( gradeFrm, edit=1, attachForm=[proGroup1, "left", 5], attachControl=[proGroup1, "top", 5, aanqSeparator])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[proGroup2, "left", 5, ], attachControl=[proGroup2, "top", 5, proGroup1])
	proShapeField=cmds.intFieldGrp( "proIntField", numberOfFields=1, label='Grade', changeCommand=updateGradeTotal)
	proTextScrollList=cmds.scrollField("proTSList", w=200, h=150, wordWrap=1)
	proCommentsLabel=cmds.text( label='Comments' )
	cmds.formLayout( gradeFrm, edit=1, attachForm=[proShapeField, "top", 5], attachControl=[proShapeField, "top", 10, proGroup2])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[proTextScrollList, "left", 140], attachControl=[proTextScrollList, "top", 10, proShapeField])
	cmds.formLayout( gradeFrm, edit=1, attachForm=[proCommentsLabel, "left", 60], attachControl=[proCommentsLabel, "top", 10, proShapeField])
	proSeparator=cmds.separator( height=15, width=460, style='in' )
	cmds.formLayout( gradeFrm, edit=1, attachForm=[proSeparator, "left", 5], attachControl=[proSeparator, "top", 5, proTextScrollList])
	cmds.setParent('..')
	cmds.setParent('..')
	cmds.setParent('..')
	
# Built the GUI	
windowGUI()
fileFrame()
gradeTotalsFrame()
gradeFrame()
lightingFunction()
compFocalLength()
antiAliasNoiseQual()
professionalism()
