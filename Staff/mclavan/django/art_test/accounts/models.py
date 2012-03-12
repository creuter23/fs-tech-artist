from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink
from django.db.models.signals import post_save
from django.db.models import signals
from art_test.accounts.signals import create_profile
#===============================================================================
# Model classes to define database connections
#===============================================================================


GENDER_CHOICES = ( ('F', ('Female')), ('M', ('Male')),)

DISC_NAMES = (( u'ANI', u'Animation'), (u'SAL', u'Shading And Lighting'), (u'VFX', u'Visual FX'), 
             (u'VEM', u'Vehicle Modeling'), (u'ARC', u'Architectural Modeling'),
             (u'CMD', u'Character Modeling'),(u'RIG', u'Rigging'), (u'COMP', u'Compositing'))

STATUS_TYPES = ((u'p', u'passed'), (u'1', u'first attempt'), (u'2', u'second attempt'), (u'3', u'third attempt'), (u'e', u'except'))

USER_LEVEL_CHOICE = ((u's', u'Student'), (u'i', u'Instructor'), (u'a', u'Admin')) # Choice Vars for user_level

ASSET_TYPES = ((u'y', u'yes'), (u'n', u'no')) #Art Test Currently Enrolled?

ASSES_TYPES = ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5))  # Assesment of art test work


#-----------------------STUDENT----yX6Ec3jN4vK6------------------------------------- 
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)  #access the built in user manager
    alt_email = models.EmailField(null=True, blank=True, max_length=100) #non-fullsail.edu domain
    disc = models.ForeignKey('accounts.Disc', null=True, blank=True,) #Prob need this to be a foreign key
    class_id = models.CharField(max_length=4) # The 3 letter course id such as DRC or PCC2
    student_id = models.IntegerField(max_length=10) #The student id given from the school
    user_level_choice = ((u's', u'Student'), (u'i', u'Instructor'), (u'a', u'Admin')) # Choice Vars for user_level
    user_level = models.CharField(max_length=15, choices=user_level_choice) # User_Level Field
    #picture = models.ImageField(('Picture/Avatar'), upload_to='profile_photo', blank=True) # pictures!
    comments = models.CharField(null=True, blank=True, max_length=255) # short comment field

    def __unicode__(self):
        return '%s %s' %(self.user.first_name, self.user.last_name) #return first, last, email

'''
class Student(models.Model)
    art_test_level = (('c', 'current'), ('p', 'passed'), )
'''

'''
Main Targets
1) Students can signup for art test.
    - Staff can see who is assigned for what art test.
    - Art Director - can see all student signed up under their art test.
2) Student can see which art test they are signed up for.
    - They can see their current status.
3) Matt in anp can direct student to sign up for the sigth.
    - Monday - Matt and 
4) Students can put there current focus down.

'''
    
#run lambda function to create or update profile from object    
#User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
#-----------------------STUDENT END--------------------------------------

#-----------------------Create User Profile------------------------------
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        UserProfile.objects.create(user=instance)
#        
#post_save.connect(create_profile, sender=User)
#-----------------------Create User Profile END--------------------------

# ArtTest, Staff, ArtDirector, ANP, PCC1, PCC2, PCC3
# user_profile = request.user.get_profile()
# Group(name='ArtTest', user_profile)


class Group(models.Model):
    name = models.CharField(max_length=25)
    members = models.ManyToManyField(UserProfile, through='Membership')
    def __unicode__(self):
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(UserProfile)
    group = models.ForeignKey(Group)
    def __unicode__(self):
        return '%s - %s' % (self.person, self.group) 

class Art_Test_Attempt(models.Model):
    status_types = ((u'p', u'passed'), (u'1', u'1'), (u'2', u'2'), (u'3', u'3'), (u'e', u'except'))
    asset_types = ((u'y', u'yes'), (u'n', u'no'), (u'c', 'current'))
    asses_types = ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5))

    student = models.ForeignKey(UserProfile)
    # Disc type will include concept share web address.
    disc_name = models.ForeignKey('accounts.Disc')

    # Students can only take art test in each disc no more than three times.
    #   Unless approved by staff (except)
    AT_status = models.CharField(max_length=5, choices=status_types)
    
    # current date would be nessary.
    # 1203, 1204, etc...
    month = models.CharField(max_length=4)
    asset_status = models.CharField(max_length=4, choices=asset_types)
    assesment = models.IntegerField(max_length=6, choices=asses_types)
    # Comment area might be nice.
    
    # Recording the staff member that administered the test (NOT WHO IS IN CHARGE OF ART TEST)
    #    In case different people where in charge.
    def __unicode__(self):
        return '%s - %s - %s - %s %s user: %s' % (self.month, self.disc_name.name, self.asset_status,
                                         self.student.user.first_name, self.student.user.last_name, self.student.user.username)
    
#-----------------------ART TEST----------------------------------------- 
class Art_Test(models.Model):
    #### FIELDS #####
    disc_name = models.ForeignKey('accounts.Disc')

    #art_director = models.CharField(max_length=50)
    art_director = models.ForeignKey(User)
    AD_Email = models.EmailField(max_length=100)
    
    ###### OUTPUT #####
    def __unicode__(self):
        return '%s %s:  %s' %(self.student.user.first_name, self.student.user.last_name, self.disc_name)
#-----------------------ART TEST END---------------------------------------





#-----------------------DISCIPLINE----------------------------------------- 
class Disc(models.Model):
    name = models.CharField(max_length=25, choices=DISC_NAMES)
    conceptshare_url = models.URLField(max_length=200)
    #notes = models.TextField()
    updated = models.DateTimeField(db_index=True, auto_now_add=True)
    #    category_choice = ((u'0', u'Fine Arts'), (u'1', u'Animation'), (u'2', u'Tech Arts'), 
    #             (u'3', u'Modeling'), (u'4', u'Finals Department'),
    #             (u'5', u'Character Modeling'))
    #    category = models.CharField(max_length=25, choices=category_choice)
    #category = models.ForeignKey('accounts.Category')
    #disc_director = models.ForeignKey('accounts.Art_Director')
    def __unicode__(self):
        return '%s' % self.name

#    @permalink
#    def get_absolute_url(self):
#        return ('view_blog_post', None, { 'slug': self.name })
#-----------------------DISCIPLINE END----------------------------------------



#-----------------------CATEGORY----------------------------------------------
class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('view_disc_category', None, { 'slug': self.slug })
#-----------------------CATEGORY END-------------------------------------------






#===============================================================================
# Unused Code... Delete before production ready
#===============================================================================





#===============================================================================
# Panel Review... This needs to be moved to its own app
#===============================================================================




'''

from django.db import models
class Page(models.Model):   
    title = models.CharField(maxlength=200, core=True)
    content = models.TextField(null=True, blank=True)

#-----------------------ART DIRECTOR----------------------------------------- 
class Art_Director(models.Model):
    user = models.ForeignKey(User, unique=True)
    discipline = models.ForeignKey('accounts.Disc')

    def __unicode__(self):
        return '%s %s' %(self.user.first_name, self.user.last_name)
#-----------------------ART DIRECTOR END--------------------------------------






    disc_choices = ((u'ANI', u'Animation'), (u'SAL', u'Shading and Lighting'), (u'VFX', u'Visual FX'), 
             (u'VEH', u'Vehicle Modeling'), (u'ARCH', u'Architectural Modeling'),
             (u'CHM', u'Character Modeling'),(u'RIG', u'Rigging'), (u'COMP', u'Compositing'))



from django import forms
from django.contrib.auth.models import User

@models.permalink
def get_absolute_url(self):
    return ('mainsignup', [str(self.id)])


'''

'''

class ContactForms(forms.Form):
    name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    
'''
'''  I think this should go into the forms.py file
class SignupForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=30,
    widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(max_length=30,
    widget=forms.PasswordInput(render_value=False))
    
    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("This username is already in use. lease choose another.")
    
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("You must type the same password each time")
        return self.cleaned_data
    
    def save(self):
        new_user = User.objects.create_user(username=self.cleaned_data['username'],
                                            email=self.cleaned_data['email'],
                                            password=self.cleaned_data['password1'])
        return new_user
'''

'''
class Course_Info(models.Model):
    
    cList = '3DF,ENC,MCR,SAL,EAP,ART1,ART2,CMA,HAM,GAM,FOP,FOA,MOD,CDC,2DA,CFM,PRM,CRI,CAN,ACG,STE,CSF,VEF,PSP,ANP,PCC1,PCC2,PCC3,PAS,Other'
    courseList = cList.split(',')
    
'''
