'''

Author:
    Firmin Saint-Amour
    
Description:
    Transfers UV sets
    
How To Run:
    import tranfer_uvs
    transfer_uvs.gui()

'''

from maya import cmds


def get_target_meshes():
    '''
    # gets a list of selected objs
    # returns that list
    '''
    selected_objs = cmds.ls(selection= True)
    return selected_objs
    
def get_source_mesh():
    '''
    # queries  the source_field 
    # retuns string
    '''
    source = cmds.textFieldButtonGrp(source_field, query= True, text= True)
    return '%s' % (source)
    
def add_source_mesh(* args):
    '''
    # edits the text of the given textFieldButtonGrp
    # add the name of the selected objects
    '''
    obj = cmds.ls(selection= True)[0]
    cmds.textFieldButtonGrp(source_field, edit= True, text= obj)

def transfer_uvs(source_mesh, target_mesh):
    '''
    # tranfers the uvs
    # takes the source and a target
    '''
    try:
        cmds.transferAttributes(source_mesh, target_mesh, transferUVs= 2,
            transferColors=2, searchMethod= 3, flipUVs= 0,
                            transferNormals= 0, sampleSpace= 1)
        
    except:
        cmds.confirmDialog(title='Error', message='WRONG OBJECT TYPE')
            
def button_cmd(* args):
    '''
    # command fro the button
    '''
    targets = get_target_meshes()
    source = get_source_mesh()
    for target in targets:
        transfer_uvs(source, target)

def gui():
    '''
    # creates the gui
    '''
    win = 'fsa_uvtransfertool'
    if(cmds.window(win, ex = True)):
        cmds.deleteUI(win)
        
    if(cmds.windowPref(win, ex = True)):
        cmds.windowPref(win, remove = True)
    global source_field #  global textFieldButtonGrp for source mesh
    
    my_win = cmds.window(win, title='transfer_uvs' , sizeable= False, mnb= True,
                      width= 200, height= 200)
    cmds.columnLayout(adjustableColumn= True, width= 200)
    
    source_field = cmds.textFieldButtonGrp(text= 'Source Mesh',
          buttonLabel='<<SOURCE<<', columnWidth= ([1, 115], [2, 85]),
                    annotation= 'add source', buttonCommand = add_source_mesh)
    
    cmds.button(width= 200, height= 100, label= 'Transfer To Selected Meshes',
        command= button_cmd,annotation= 'select target meshes after ' +
                                                'source has been added')
    
    cmds.showWindow(my_win)
        