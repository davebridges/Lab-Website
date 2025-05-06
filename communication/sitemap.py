'''This package controls the sitemap for the :mod:`communication` app. 

There will be sitemaps generated at **/sitemap-posts.xml**.
'''

from django.contrib.sitemaps import Sitemap

from communication.models import Post

class PostsSitemap(Sitemap):
    '''This sitemap lists all :class:`~communication.models.Post` objects to be indexed.
    
    '''

    changefreq = 'monthly'
    priority = '0.9'
    
    def items(self):
        '''Shows all :class:`~communication.models.Post` objects.'''
        return Post.objects.all()
        
    def lastmod(self, post):
        '''lastmod uses the last modification of the post or the creation date.'''
        if post.modified:
            return post.modified
        else:
            return post.created
