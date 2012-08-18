'''This file contains context processors to pass api keys to templates as part of the :mod:`papers` app.

This is needed to properly render the PLOS API requests.
'''

from django.conf import settings

def api_keys(request):
    '''A context processor to add the a dictionary of api keys to the context.
    
    If no accounts are specified then empty strings should be passed.
    '''
    dict = {}
    dict['plos_api_key'] = settings.PLOS_API_KEY
    return dict
