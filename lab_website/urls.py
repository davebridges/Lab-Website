'''This package has the url encodings for the main app.'''
from django.conf.urls import patterns, include, url
from django.contrib import admin

from tastypie.api import Api

from personnel.sitemap import LabPersonnelSitemap
from papers.sitemap import LabPublicationsSitemap

from papers.api import PublicationResource

v1_api = Api(api_name='v1')
v1_api.register(PublicationResource())

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
    url(r'^personnel/', include('personnel.urls')), 
    (r'^api/',include(v1_api.urls)),   
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    )   

