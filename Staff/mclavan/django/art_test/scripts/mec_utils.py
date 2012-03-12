
'''
from accounts.models import UserProfile, Disc, Category, Art_Test, Art_Test_Attempt
ani = Disc.objects.filter(name='Animation')
ani[0].name

from django.contrib.auth.models import User
current_user = User.objects.filter(username='mclavan')
current = UserProfile.objects.filter(user=current_user)
current.user.username
'''

from accounts.models import UserProfile, Disc, Category, Art_Test, Art_Test_Attempt
from django.contrib.auth.models import User

def populate_disc():
    disc_names = (u'ANI', u'SAL', u'VFX', 
                 u'VEM', u'ARC',
                 u'CMD',u'RIG', u'COMP')
    base_path = 'http://conceptshare.fullsail.com/w=33454'
    for i, disc_name in enumerate(disc_names):
        new_path = '%s%s' % (base_path, i + 1)
        # Check to see if they exists already.
        result = Disc.objects.filter(name=disc_name)
        if not result:
            disc_obj = Disc(name=disc_name, conceptshare_url=new_path)
            disc_obj.save()
        else:
            print result, 'Already exists.'
            
def add_students():
    STUDENTS = [
    {'name': 'Django Reinhardt', 'disc': 'VFX',    'courseid': 'ANP' },
    {'name': 'Jimi Hendrix',     'disc': 'SAL',    'courseid': 'ANP' },
    {'name': 'Louis Armstrong',  'disc': 'VFX',    'courseid': 'PCC' },
    {'name': 'Pete Townsend',    'disc': 'SAL',    'courseid': 'PCC' },
    {'name': 'Yanni',            'disc': 'ANI',    'courseid': 'ANP' },
    {'name': 'Wesley Willis',    'disc': 'ANI',    'courseid': 'ANP' },
    {'name': 'John Lennon',      'disc': 'SAL',    'courseid': 'PCC' },
    {'name': 'Bono',             'disc': 'SAL',    'courseid': 'ANP' },
    {'name': 'Garth Brooks',     'disc': 'ANI',    'courseid': 'ANP' },
    {'name': 'Duke Ellington',   'disc': 'VFX',    'courseid': 'PCC' },
    {'name': 'William Shatner',  'disc': 'COMP',   'courseid': 'ANP' },
    {'name': 'Madonna',          'disc': 'COMP',   'courseid': 'ANP' }
    ]    

    for i, student in enumerate(STUDENTS):
        # Get disc
        
        # Split names
        name = student['name'].split()
        fname = name[0]
        lname = ' '
        if len(name) > 1:
            lname = name[-1]
        uname = '%s%s' % (fname, lname[0])
        disc = Disc.objects.filter(name=student['disc'])
        
        # password is incorrect.
        # Check for existing user
        if not User.objects.filter(username=uname):
            current_user = User(username=uname, password='aaaa', first_name=fname,
                 last_name=lname, email=' ')
            current_user.save()

            
        else:
            current_user = User.objects.filter(username=uname)[0]
            print 'Already exists.'
            
        current_prof = UserProfile.objects.filter(user=current_user)[0]
        current_prof.alt_email = ''
        current_prof.user_level = 's'
        current_prof.class_id = student['courseid']
        current_prof.alt_email = ''
        current_prof.student_id = '11223344'
        current_prof.comments = 'none'
        current_prof.save()    
            