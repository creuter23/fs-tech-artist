#from django.forms import ModelForm
#from art_test.accounts.models import UserProfile
#from registration.forms import RegistrationForm, RegistrationFormTermsOfService, RegistrationFormUniqueEmail
#from registration.models import RegistrationProfile
#
#
#attrs_dict = { 'class': 'required' }
#class ProfileForm(RegistrationFormUniqueEmail, RegistrationFormTermsOfService):
#    GENDER_CHOICES = (
#    (0, 'Select Gender'),
#    (1, 'Male'),
#    (2, 'Female'),)
#    first_name = forms.CharField(widget=forms.TextInput())
#    last_name = forms.CharField(widget=forms.TextInput())
#    picture = forms.ImageField(required=False)
#    gender = forms.IntegerField(widget=forms.Select(choices=GENDER_CHOICES))
#    birth_date = forms.DateField(widget=SelectDateWidget(years=range(1911,1999)))
#    
#    def save(self, user):
#        try:
#            data = user.get_profile()
#        except:
#            data = Profile(user=user)
#            data.first_name = self.cleaned_data["first_name"]
#            data.first_name = self.cleaned_data["last_name"]
#            data.gender = self.cleaned_data["gender"]
#            data.birth_date = self.cleaned_data["birth_date"]
#            data.save()