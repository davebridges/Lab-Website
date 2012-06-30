'''This package contains views for the communication app.

So far this includes API calls for Twitter feeds and Google Calendar'''

import json
import urllib, urllib2
import datetime, time

from django.conf import settings
from django.shortcuts import render_to_response
from django.views.generic import View
from django.template import RequestContext
from django.contrib import messages


def generate_timeline(screen_name, count):
    '''This function generates a timeline from a twitter username.

    This function requires a valid TWITTER_NAME as defined in localsettings.py.
    The function also requires an integer for the number of tweets as a second argument.
    It places a REST call to the Twitter API v1 (see https://dev.twitter.com/docs/api/1/get/statuses/user_timeline)
    It returns a dictionary containing information on the most recent tweets from that account (excluding replies).
    If twitter returns a HTTPError, an error message is returned.
    
    '''
    values = {'screen_name':screen_name, 'count':count, 'rts':'true', 'trim_user':'true', 'exclude_replies':'true'}
    params = urllib.urlencode(values)
    target_site = 'https://api.twitter.com/1/statuses/user_timeline.json?' + params
    response = urllib2.urlopen(target_site)
    json_response = response.read() #this reads the HTTP response
    timeline = json.loads(json_response)
    for tweet in timeline:
        str_time = time.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
        tweet['created_at_cleaned'] = datetime.datetime(*str_time[:6])
    return timeline
    
def get_wikipedia_edits(username, count):
    '''This function gets the wikipedia edits for a particular user.
    
    This function takes a username argument and a count argument.
    It places a REST call to the Wikipedia API (see http://www.mediawiki.org/wiki/API).
    It returns a dictionary with the names of the edited articles.
    '''    
    values = {'ucuser':username, 
    'action':'query', 
    'list':'usercontribs', 
    'format':'json', 
    'uclimit':count,
    'ucnamespace':'0',
    'ucprop':'title|timestamp',
    'ucshow':'!minor'}
    params = urllib.urlencode(values)
    target_site = 'http://en.wikipedia.org/w/api.php?' + params
    response = urllib2.urlopen(target_site)
    json_response = response.read() #this reads the HTTP response
    pages = json.loads(json_response) 
    for edit in pages['query']['usercontribs']:
        str_time = time.strptime(edit['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
        edit['timestamp_cleaned'] = datetime.datetime(*str_time[:6])    
    return pages

class TwitterView(View):
    '''This view class generates a page showing the twitter timeline for the lab twitter feed.
    '''

    def get(self, request, *args, **kwargs):
        '''This sets the GET function for TwitterView.'''
        try: 
            timeline = generate_timeline(settings.TWITTER_NAME,50)
            return render_to_response('twitter_timeline.html',
            {'timeline':timeline, 'screen_name':settings.TWITTER_NAME},
             mimetype='text/html',
             context_instance=RequestContext(request))
        except urllib2.HTTPError:
            messages.error(request, 'No Response from Twitter.  Are you sure that %s is a valid twitter name?' % settings.TWITTER_NAME)	    
            return render_to_response('twitter_timeline.html',
            {'screen_name':settings.TWITTER_NAME},
             mimetype='text/html',
             context_instance=RequestContext(request))
             
class GoogleCalendarView(View):
    '''This view renders a google calendar page.
    
    It can render a link to the iCalendar representation of the calendar.
    This view will also display the next few events.
    Currently this only works for publicly shared Google Calendars.
    Not yet functional.'''

    def get(self, request, *args, **kwargs):
        '''This sets the GET function for GoogleCalendarView.
       
        Optional parameters are set in the values call.
        See https://developers.google.com/google-apps/calendar/v2/reference for more options.'''
        try:
            values = {'orderby':'starttime', 'max-results':15, 'singleevents':'true', 'sortorder':'ascending', 'futureevents':'true', 'alt':'json'}
            params = urllib.urlencode(values)
            target_site = "http://www.google.com/calendar/feeds/%s/public/full?" %str(settings.GOOGLE_CALENDAR_ID) + params 
            response = urllib2.urlopen(target_site)
            json_response = response.read() #this reads the HTTP response
            calendar = json.loads(json_response) 
            return render_to_response('calendar.html',
            {'calendar':calendar},
             mimetype='text/html',
             context_instance=RequestContext(request))
        except urllib2.HTTPError:
            messages.error(request, 'No Response from Google.  Are you sure that %s is a valid google calendar id?' % settings.GOOGLE_CALENDAR_ID)	    
            return render_to_response('calendar.html',
            {},
             mimetype='text/html',
             context_instance=RequestContext(request))                   
           
        '''json parsing example for event in calendar['feed']['entry']:
                    print event['title']['$t']  
                    
              relevant fields also
              print x['gd$when'][0]['endTime']
              print x['gd$when'][0]['startTime']      
        '''
        
class WikipedaEditsView(View):  
    '''This view class generates a page showing the wikipedia edits for a user.
    '''

    def get(self, request, *args, **kwargs):
        '''This sets the GET function for WikipediaEditsView.'''
        try: 
            pages = get_wikipedia_edits(settings.WIKIPEDIA_USERNAME,50)
            return render_to_response('wikipedia_edits.html',
            {'pages':pages,'username':settings.WIKIPEDIA_USERNAME},
             mimetype='text/html',
             context_instance=RequestContext(request))
        except urllib2.HTTPError:
            messages.error(request, 'No Response from Wikipedia.  Are you sure that %s is a valid username?' % settings.WIKIPEDIA_USERNAME)	    
            return render_to_response('wikipedia_edits.html',
            {'username':settings.WIKIPEDIA_USERNAME},
             mimetype='text/html',
             context_instance=RequestContext(request))      