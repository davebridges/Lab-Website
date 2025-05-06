'''This package controls the sitemap for the :mod:`projects` app. 

This sitemap will be generated at **/sitemap-projects.xml**
'''

from django.contrib.sitemaps import Sitemap

from projects.models import Project, Funding

class ProjectsSitemap(Sitemap):
    '''This sitemap lists all :class:`~projects.models.Project` objects to be indexed.
    
    It includes all projects.'''

    changefreq = 'monthly'
    priority = '0.7'
    
    def items(self):
        '''Filters :class:`~papers.models.Publication` to show only laboratory papers.'''
        return Project.objects.all()
        
    def lastmod(self, project):
        '''lastmod uses the last modification of the paper (not the comments).'''
        return project.date_last_modified
        
class FundingSitemap(Sitemap):
    '''This sitemap lists all :class:`~projects.models.Funding` objects to be indexed.
    
    It includes all funding.'''

    changefreq = 'monthly'
    priority = '0.6'
    
    def items(self):
        '''Filters :class:`~papers.models.Publication` to show only laboratory papers.'''
        return Funding.objects.all()
        
    def lastmod(self, project):
        '''lastmod uses the last modification of the paper (not the comments).'''
        return project.date_last_modified        