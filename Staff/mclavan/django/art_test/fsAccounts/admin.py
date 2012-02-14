from django.contrib import admin
from art_test.accounts.models import Student, Art_Test, Disc, Art_Director



#===============================================================================
# Define interface 'views' to admin site
#===============================================================================
class ArtTest_Admin(admin.ModelAdmin):
    list_display = ('art_director', 'AD_Email', 'AT_status', 'student')







#===============================================================================
# Register the classes
#===============================================================================
admin.site.register(Art_Director)
admin.site.register(Student)
admin.site.register(Art_Test, ArtTest_Admin)
admin.site.register(Disc)
