'''This package controls syndication for the :mod:papers, mainly for :class:`~papers.models.Publication` objects.

The available feeds are as follows:

+--------------------+---------------------------+---------------------------------------------+ 
| Feed               | Feed Location             | Feed Class                                  | 
+====================+===========================+=============================================+ 
| Laboratory papers  | /feeds/lab-papers         | :class:`~papers.feeds.LabPapersFeed         | 
+--------------------+---------------------------+---------------------------------------------+
| Interesting papers | /feeds/interesting-papers | :class:`~papers.feeds.InterestingPapersFeed | 
+--------------------+---------------------------+---------------------------------------------+

A main page describing all feeds is available at **/feeds**.
'''

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.conf import settings

from papers.models import Publication

class PapersFeed(Feed):
    '''This is the main class for all feeds related to :class:`~papers.models.Publication`.'''
    
    def item_title(self, item):
        '''The feed item title is the title of the paper.'''
        return item.title

    def item_description(self, item):
        '''The feed description is the abstract of the paper.'''
        return item.abstract

class LabPapersFeed(PapersFeed):
    '''This generates a feed for papers from this group.'''

    title = "Papers From the %s" % settings.LAB_NAME
    link = "/feeds/lab-papers"
    description = "This feed contains papers published by members of the %s." % settings.LAB_NAME

    def items(self):
        '''The items returned by this feed are papers set as laboratory papers.'''
        return Publication.objects.filter(laboratory_paper=True)
        
class InterestingPapersFeed(PapersFeed):
    '''This generates a feed for papers marked as interesting.'''

    title = "Papers of Interest"
    link = "/feeds/interesting-papers"
    description = "This feed contains papers that the %s is particularly interested in." % settings.LAB_NAME

    def items(self):
        '''The items returned by this feed are papers set as interesting.'''
        return Publication.objects.filter(interesting_paper=True)