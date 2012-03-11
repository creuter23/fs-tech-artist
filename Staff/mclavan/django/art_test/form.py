from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import Input
from django.forms import ModelForm
from django.db import models
from art_test.accounts.models import *
from django.utils.translation import ugettext_lazy as _

#attrs_dict = { 'class': 'required' }

#===============================================================================
# Form Classes used to generate a profile linked to a user
#===============================================================================
class SignupForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False))
    
    #---------------------------CLEANS INPUT DATA FOR----------------------
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
        
        #######ADD FIRST AND LAST NAME TO USER DATA#########
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save()
        #######USER PROFILE SETTINGS ##########
        
        
        #User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
#        user_profile = new_user.get_profile()
#        print user_profile

        return new_user






'''
        def user_update(self):
            updated = User.objects.set(first_name=self.cleaned_data['first_name'],
                                       last_name=self.cleaned_data['last_name'])
            
            return updated
'''
    
                #first_name = self.cleaned_data["first_name"]
                #first_name = self.cleaned_data["last_name"]
#===============================================================================
#  Profile Form
#===============================================================================
#
#
#class UserProfileForm(ModelForm):
#    class Meta:
#        model = UserProfile
#
'''
class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.user.email
            # self.fields['first_name'].initial = self.instance.user.first_name
            # self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass
     
        email = forms.EmailField(label="Primary email",help_text='')
        class Meta:
          model = UserProfile
          exclude = ('user',)        
     
        def save(self, *args, **kwargs):
            """
            Update the primary email address on the related User object as well.
            """
            u = self.instance.user
            u.email = self.cleaned_data['email']
            u.save()
            profile = super(ProfileForm, self).save(*args,**kwargs)
            return profile
'''
#class Panel_Review(forms.Form):
    #        try:
    #            User.objects.get(first_name=self.cleaned_data['first_name'])
    #            User.objects.get(last_name=self.cleaned_data['last_name'])
    #        except:
    #            print("first or last name not submitting, try something else?")
'''
class UserProfile(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password1 = forms.CharField(max_length=30,
    widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(max_length=30,
    widget=forms.PasswordInput(render_value=False))
    
    #---------------------------CLEANS INPUT DATA FOR----------------------
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
        try:
            User.objects.get(first_name=self.cleaned_data['first_name'])
            User.objects.get(last_name=self.cleaned_data['last_name'])
        except:
            print("first or last name not submitting, try something else?")
        return self.cleaned_data

    
    def save(self):
        new_user = User.objects.create_user(username=self.cleaned_data['username'],
                                            email=self.cleaned_data['email'],
                                            password=self.cleaned_data['password1'])
        return new_user

    def user_update(self):
        updated = User.objects.set(first_name=self.cleaned_data['first_name'],
                                   last_name=self.cleaned_data['last_name'])
        return updated



'''

#===============================================================================
# UNUSED ---> Delete before production
#===============================================================================

'''
class ContactForms(forms.Form):
    name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    
    
    #first_name = forms.CharField(max_length=30)
    #last_name = forms.CharField(max_length=30)
'''
