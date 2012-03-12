from django.conf.urls.defaults import patterns, include, url
import art_test.views as views
from django.core.urlresolvers import reverse
from django.contrib.auth.views import login, logout
from django.contrib.auth.models import User
from accounts.models import *
#from art_test.form import ProfileForm





# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#===============================================================================
# Regular expressions used to map urls to functions/scripts
#===============================================================================

urlpatterns = patterns('',
    # matches everything 'else'
    (r'^$', views.gateway),
    # good/bad gateways... still using?
    (r'^bad_gateway/$', views.bad_gateway),
    (r'^user_access/$', views.login),
    (r'^main_page/$', views.site_status),
    (r'^logout/$', views.site_logout),
    # Apply to an art test
    (r'^apply/$', views.apply),   
    (r'^art_apply/$', views.apply_check),
    
    # Test Area
    (r'^main/$', views.site_status2),
    
    #Panel Review Pages...
    (r'^panels/$', views.panels),
    (r'^panel/$', views.panel),
    # signup page ---> inital site registration
    url(r"^signup/$", views.signup, name='mainsignup'),
    
    #Login/Logout/Profile
    (r'^login/$', login),
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout),
    (r'^accounts/profile/$', views.profile),
    
    # the admin documentation and the admin site itself
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    #The search function...
    (r'^search/$', 'search.views.search'),
    #Flat page urls...catchall...
    (r'', include('django.contrib.flatpages.urls')),

)



#===============================================================================
# UNUSED CODE >> Remove Before Production
#===============================================================================
'''

from profiles.forms import UserRegistrationForm




import registration.backends.default.urls as regUrls
from registration.backends.default import DefaultBackend
from basic.members.forms import ProfileForm


    # url(r'^$', 'art_test.views.home', name='home'),
    # url(r'^art_test/', include('art_test.foo.urls')),
    #(r'^signup/$', views.signup),
    #url(r'^signup/', views.signup, name="usersignup"),
    # Examples:
    (r'^user_check/$', views.user_check),
    (r'^$', 'views.index'),
    url(
    r'^disc/view/(?P<slug>[^\.]+).html', 
        'views.view_post', 
        name='view_disc_post'),
    url(
        r'^disc/category/(?P<slug>[^\.]+).html', 
        'views.view_category', 
        name='view_disc_category'),
'''
