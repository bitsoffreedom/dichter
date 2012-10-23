from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    
    urlpatterns = staticfiles_urlpatterns()
    
    from os import path
    urlpatterns += patterns('django.views', 
                            (r'^%s(?P<path>.*)$' % \
                                settings.MEDIA_URL.lstrip('/'),
                             'static.serve',
                             {'document_root': settings.MEDIA_ROOT }))
    
else:
    urlpatterns = patterns('')


urlpatterns += patterns('',
  # Example:
  # (r'^dichter/', include('dichter.foo.urls')),
  (r'^$', 'dichter.denhaag.views.index'),

  (r'^action/(?P<campaign_id>\d+)/(?P<user>\w+)/mail/$', 'dichter.denhaag.views.send_message_mail'),
  (r'^action/(?P<campaign_id>\d+)/(?P<user>\w+)/facebook/$', 'dichter.denhaag.views.send_message_facebook'),

  (r'^campaign/(?P<campaign_slug>[\w-]+)/$', 'dichter.denhaag.views.index'),
  (r'^politicus/(?P<politician>[\w-]+)/$', 'dichter.denhaag.views.politician_info'),
  (r'^static/(?P<slug>[-\w]+)/$', 'dichter.denhaag.views.static'),

  # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
  # to INSTALLED_APPS to enable admin documentation:
  # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

  # Uncomment the next line to enable the admin:
  (r'^admin/', include(admin.site.urls)),
)
