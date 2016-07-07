'''This package has the url encodings for the main app.'''
from django.conf.urls import include, url
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.contrib.sitemaps import Sitemap
from django.conf.urls.static import static
from django.conf import settings

#from tastypie.api import Api

import communication
from communication.views import FeedDetailView, LabLocationView

from personnel.sitemap import LabPersonnelSitemap
from papers.sitemap import LabPublicationsSitemap, CommentarySitemap
from projects.sitemap import ProjectsSitemap, FundingSitemap
from communication.sitemap import PostsSitemap

#from papers.api import PublicationResource
#from projects.api import ProjectResource
#from personnel.api import PersonnelResource

from papers.feeds import LabPapersFeed, InterestingPapersFeed, CommentaryFeed
from projects.feeds import ProjectsFeed
from communication.feeds import PostsFeed

from views import IndexView

class StaticViewSitemap(Sitemap):
    '''This sitemap is for all static pages, including list views home and feeds.'''   
 
    priority = 0.4
    changefreq = 'weekly'

    def items(self):
        return ['location','feed-details','laboratory-papers','interesting-papers','commentary-list','laboratory-personnel','laboratory-alumni','project-list', 'post-list', 'twitter','google-calendar','wikipedia','lab-rules','publication-policy','data-resource-policy','lab-news','contact-info','funding-list']

    def location(self, item):
        return reverse(item)

#v1_api = Api(api_name='v1')
#v1_api.register(PublicationResource())
#v1_api.register(ProjectResource())
#v1_api.register(PersonnelResource())

#this dictionary lists sitemap files which will be generated.
sitemaps = {
    'personnel': LabPersonnelSitemap,
    'papers': LabPublicationsSitemap,
    'commentary': CommentarySitemap,
    'posts': PostsSitemap,
    'projects': ProjectsSitemap,
    'funding': FundingSitemap,
    'static': StaticViewSitemap
    }

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

admin.autodiscover()

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^contact/', include('communication.urls')), 
    url(r'^posts/', include('communication.urls_posts')),
    url(r'^papers/', include('papers.urls')),
    url(r'^people/', include('personnel.urls')),
    url(r'^projects/', include('projects.urls')),
    url(r'^funding/', include('projects.funding_urls')),    
    
    url(r'location/?$', LabLocationView.as_view(), name="location"),
    
    url(r'^feeds/?$', FeedDetailView.as_view(), name="feed-details"),
    url(r'^feeds/lab-papers/?$', LabPapersFeed(), name="lab-papers-feed"),
    url(r'^feeds/interesting-papers/?$', InterestingPapersFeed(), name="interesting-papers-feed"),
    url(r'^feeds/commentaries/?$', CommentaryFeed(), name="commentary-feed"),
    url(r'^feeds/projects/?', ProjectsFeed(), name="projects-feed"),
    url(r'^feeds/posts/?', PostsFeed(), name="posts-feed"),    
      
    url(r'^twitter/?$', communication.views.TwitterView.as_view(), name="twitter"),
    url(r'^calendar/?$', communication.views.GoogleCalendarView.as_view(), name="google-calendar"),
    url(r'^wikipedia/?$', communication.views.WikipedaEditsView.as_view(), name="wikipedia"),
    url(r'^lab-rules/?$', communication.views.LabRulesView.as_view(), name="lab-rules"),
    url(r'^publication-policy/?$', communication.views.PublicationPolicyView.as_view(), name="publication-policy"),
    url(r'^data-resource-sharing/?$', communication.views.DataResourceSharingPolicyView.as_view(), name="data-resource-policy"),
    url(r'^news/?$', communication.views.NewsView.as_view(), name='lab-news'),

 
    #url(r'^api/',include(v1_api.urls)),   
    url(r'^sitemap\.xml$', sitemap_views.index, {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemap_views.sitemap, {'sitemaps': sitemaps}),
    url(r'^$', IndexView.as_view(), name="home")
]

