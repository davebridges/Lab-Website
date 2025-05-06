'''This package controls the sitemap for the :mod:`papers` app. 

There will be sitemaps generated at **/sitemap-papers.xml and **/sitemap-commentaries.xml**
'''

from django.contrib.sitemaps import Sitemap

from papers.models import Publication, Commentary

class LabPublicationsSitemap(Sitemap):
    '''This sitemap lists all :class:`~papers.models.Publication` objects to be indexed.
    
    It only includes papers from this laboratory (laboratory_papers=True)'''

    changefreq = 'yearly'
    priority = '0.7'
    
    def items(self):
        '''Filters :class:`~papers.models.Publication` to show only laboratory papers.'''
        return Publication.objects.filter(laboratory_paper=True)
        
    def lastmod(self, paper):
        '''lastmod uses the last modification of the paper (not the comments).'''
        return paper.date_last_modified

class CommentarySitemap(Sitemap):
    '''This sitemap lists all :class:`~papers.modelsCommentary` objects.'''

    changefreq = 'yearly'
    priority = '0.6'

    def items(self):
        '''All Commentaries are shown.'''
        return Commentary.objects.all()

    def lastmod(self, commentary):
        return commentary.modified
