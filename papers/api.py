'''This package controls api access to the papers app

These urls are served at /api/papers.'''

from tastypie.resources import ModelResource

from papers.models import Publication

class PublicationResource(ModelResource):
    '''This generates the API resource for Publications.
    
    It returns all publications in the database.
    Authors are currently not linked, as that would require an API to personnel.'''
    class Meta:
        '''The Meta class sets the conditions for the API.'''
        queryset = Publication.objects.all()
        resource_name = 'publications'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get'] 
        include_absolute_url = True
        filtering = {
            "year": 'exact',
            "type": ('exact', 'contains',),
        }      
               