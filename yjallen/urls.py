#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from yjallen_app.views import index, overview, letter_display, searchbox

urlpatterns = patterns('yjallen_app.views',
    url(r'^$', 'index', name='index'),
    url(r'^overview$', 'overview', name='overview'),
    url(r'^(?P<doc_id>[^/]+)$', 'letter_display', name="letter_display"),
    url(r'^search/$', 'searchbox', name='searchbox')
   )

if settings.DEBUG:
  urlpatterns += patterns(
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT } ),
)



