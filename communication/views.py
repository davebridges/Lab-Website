'''This package contains views for the communication app'''

import json
import urllib, urllib2
import datetime, time

from django.conf import settings
from django.shortcuts import render_to_response
from django.views.generic import View
from django.template import RequestContext
from django.contrib import messages


def generate_timeline(screen_name):
    '''This function generates a timeline from a twitter username.

    This function requires a valid TWITTER_NAME as defined in localsettings.py.
    It places a REST call to the Twitter API v1 (see https://dev.twitter.com/docs/api/1/get/statuses/user_timeline)
    It returns a dictionary containing information on the most recent 200 tweets from that account (excluding replies).
    If twitter returns a HTTPError, an error message is returned.
    '''
    values = {'screen_name':screen_name, 'count':200, 'rts':'true', 'trim_user':'true', 'exclude_replies':'true'}
    params = urllib.urlencode(values)
    target_site = 'https://api.twitter.com/1/statuses/user_timeline.json?' + params
    response = urllib2.urlopen(target_site)
    json_response = response.read() #this reads the HTTP response
    timeline = json.loads(json_response)
    for tweet in timeline:
        str_time = time.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
        tweet['created_at_cleaned'] = datetime.datetime(*str_time[:6])
    return timeline

class TwitterView(View):
    '''This view class generates a page showing the twitter timeline for the lab twitter feed.
    '''

    def get(self, request, *args, **kwargs):
        '''This sets the GET function for TwitterView.'''
        try: 
            timeline = generate_timeline(settings.TWITTER_NAME)
            return render_to_response('twitter_timeline.html',
            {'timeline':timeline, 'screen_name':settings.TWITTER_NAME},
             mimetype='text/html',
             context_instance=RequestContext(request))
        except urllib2.HTTPError:
            messages.error(request, 'No Response from twitter.  Are you sure that %s is a valid twitter name?' % settings.TWITTER_NAME)	    
            return render_to_response('twitter_timeline.html',
            {'screen_name':settings.TWITTER_NAME},
             mimetype='text/html',
             context_instance=RequestContext(request))