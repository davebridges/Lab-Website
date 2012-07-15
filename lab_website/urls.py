'''This package has the url encodings for the main app.'''
from django.conf.urls import patterns, include, url
from django.contrib import admin

from personnel.sitemap import LabPersonnelSitemap
from papers.sitemap import LabPublicationsSitemap

#this dictionary lists sitemap files which will be generated.
sitemaps = {
    'personnel': LabPersonnelSitemap,
    'papers': LabPublicationsSitemap
    }

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^communication/', include('communication.urls')), 
    url(r'^papers/', include('papers.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    )   

