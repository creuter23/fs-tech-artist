from django.conf.urls.defaults import patterns, include, url
import art_test.views as views
from django.core.urlresolvers import reverse

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
    
    # Apply to an art test
    (r'^apply/$', views.apply),   

    # signup page ---> inital site registration
    url(r"^signup/$", views.signup, name='mainsignup'),

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
