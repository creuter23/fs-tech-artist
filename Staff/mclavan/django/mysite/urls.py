from django.conf.urls.defaults import patterns, include, url

# Connecting to different views.
from mysite.django_test import current_datetime
from mysite.views import hello
from mysite.views import hours_ahead
from mysite.views import fill_data

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Site root
    (r'^$', fill_data),
    # /time
    (r'^time/$', current_datetime),
    (r'^time/plus/(\d{1,2})/$', hours_ahead),
    # /hello
    (r'^hello/$', hello),
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
