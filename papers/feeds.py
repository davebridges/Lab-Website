'''This package controls syndication for the :mod:papers, mainly for :class:`~papers.models.Publication` objects.

The available feeds are as follows:

+--------------------+---------------------------+---------------------------------------------+ 
| Feed               | Feed Location             | Feed Class                                  | 
+====================+===========================+=============================================+ 
| Laboratory papers  | /feeds/lab-papers         | :class:`~papers.feeds.LabPapersFeed         | 
+--------------------+---------------------------+---------------------------------------------+
| Interesting papers | /feeds/interesting-papers | :class:`~papers.feeds.InterestingPapersFeed | 
+--------------------+---------------------------+---------------------------------------------+
| Commentaries       | /feeds/commentaries       | :class:`~papers.feeds.CommentaryFeed        | 
+--------------------+---------------------------+---------------------------------------------+

A main page describing all feeds is available at **/feeds**.
'''

from datetime import datetime, time

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.conf import settings

from papers.models import Publication, Commentary

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

class CommentaryFeed(Feed):
    '''This class defines the feed for commentaries.'''

    title = "Commentaries by the %s" % settings.LAB_NAME
    link = "/feeds/commentaries"
    description = "Comments, written by members of the %s on papers.  These are typically the results of our internal journal club discussions."

    def items(self):
        '''The items returned by this feed are all Commentary objects.'''
        return Commentary.objects.all()

    def item_title(self, item):
        '''The title of each item will be "Commentary on XXX" or the unicode representation''' 
        return item.__unicode__()

    def item_description(self,item):
        '''The content of the feed is the actual comments.'''
        return item.comments + item.citation

    def item_author_name(self, item):
        '''The author of the item.'''
        return item.author

    def item_author_link(self, item):
        '''The link to the author's page.'''
        return item.author.get_absolute_url()

    def item_pubdate(self, item):
        '''The date of publication of this commentary, not the modification date.'''
        return datetime.combine(item.created, time())

    def item_updateddate(self, item):
        '''The date when this commentary was updated.'''
        return datetime.combine(item.modified, time())

#    def item_copyright(self, item):
#        '''The copyright is always CC-BY for commentaries.'''
#        return "%s by %s is licensed under a Creative Commons Attribution 3.0 Unported License.  Based on the work %s at %s." %(item, item.author, item.paper, item.paper.doi_link)
