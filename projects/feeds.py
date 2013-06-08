'''This package controls syndication for the :mod:projects,  for :class:`~projects.models.Project` objects.

The available feeds are as follows:

+--------------------+---------------------------+---------------------------------------------+ 
| Feed               | Feed Location             | Feed Class                                  | 
+====================+===========================+=============================================+ 
| Projects           | /feeds/projects           | :class:`~projects.feeds.ProjectsFeed        | 
+--------------------+---------------------------+---------------------------------------------+

A main page describing all feeds is available at **/feeds**.
'''

from django.contrib.syndication.views import Feed
from django.conf import settings

from projects.models import Project

class ProjectsFeed(Feed):
    '''This is the main class for all feeds related to :class:`~papers.models.Publication`.'''
    
    title = "Projects In the %s" % settings.LAB_NAME
    link = "/feeds/projects"
    description = "This feed contains projects being worked on by members of the %s." % settings.LAB_NAME    
    
    def items(self):
        return Project.objects.all()

    def item_title(self, item):
        '''The feed item title is the title of the paper.'''
        return item.title

    def item_description(self, item):
        '''The feed description is the abstract of the paper.'''
        return item.summary
