'''
pipeline.py
Michael Clavan

just picking this apart...
--heiths


Description:
    This script does various action on the pipeline.
    From creating folder structures to return different paths for the pipeline.
   
    
'''
import os
import os.path
import re

BASE_DRIVE_OSX = '/Volumes/3DArts_Intern/Project_pipline/Up'

def create_asset(item_name, item_type='Props', project='0001_Teasers', base_path='/Volumes/3DArts_Intern/Project_pipline/Up'):
    '''
    Add the folder structure for a new asset.
    Arguments:
        item_name (string) = Name of the asset.
        item_type (string) = Acceptable values ('Props', 'Characters', 'Enviroments')
        project (string) = Given project to add sequence to.
        base_path (string) = The base path that the project resides.
        
    '''
    base_path = os.path.join(base_path, project)    
    # item_types = {'Props': True, 'Characters': True, 'Enviroment': True]
    # if item_types['Prop']:
    job_types = ['Model', 'Texture', 'Rig']
    for job_type in job_types:
        # os.makedirs(os.path.join(base_path, 'Assets', item_type, item_name, 'Production'))
        os.makedirs(os.path.join(base_path, 'Assets', item_type, item_name, job_type, 'Production', 'Wip'))
        os.makedirs(os.path.join(base_path, 'Assets', item_type, item_name, job_type, 'Final'))    

# create_asset('Merc', 'Characters')


def create_seq(seq='001-005', project='0001_Teasers', base_path='/Volumes/3DArts_Intern/Project_pipline/Up'):
    '''
    Create a new sequence for the given project.
    Arguments:
        seq (string) = Given range '0001-0010', '01-01'.
        project (string) = Given project to add sequence to.
        base_path (string) = The base path that the project resides.
    '''
    
    base_path = os.path.join(base_path, project, 'Sequences')
    # Jobs to be created in each shot.    
    
    # Breaking up sequence range.
    seq_group = re.match(r'(\d*)-*(\d*)', seq_line)
    seq_group.groups()
    start_shot = int(seq_group.groups()[0])
    end_shot = int(seq_group.groups()[1])
    
    # Create sequence folder
    # os.makedirs(os.path.join(base_path, 'Sequences')
    os.makedirs(os.path.join(base_path, seq))
    for i in xrange(start_shot, end_shot):
        shot_path = os.path.join(base_path, seq, '%d03' % i)
        os.makedirs(shot_path)
        job_types = ['Lighting', 'Animation', 'Layout']
        for job_type in job_types:
            os.makedirs(os.path.join(shot_path, job_type, 'Production', 'Wip'))
            os.makedirs(os.path.join(shot_path, job_type, 'Final'))     

def push_asset(asset_name, asset_type, asset_job, file_path):
    '''
    Update assets Wip file and swqp out most current file.
    '''
    asset_short = {'Model': 'mod', 'Texture': 'text', 'Rig': 'rig'}
    short_name = '%s_%s.ma' % (asset_name.lower(), asset_short[asset_job])
    print 'Asset: %s (%s): \n\thas been updated to WIP and to %s_%s.ma' % (asset_name, asset_type, short_name)

def add_shot(seq, shots):
    '''
    Add a shot to an existing sequence.
    '''
    print 'Added %s to sequence %s' % (seq, shots)
  
class Project():
    '''
    Returns an object will paths to all the parts of the pipeline.
    '''
    def __init__(self, project_name):
        self.name = project_name
        self.assets = '' # this will be connected to the assets object.
        self.sequences = '' # this will be connected to the sequences object.
        
'''
#### Needed
# Create Project
# -- This will create the base folder structure,
# --    Scripts, Env, Assets, Sequence

# Prototypes for Assets, Sequences, Project classes (ZOPE)

-- Notes
base_path = '/Volumes/3DArts_Intern/Project_pipline/Up/Teasers'
base_path = 'smb://studentvfiler/3DArts_Intern/Project_pipline/Up/Teasers/Assets'
os.makedirs(os.path.join(base_path, 'Assets', 'Props', 'Production'))
os.makedirs(os.path.join(base_path, 'Assets', 'Props', 'Production', 'Wip'))
os.makedirs(os.path.join(base_path, 'Assets', 'Props', 'Final'))

for item_type in item_types:
    job_types = ['Model', 'Texture', 'Rig']
    for job_type in job_types:
        os.makedirs(os.path.join(base_path, 'Assets', job_type, item_type, 'Production'))
        os.makedirs(os.path.join(base_path, 'Assets', job_type, item_type, 'Production', 'Wip'))
        os.makedirs(os.path.join(base_path, 'Assets', job_type, item_type, 'Final'))

os.listdir(os.path.join(base_path, 'Assets', 'Props'))

# Regular Expresions
seq_line = '001-001'
seq_group = re.match(r'(\d*)-*(\d*)', seq_line)
seq_group.groups()
start_shot = int(seq_group.groups()[0])
end_shot = int(seq_group.groups()[1])

'''


