from django.conf.urls.defaults import patterns, include, url

import art_test.views as views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', views.gateway),                  
    (r'^user_access/$', views.login),
    (r'^apply/$', views.apply),
    # Examples:
    # url(r'^$', 'art_test.views.home', name='home'),
    # url(r'^art_test/', include('art_test.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     #url(r'^admin/', include(admin.site.urls)),
)
