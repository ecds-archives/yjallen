from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.sitemaps import views as sitemaps_views
#from django.contrib.sitemaps import views as sitemaps_views
#from django.contrib.sitemaps import Sitemap

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from yjallen_app.models import LetterTitle
from yjallen_app.sitemaps import LetterSitemap
from yjallen_app.views import *

# info_dict = {
#   'queryset': LetterTitle.objects.all(),
# }

sitemaps = {
    'letters': LetterSitemap,
}

urlpatterns = patterns('',
    url(r'^sitemap\.xml$', sitemaps_views.index, {'sitemaps': sitemaps}),
    url(r'^$', 'yjallen_app.views.index', name='index'),
    url(r'^overview$', 'yjallen_app.views.overview', name='overview'),
    url(r'^(?P<doc_id>[^/]+)$', 'yjallen_app.views.letter_display', name="letter_display"),
    url(r'^(?P<doc_id>[^/]+)/xml$', 'yjallen_app.views.letter_xml', name="letter_xml"),
    url(r'^search/$', 'yjallen_app.views.searchbox', name='searchbox'),
    url(r'^(?P<basename>[^/]+)/download$', 'yjallen_app.views.send_file', name='send_file'),
)

# urlpatterns += patterns('',
#     url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
#     )

if settings.DEBUG:
  urlpatterns += patterns(
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT } ),
)



