from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^subscribe/(?P<service>[-\w]+)?', 'mail_bin.collector.views.subscribe', name='subscribe'),
                       url(r'^subscribe-form/(?P<service>[-\w]+)?',
                           'mail_bin.collector.views.subscribe_form', name='subscribe-form'),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       )
