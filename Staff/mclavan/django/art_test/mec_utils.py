
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


def populate_disc():
    disc_names = (u'ANI', u'SAL', u'VFX', 
                 u'VEM', u'ARC',
                 u'CMD',u'RIG', u'COMP')
    base_path = 'http://conceptshare.fullsail.com/w=33454'
    for i, disc_name in enumerate(disc_names):
        new_path = '%s%s' % (base_path, i + 1)
        # Check to see if they exists already.
        result = Disc.object.filter(name=disc_name)
        if not result:
            disc_obj = Disc(name=disc_name, conceptshare_url=new_path)
            disc_obj.save()
            

