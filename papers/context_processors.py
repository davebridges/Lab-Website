'''This file contains context processors to pass api keys to each template.

These are needed to properly render the PLOS APIs'''

from django.conf import settings

def api_keys(request):
    '''A context processor to add the a dictionary of api keys to the context.
    
    If no accounts are specified then empty strings should be passed.
    '''
    dict = {}
    dict['plos_api_key'] = settings.PLOS_API_KEY
    return dict
