from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink

# Create your models here.
class Student(models.Model):
    user = models.ForeignKey(User, unique=True)
    name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    email = models.EmailField(max_length=100)
    disc = models.CharField(null=True, max_length=18)
    classid = models.CharField(max_length=4)
    student_id = models.IntegerField(10)
    comments = models.CharField(null=True, max_length=255)

    def __unicode__(self):
        return '%s: %s %s' %(self.name, self.user_name, self.email)
 
# Username: mclavan_hsdb dbPassword = FS!@#$% student table
class Art_Test(models.Model):
    # Setting up enum type
    status_types = ((u'p', u'passed'), (u'1', u'1'), (u'2', u'2'), (u'3', u'3'), (u'e', u'except'))
    asset_types = ((u'y', u'yes'), (u'n', u'no'))
    asses_types = ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5))
    AT_status = models.CharField(max_length=5, choices=status_types)
    asset_status = models.CharField(max_length=2, choices=asset_types)
    assesment = models.CharField(max_length=6, choices=asses_types)
    student = models.ForeignKey(Student)
    art_director = models.CharField(max_length=50)
    AD_Email = models.EmailField(max_length=100)
    






class Disc(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    category = models.ForeignKey('users.Category')

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('view_blog_post', None, { 'slug': self.slug })

class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('view_disc_category', None, { 'slug': self.slug })


from django import forms
from django.contrib.auth.models import User



class ContactForms(forms.Form):
    name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    
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