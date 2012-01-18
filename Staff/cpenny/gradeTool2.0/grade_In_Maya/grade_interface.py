
import maya.cmds as cmds  
import get_Sections as get_sec
reload(get_sec)
#import xlrd
#from grade_In_Maya import get_Sections 

class Slider_button():
    grade_vals = [65, 72, 80, 90, 100]
    def __init__(self, w=470, h=150,
                    title = "Unknown",
                    sections_list = [[u'Main Section One', [u'Sub Section 1', u'Sub Section 2', u'Sub Section 3']],
                    [u'Main Section Two', [u'Edgeflow/ Necessary geo', u'Built in Logical pieces', u'Engons/ Problem geo', u"UV's Properly flattened and laid out"]],
                    [u'Turn In Requirements', [u'Maya File Named Properly', u'Reference / Grade Sheet Enclosed', u'Objects named', u'Objects/scene grouped', u'Objects on separate layers', u'Freeze Transforms', u'History deleted', u'Object pivots centered']]],
                    info = [u'Sub Section 1', [0.5], [u'All or almost all object shapes are specific and accurate to reference in entire scene. Excellent attention to the varied softness or sharpness of edges on objects compared to reference.', u'Many objects in scene are specific and accurate to reference. Good attention to the varied softness or sharpness of edges on objects compared to reference.', u'Some objects are specific and unique and accurate to reference. Some generic objects.  Average attention to the varied softness or sharpness of edges on objects compared to reference.', u' Hardly any objects are specific and accurate to reference; feel generic.   Poor attention to the varied softness or sharpness of edges on objects compared to reference.   Missing bevels/ holding edges on objects which still feel like block-ins in most of scene.   Missing critical objects or details to make scene feel complete. '], [22.0]]
                    ):
        
        self.title = info[0]
        self.worth = info[1]
        
        self.sec_A_Reason = info[0]
        self.sec_B_Reason = info[1]
        self.sec_C_Reason = info[2]
        self.sec_DF_Reason = info[3]
        #dictionary for grade range and information on why

        self.grade_range = { 65 : [[0.52, 0, 0], self.sec_DF_Reason], 72: [[0.84, 0.36, 0], self.sec_DF_Reason], 80: [[0.43, 0.41, .08], self.sec_C_Reason],
            90:  [[1, 0.88, 0], self.sec_B_Reason], 100: [[0, 0.5, 0], self.sec_A_Reason]}
        self.grade_state = 100
        self.main = cmds.columnLayout()
        
        cmds.text(title)

        self.info_area = cmds.scrollField(w=w, h=(h *.75), bgc=[0, 0.5, 0], keyPressCommand=self.scroll_change)
        self.slider = cmds.floatSliderGrp( v=100, min=0, max=100, field=True,
            dc=self.update, cc=self.update, w=w, h=(h *.25), cw=[[1, w*.15], [2, w*.85]])
        cmds.setParent('..')
        

    def update(self, *args):        
        color_val = cmds.floatSliderGrp(self.slider, q=1, v=1)

        for grade in Slider_button.grade_vals:
            if color_val < grade:
                self.grade_state = grade
                cmds.scrollField(self.info_area, e=1, text=self.grade_range[grade][-1]) 
                cmds.scrollField(self.info_area, e=1, bgc=self.grade_range[grade][0])    

                break
            
            
    def scroll_change(self, *args):
        # color_val = cmds.floatSliderGrp(self.slider, q=1, v=1)
        current_text = cmds.scrollField(self.info_area, q=1, text=True)
        self.grade_range[float(self.grade_state)][-1] = current_text
        
        
def section_aquire(start = 0, end = 1,
                   start_range = 1,
                   end_range = 7,
                   *args):
    global num_Sec
    file_loc = cmds.textField('sheet_load', q =True, tx = True)
   
    sec_list = []
    sections = []

    for n in range(int(num_Sec)):
        sections_list = []
        n = str(n)
        col = 'col' + n
        start_range = 'start_range' + n
        start_range = cmds.intField(start_range, q = True, v = True)
        
        end_range = 'end_range' + n
        end_range = cmds.intField(end_range, q = True, v = True)

        start = 'start' + n
        start = cmds.intField(start, q = True, v = True)

        end = 'end' + n
        end  = cmds.intField(end, q = True, v = True)
      

        col = get_sec.Get_Sections(file_loc = file_loc, start_Range = start_range, end_Range = end_range, start = start, end = end)
        col= col.get_sections()
        sec_list.append(col)

    print sec_list
    print sections
    grade_gui(sections_list = sec_list, sections = sections)

    '''    
    col2= get_sec.Get_Sections(file_loc = file_loc, start_Range = start_range1, end_Range = end_range1, start = start1, end = end1)
    col2 = col2.get_sections()
    
    row1 = get_sec.Get_Sections(start_Range = 2, end_Range = 4, start = 2, end = 3).get_info()
    
    #row2 = get_sec.Get_Sections(start_Range = 4, end_Range = 6, start = 2, end = 3).get_info()
    '''
    
    #print col1, col2
    
def save_pref(*args):
    global num_Sec
    
    range_info = []
    
    num_Sec = int(num_Sec)
    counter = 0
    '''
    for field in range[0:num_Sec]:

        start_range = cmds.intField('start_range'+str(counter), q= True, v =True)
        start = cmds.intField('start'+str(counter),q= True, v = True)
        end_range = cmds.intField('end_range'+str(counter),q= True, v = True)
        end = cmds.intField('end'+str(counter),q= True, v = True)
        
        range_info.append(start_range)
        counter = +1
    '''
    section_aquire()


def main_title(title = 'Unknown', *args):

    cmds.text(title)
    cmds.separator()
    cmds.setParent('mainCol')

def get_file(*args):
    filename = cmds.fileDialog2(fileMode=1, caption="Import Excell")
    cmds.textField('sheet_load', e = True, tx = filename[0])

def grade(*args):
    print "GRADING"
    '''
    Check if sheet exists, if not then create one using project turned in name
    Or name of file that is saved as.

    file_name = cmds.file(q = True, sn = True)

    os.system("open %s" %excell_loc)

    cmds.file(file_loc, force= True, open= True)
    cmds.file(save= True, force = True, type = 'mayaAscii')

        
    '''


def grade_gui(sections_list = [], sections = [], *args):
    
    
    #print sections_list, sections
    win2 = "Grading"
    win = 'Start_Window'
    if cmds.window(win, ex = True):
        cmds.deleteUI(win)  
    if cmds.window(win2, ex = True):
        cmds.deleteUI(win2)
    if cmds.windowPref(win2, ex = True):
        cmds.windowPref(win2, r= True)
    
    cmds.window(win2, tlc = [0, 900])
    cmds.scrollLayout(w = 500, h = 800)
    cmds.columnLayout('mainCol')
    cmds.rowColumnLayout('excellTitleRowCol', nc= 2, cw = ([1,150],[2,200]))
    cmds.text(' ')
    
    xls_Name = cmds.file(q = True, sn = True)
    #print xls_Name
    cmds.textField('xll_Name', tx = xls_Name)
    
    cmds.setParent('excellTitleRowCol')
    cmds.setParent('mainCol')
    #print sections_list
    #match them and build list from here.
    for each in sections_list:
        main_title(title = each[0])
        for sect in each[1]:
            title = sect[0]
            info = sect[2]
            #print title, info
            Slider_button(title = title, info = info)

    cmds.button('Grade', c = grade)

    cmds.showWindow(win2)

def gui():
    '''
    only if preference file doesn't exist in scripts folder will this window appear
    otherwise use preferences from that file
    
    
    grade_pref.bld
    '''
    global num_Sec
    
    num_Sec = ''
    result = cmds.promptDialog(
                title='Grading Start',
                message='Assumming your sections are organized like template.\nEnter Number of Sections:',
                button=['OK', 'Cancel'],
                defaultButton='OK',
                cancelButton='Cancel',
                dismissString='Cancel', tx = '2')

    if result == 'OK':
            num_Sec = cmds.promptDialog(query=True, text=True)
            
            
    win = "Start_Window"
    width = 200
    if cmds.window(win, ex = True):
        cmds.deleteUI(win)
    if cmds.windowPref(win, ex = True):
        cmds.windowPref(win, r= True)
    
    cmds.window(win, w = width)
    cmds.columnLayout()
    
    cmds.textField('sheet_load', w = width, tx = '/Users/ChrisP/template.xls')
    cmds.button("Load Excell Sheet", c = get_file)
    
    for n in range(int(num_Sec)):
        
        cmds.rowColumnLayout(nc = 4)
    
        cmds.text("Spaces")
        
        cmds.text(' ')
        cmds.text("Columns")
        cmds.text(' ')

        cmds.text('Start Range')
        cmds.intField('start_range'+str(n), v = 1)
        cmds.text('Start')
        cmds.intField('start'+str(n), v = 0)
        cmds.text('End Range')
        cmds.intField('end_range'+str(n), v = 7)
        cmds.text('End')
        cmds.intField('end'+str(n), v = 1)
        
        cmds.separator()
        cmds.separator()
        cmds.separator()
        cmds.separator()
            
        cmds.setParent('..')

    cmds.button('Initalize', c = save_pref )
    
    
    cmds.showWindow(win)
