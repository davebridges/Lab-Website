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

class LabPapersFeed(Feed):
    title = "Papers From the %s" % settings.LAB_NAME
    link = "/feeds/lab-papers"
    description = "This feed contains papers published by members of the %s." % settings.LAB_NAME

    def items(self):
        return Publication.objects.filter(laboratory_paper=True)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.abstract
        
class InterestingPapersFeed(Feed):
    title = "Papers of Interest"
    link = "/feeds/interesting-papers"
    description = "This feed contains papers that the %s is particularly interested in." % settings.LAB_NAME

    def items(self):
        return Publication.objects.filter(interesting_paper=True)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.abstract