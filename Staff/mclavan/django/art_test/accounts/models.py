from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink
from django.db.models.signals import post_save
from django.db.models import signals
from art_test.accounts.signals import create_profile
#===============================================================================
# Model classes to define database connections
#===============================================================================


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




#-----------------------ART TEST----------------------------------------- 
class Art_Test(models.Model):
    # Setting up enum type
    student = models.ForeignKey(UserProfile)
    ###### VARS ######

    status_types = ((u'p', u'passed'), (u'1', u'1'), (u'2', u'2'), (u'3', u'3'), (u'e', u'except'))
    asset_types = ((u'y', u'yes'), (u'n', u'no'))
    asses_types = ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5))
    #### FIELDS #####
    disc_name = models.ForeignKey('accounts.Disc')
    AT_status = models.CharField(max_length=5, choices=status_types)
    asset_status = models.CharField(max_length=4, choices=asset_types)
    assesment = models.IntegerField(max_length=6, choices=asses_types)
    #art_director = models.CharField(max_length=50)
    art_director = models.ForeignKey(User)
    AD_Email = models.EmailField(max_length=100)
    
    ###### OUTPUT #####
    def __unicode__(self):
        return '%s %s:  %s' %(self.student.user.first_name, self.student.user.last_name, self.disc_name)
#-----------------------ART TEST END---------------------------------------

    



#-----------------------DISCIPLINE----------------------------------------- 
class Disc(models.Model):
    disc_names = ((u'Animation', u'Animation'), (u'Shading And Lighting', u'Shading and Lighting'), (u'VFX', u'Visual FX'), 
             (u'Vehicle Modeling', u'Vehicle Modeling'), (u'Architectural Modeling', u'Architectural Modeling'),
             (u'Character Modeling', u'Character Modeling'),(u'Rigging', u'Rigging'), (u'Compositing', u'Compositing'))
    name = models.CharField(max_length=25, choices=disc_names)
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

'''



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
