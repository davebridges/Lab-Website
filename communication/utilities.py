'''This package contains utility functions for the :mod:`communication` app.

This will include generic API request functionality (currently for oauth2).
OAuth2 authentication is done using the python-oauth2 library (from https://github.com/brosner/python-oauth2).  This library in turn requires httplib2
'''

from django.conf import settings

import oauth2 as oauth
import time

def twitter_oauth_req(url, http_method="GET", post_body=None, http_headers=None):
    '''This function is a generic oauth request object.
    
    This request will only work for the twitter API, providing you have set all the applicable settings in localsettings.py
    As currently configured, this request will only have access to an account which is registered as your home account at https://dev.twitter.com/apps.
    This function requires a url and will return json content from that url. 
    '''
    consumer = oauth.Consumer(key=settings.TWITTER_CONSUMER_KEY, secret=settings.TWITTER_CONSUMER_SECRET)
    access_token = oauth.Token(key=settings.TWITTER_ACCESS_TOKEN, secret=settings.TWITTER_ACCESS_TOKEN_SECRET)
    client = oauth.Client(consumer, access_token)
 
    resp, content = client.request(
        url,
        method=http_method,
        body=post_body,
        headers=http_headers,
        force_auth_header=True
    )
    return content