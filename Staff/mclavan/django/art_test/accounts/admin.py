from django.contrib import admin
from art_test.accounts.models import UserProfile, Art_Test, Art_Test_Attempt, Disc
from art_test.accounts.models import Group, Membership



#===============================================================================
# Define interface 'views' to admin site
#===============================================================================
'''
class ArtTest_Admin(admin.ModelAdmin):
    list_display = ('student','AD_Email', 'AT_status', 'art_director')
'''

class UserProfile_Admin(admin.ModelAdmin):
    
    list_display = ('user','student_id', 'disc', 'user_level')
    

#===============================================================================
# Register the classes
#===============================================================================
admin.site.register(UserProfile, UserProfile_Admin)
admin.site.register(Art_Test_Attempt)
admin.site.register(Disc)
admin.site.register(Group)
admin.site.register(Membership)