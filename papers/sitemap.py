'''This package controls the sitemap for the papers app. 

This sitemap will be generated at /sitemap-papers.xml
'''

from django.contrib.sitemaps import Sitemap

from papers.models import Publication

class LabPublicationsSitemap(Sitemap):
    '''This sitemap lists all papers to be indexed.
    
    It only includes papers from this laboratory (laboratory_papers=True)'''

    changefreq = 'yearly'
    priority = '0.7'
    
    def items(self):
        '''Filters Publications to show only laboratory papers.'''
        return Publication.objects.filter(laboratory_paper=True)
        
    def lastmod(self, paper):
        '''lastmod uses the last modification of the paper (not the comments).'''
        return paper.date_last_modified