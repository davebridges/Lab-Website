'''This package controls api access to the :mod:`papers` app

These urls are served at **/api/papers**.'''

from tastypie.resources import ModelResource

from papers.models import Publication

class PublicationResource(ModelResource):
    '''This generates the API resource for :class:`~papers.models.Publication` objects.
    
    It returns all publications in the database.
    Authors are currently not linked, as that would require an API to the :mod:`personnel` app.
    '''
    
    class Meta:
        '''The API serves all :class:`~papers.models.Publication` objects in the database..'''
        queryset = Publication.objects.all()
        resource_name = 'publications'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get'] 
        include_absolute_url = True
        filtering = {
            "year": 'exact',
            "type": ('exact', 'contains',),
        }      
               