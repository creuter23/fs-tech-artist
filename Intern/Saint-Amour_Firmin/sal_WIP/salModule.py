#module of gui components
'''
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
	
'''
import pymel.core as pm


# Section class
# name = what will be displayed in that grading section
# layout = the formLayout that these GUI components will be attached to
# total = the total function the function that will run through and add up all the grades
# command = the onCommand for the radio Buttons

class Section():
    def __init__(self, name, layout, command , total, control=''):
        self.name = name
        
        self.control = control
        self.command = command
        self.total = total
        self.layout = layout
        
    def create(self):
        
        if self.control == '':
            
            self.row01 = pm.radioButtonGrp( numberOfRadioButtons = 3, label = '%s (45)' % self.name, labelArray3=['A+ -A', 'B+ -B', 'C+ -C'], onCommand = self.command)
            self.row02 = pm.radioButtonGrp(  numberOfRadioButtons = 2, shareCollection = self.row01, label='', labelArray2=['D', 'F'], onCommand = self.total)
            pm.formLayout( self.layout , edit=1, attachForm=[[self.row01, "top", 5], [self.row01, "left", 5]])
            pm.formLayout( self.layout , edit=1, attachForm=[self.row02, "left", 5, ], attachControl=[self.row02, "top", 5, self.row01])
            self.intField = pm.intFieldGrp( numberOfFields = 1, label = 'Grade', changeCommand = self.total)
            self.comments = pm.text( label = 'comments')
            self.scrollList = pm.scrollField( w=200, h=150, wordWrap=1)
            self.separator = pm.separator( height=15, width=460, style='in' )
    
            pm.formLayout( self.layout , edit=1, attachForm=[self.intField, "top", 5], attachControl=[self.intField, "top", 10, self.row02])
            pm.formLayout( self.layout , edit=1, attachForm=[self.scrollList, "left", 140], attachControl=[self.scrollList, "top", 10, self.intField])
            pm.formLayout( self.layout , edit=1, attachForm=[self.comments, "left", 60], attachControl=[self.comments, "top", 10, self.intField])
            pm.formLayout( self.layout , edit=1, attachForm=[self.separator, "left", 60], attachControl=[self.separator, "top", 10, self.scrollList])
        
            return self.separator
        
        else:
            
            self.row01 = pm.radioButtonGrp( numberOfRadioButtons = 3, label = '%s (45)' % self.name, labelArray3=['A+ -A', 'B+ -B', 'C+ -C'], onCommand = self.command)
            self.row02 = pm.radioButtonGrp(  numberOfRadioButtons = 2, shareCollection = self.row01, label='', labelArray2=['D', 'F'], onCommand = self.total)
            pm.formLayout( self.layout , edit=1, attachForm=[[self.row01, "top", 5], [self.row01, "left", 5]] , attachControl=[self.row01, "top", 5, self.control])
            pm.formLayout( self.layout , edit=1, attachForm=[self.row02, "left", 5, ], attachControl=[self.row02, "top", 5, self.row01])
            self.intField = pm.intFieldGrp( numberOfFields = 1, label = 'Grade', changeCommand = self.total)
            self.comments = pm.text( label = 'comments')
            self.scrollList = pm.scrollField( w=200, h=150, wordWrap=1)
            self.separator = pm.separator( height=15, width=460, style='in' )
    
            pm.formLayout( self.layout , edit=1, attachForm=[self.intField, "top", 5], attachControl=[self.intField, "top", 10, self.row02])
            pm.formLayout( self.layout , edit=1, attachForm=[self.scrollList, "left", 140], attachControl=[self.scrollList, "top", 10, self.intField])
            pm.formLayout( self.layout , edit=1, attachForm=[self.comments, "left", 60], attachControl=[self.comments, "top", 10, self.intField])
            pm.formLayout( self.layout , edit=1, attachForm=[self.separator, "left", 60], attachControl=[self.separator, "top", 10, self.scrollList])
        
            return self.separator
        

