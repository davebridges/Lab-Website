'''This package has the url encodings for the main app.'''
from django.urls import path, re_path, include
from django.urls import reverse
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.contrib.sitemaps import Sitemap

#from tastypie.api import Api

import communication
from communication.views import FeedDetailView, LabLocationView
from papers.views import JournalClubList

from personnel.sitemap import LabPersonnelSitemap
from papers.sitemap import LabPublicationsSitemap, CommentarySitemap
from projects.sitemap import ProjectsSitemap, FundingSitemap
from communication.sitemap import PostsSitemap

#from papers.api import PublicationResource
#from projects.api import ProjectResource
#from personnel.api import PersonnelResource

from papers.feeds import LabPapersFeed, InterestingPapersFeed, CommentaryFeed, JournalClubArticleFeed
from projects.feeds import ProjectsFeed
from communication.feeds import PostsFeed

from .views import IndexView, PhotoView
from django.views.generic import TemplateView

class StaticViewSitemap(Sitemap):
    '''This sitemap is for all static pages, including list views home and feeds.'''   
 
    priority = 0.4
    changefreq = 'weekly'

    def items(self):
        return ['location','feed-details','laboratory-papers','interesting-papers','commentary-list','laboratory-personnel','laboratory-alumni','project-list', 'post-list', 'twitter','google-calendar','wikipedia','lab-rules','publication-policy','data-resource-policy','lab-news','contact-info','funding-list','jc-list']

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
    # Admin docs and admin site
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    
    # App includes (no namespace change here assuming no 3-tuples passed)
    path('contact/', include('communication.urls')), 
    path('posts/', include('communication.urls_posts')),
    path('papers/', include('papers.urls')),
    path('people/', include('personnel.urls')),
    path('projects/', include('projects.urls')),
    path('funding/', include('projects.funding_urls')),
    
    # Views with trailing slashes made consistent (using path syntax)
    path('lab-photos/', PhotoView.as_view(), name="lab-photos"),    
    path('location/', LabLocationView.as_view(), name="location"),
    path('feeds/', FeedDetailView.as_view(), name="feed-details"),
    
    # Feed URLs
    path('feeds/lab-papers/', LabPapersFeed(), name="lab-papers-feed"),
    path('feeds/interesting-papers/', InterestingPapersFeed(), name="interesting-papers-feed"),
    path('feeds/commentaries/', CommentaryFeed(), name="commentary-feed"),
    path('feeds/projects/', ProjectsFeed(), name="projects-feed"),
    path('feeds/posts/', PostsFeed(), name="posts-feed"), 
    path('feeds/journal-club/', JournalClubArticleFeed(), name="jc-feed"),    
    
    # Other views
    path('twitter/', communication.views.TwitterView.as_view(), name="twitter"),
    path('calendar/', communication.views.GoogleCalendarView.as_view(), name="google-calendar"),
    path('wikipedia/', communication.views.WikipedaEditsView.as_view(), name="wikipedia"),
    path('lab-rules/', communication.views.LabRulesView.as_view(), name="lab-rules"),
    path('publication-policy/', communication.views.PublicationPolicyView.as_view(), name="publication-policy"),
    path('data-resource-sharing/', communication.views.DataResourceSharingPolicyView.as_view(), name="data-resource-policy"),
    path('news/', communication.views.NewsView.as_view(), name='lab-news'),
    path('journal-club/', JournalClubList.as_view(), name='jc-list'),
    
    # Sitemap URLs need regex, use re_path
    re_path(r'^sitemap\.xml$', sitemap_views.index, {'sitemaps': sitemaps}),
    re_path(r'^sitemap-(?P<section>.+)\.xml$', sitemap_views.sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    
    # Robots.txt
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    
    # Home page
    path('', IndexView.as_view(), name="home"),
]