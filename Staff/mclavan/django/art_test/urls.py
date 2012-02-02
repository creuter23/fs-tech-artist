from django.conf.urls.defaults import patterns, include, url
import art_test.views as views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', views.gateway),
    (r'^bad_gateway/$', views.bad_gateway),
    (r'^user_access/$', views.login),
    (r'^apply/$', views.apply),   
    (r'^signup/$', views.signup),
    (r'^user_check/$', views.user_check),
    # Examples:
    # url(r'^$', 'art_test.views.home', name='home'),
    # url(r'^art_test/', include('art_test.foo.urls')),
    (r'^$', 'views.index'),
    url(
    r'^disc/view/(?P<slug>[^\.]+).html', 
        'views.view_post', 
        name='view_disc_post'),
    url(
        r'^disc/category/(?P<slug>[^\.]+).html', 
        'views.view_category', 
        name='view_disc_category'),
                       
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    #The search function...
    (r'^search/$', 'search.views.search'),
    #Flat page urls...catchall...
    (r'', include('django.contrib.flatpages.urls')),

)