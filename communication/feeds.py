'''This package controls syndication for the :mod:communication, only for :class:`~communication.models.Post` objects.

The available feeds are as follows:

+--------------------+---------------------------+---------------------------------------------+ 
| Feed               | Feed Location             | Feed Class                                  | 
+====================+===========================+=============================================+ 
| Posts               | /feeds/posts             | :class:`~commentary.feeds.PostssFeed         | 
+--------------------+---------------------------+---------------------------------------------+


A main page describing all feeds is available at **/feeds**.
'''

from datetime import datetime, time

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.conf import settings

from communication.models import Post


class PostsFeed(Feed):
    '''This class defines the feed for posts.'''

    title = "Posts by the %s" % settings.LAB_NAME
    link = "/feeds/posts"
    description = "Blog posts, about papers or interesting topics to our group."

    def items(self):
        '''The items returned by this feed are all Post objects.'''
        return Post.objects.all()

    def item_title(self, item):
        '''The title of each item will be the unicode representation''' 
        return item.__unicode__()

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

    def item_copyright(self, item):
        '''The copyright is always CC-BY for posts.'''
        return "%s by %s is licensed under a Creative Commons Attribution 4.0 Unported License." %(item, item.author)
