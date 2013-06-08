'''This package has the url encodings for the main app.'''
from django.conf.urls import patterns, include, url
from django.contrib import admin

from tastypie.api import Api

from communication.views import FeedDetailView

from personnel.sitemap import LabPersonnelSitemap
from papers.sitemap import LabPublicationsSitemap
from projects.sitemap import ProjectsSitemap

from papers.api import PublicationResource
from papers.feeds import LabPapersFeed, InterestingPapersFeed

from views import IndexView

v1_api = Api(api_name='v1')
v1_api.register(PublicationResource())

#this dictionary lists sitemap files which will be generated.
sitemaps = {
    'personnel': LabPersonnelSitemap,
    'papers': LabPublicationsSitemap,
    'projects': ProjectsSitemap
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
    url(r'^people/', include('personnel.urls')),
    url(r'^projects/', include('projects.urls')),
    
    url(r'^feeds/?$', FeedDetailView.as_view(), name="feed-details"),
    url(r'^feeds/lab-papers/?$', LabPapersFeed(), name="lab-papers-feed"),
    url(r'^feeds/interesting-papers/?$', InterestingPapersFeed(), name="interesting-papers-feed"),
       
    (r'^api/',include(v1_api.urls)),   
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^$', IndexView.as_view())
    )

