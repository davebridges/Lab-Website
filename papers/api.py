'''This package controls api access to the papers app

These urls are served at /api/papers.'''

from tastypie.resources import ModelResource

from papers.models import Publication


class PublicationResource(ModelResource):
    '''This generates the API resource for Publications.
    
    It returns all publications in the database'''
    class Meta:
        '''The Meta class sets the conditions for the API.'''
        queryset = Publication.objects.all()
        resource_name = 'publications'