'''This file contains context processors to pass social media information to each template.

These are needed to properly render the Follow On Twitter, Like on Facebook and Add to Google Plus Information'''

from django.conf import settings

def social_media_accounts(request):
    '''A context processor to add the a dictionary of social media accounts to the context.
    
    If no accounts are specified then empty strings should be passed.
    '''
    dict = {}
    dict['twitter'] = settings.TWITTER_NAME
    dict['google_plus'] = settings.GOOGLE_PLUS_ID
    dict['facebook'] = settings.FACEBOOK_NAME
    dict['lab_name'] = settings.LAB_NAME
    return dict
