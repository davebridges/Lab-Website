'''This package contains views for the communication app.

So far this includes API calls for Twitter feeds and Google Calendar'''

import json
import urllib.request
import urllib.error
import urllib.parse
import datetime, time
import requests
import dateutil

from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.template import RequestContext
from django.contrib import messages
from django.urls import reverse_lazy

from django.contrib.auth.mixins import PermissionRequiredMixin

from communication.models import LabAddress, LabLocation, Post
from papers.models import Commentary

def generate_twitter_timeline(count=5):
    """
    Fetches the most recent tweets for a given user using Twitter API v2.

    Requires:
        - TWITTER_BEARER_TOKEN
        - TWITTER_NAME (handle without @)

    Returns:
        List of tweets as dictionaries, or error message.
    """
    headers = {
        "Authorization": f"Bearer {settings.TWITTER_BEARER_TOKEN}"
    }

    # Step 1: Get user ID from username
    user_url = f"https://api.twitter.com/2/users/by/username/{settings.TWITTER_NAME}"
    user_resp = requests.get(user_url, headers=headers)
    if user_resp.status_code != 200:
        return {"error": f"User lookup failed: {user_resp.text}"}
    
    user_id = user_resp.json()["data"]["id"]

    # Step 2: Get tweets from that user
    timeline_url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    params = {
        "max_results": min(count, 100),  # Twitter max is 100
        "tweet.fields": "created_at,text,id"
    }

    tweets_resp = requests.get(timeline_url, headers=headers, params=params)
    if tweets_resp.status_code != 200:
        return {"error": f"Tweet fetch failed: {tweets_resp.text}"}

    return tweets_resp.json().get("data", [])
    
def facebook_status_request(type, max):
    '''This function takes a request url and token and returns deserialized data.
        
    It requires a type (general, milestones or posts) and a maximum number of entries to return
    '''
    values = {'access_token':settings.FACEBOOK_ACCESS_TOKEN}
    params = urllib.parse.urlencode(values)
    request_url = 'https://graph.facebook.com/v2.3/'+ '447068338637332' + type + '&' + params + '&limit=' + str(max)  
    request = urllib.request.Request(request_url)
    
    try:
        response = urllib.request.urlopen(request)
    except urllib.error.URLError as e:
        if e.code == 404:
            data = "Facebook API is not Available."
        else:
            #this is for a non-404 URLError.
            data = "Facebook API is not Available."
    except ValueError:
            data = "Facebook API is not Available."        
    else:
            #successful connection
            json_data = response.read()
            data = json.loads(json_data)
            return data       
    
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
    params = urllib.parse.urlencode(values)
    target_site = 'http://en.wikipedia.org/w/api.php?' + params
    response = urllib.request.urlopen(target_site)
    json_response = response.read() #this reads the HTTP response
    pages = json.loads(json_response) 
    for edit in pages['query']['usercontribs']:
        str_time = time.strptime(edit['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
        edit['timestamp_cleaned'] = datetime.datetime(*str_time[:6])    
    return pages

class TwitterView(TemplateView):
    '''This view class generates a page showing the twitter timeline for the lab twitter feed.
    
    This view uses the function :function:`~communication.utilities.twitter_oauth_req`.
    The default settings are to return 20 tweets including retweets but excluding replies.
    '''

    template_name = "twitter_timeline.html"
    
    def get_context_data(self, **kwargs):
        '''This function adds the google_calendar_id to the context.'''
        context = super(TwitterView, self).get_context_data(**kwargs)
        context['timeline'] = generate_twitter_timeline(50)
        context['screen_name'] = settings.TWITTER_NAME
        return context 
             
class GoogleCalendarView(TemplateView):
    '''This view renders a google calendar page.
    
    It can render a link to the iCalendar representation of the calendar.
    This view will also display the next few events.
    The calendar is generated by a widget
    Currently this only works for publicly shared Google Calendars.
    '''
    
    template_name = 'calendar.html'
    
    def get_context_data(self, **kwargs):
        '''This function adds the google_calendar_id to the context.'''
        context = super(GoogleCalendarView, self).get_context_data(**kwargs)
        context['google_calendar_id'] = settings.GOOGLE_CALENDAR_ID
        return context    
        
class WikipedaEditsView(View):  
    '''This view class generates a page showing the wikipedia edits for a user.
    '''

    def get(self, request, *args, **kwargs):
        '''This sets the GET function for WikipediaEditsView.'''
        try: 
            pages = get_wikipedia_edits(settings.WIKIPEDIA_USERNAME,50)
            return render(request, 'wikipedia_edits.html',
            {'pages':pages,'username':settings.WIKIPEDIA_USERNAME})
        except urllib.error.HTTPError:
            messages.error(request, 'No Response from Wikipedia.  Are you sure that %s is a valid username?' % settings.WIKIPEDIA_USERNAME)	    
            return render('wikipedia_edits.html',
            {'username':settings.WIKIPEDIA_USERNAME})
             
class LabRulesView(TemplateView):
    '''This view gets the lab rules markdown and displays this file.
    
    This file must be supplied in LAB_RULES_FILE in localsettings.py
    The template will markup this file and display it as formatted HTML.
    If this file is not provided or is unavailable, an error will be displayed.
    '''
    
    template_name = 'lab_rules.html'
    
    def get_context_data(self, **kwargs):
        '''This function provides the context which is passed to this view.
        
        It will check if the markdown file is available, download it and pass  it to the template.
        If there is no markdown file, then it will generate a no file presented note.'''
        context = super(LabRulesView, self).get_context_data(**kwargs)
        request = urllib.request.Request(settings.LAB_RULES_FILE)
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.URLError as e:
            if e.code == 404:
                lab_rules = "Lab Rules File is not Available."
            else:
                #this is for a non-404 URLError.
                lab_rules = "Lab Rules File is not Available."
        except ValueError:
            lab_rules = "Lab Rules File is not Available."        
        else:
             #successful connection
             lab_rules = response.read()         
        context['lab_rules'] = lab_rules
        context['lab_rules_source'] = settings.LAB_RULES_FILE
        return context 
    
class PublicationPolicyView(TemplateView):
    '''This view gets the publication policy markdown and displays this file.
    
    This file must be supplied in PUBLICATION_POLICY_FILE in localsettings.py
    The template will markup this file and display it as formatted HTML.
    If this file is not provided or is unavailable, an error will be displayed.
    '''
    
    template_name = 'publication_policy.html'
    
    def get_context_data(self, **kwargs):
        '''This function provides the context which is passed to this view.
        
        It will check if the markdown file is available, download it and pass  it to the template.
        If there is no markdown file, then it will generate a no file presented note.'''
        context = super(PublicationPolicyView, self).get_context_data(**kwargs)
        request = urllib.request.Request(settings.PUBLICATION_POLICY_FILE)
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.URLError as e:
            if e.code == 404:
                publication_policy = "Publication Policy File is not Available."
            else:
                #this is for a non-404 URLError.
                publication_policy = "Publication Policy File is not Available."
        except ValueError:
            publication_policy = "Publication Policy File is not Available."        
        else:
             #successful connection
             publication_policy = response.read()         
        context['publication_policy'] = publication_policy
        context['publication_policy_source'] = settings.PUBLICATION_POLICY_FILE
        return context

class DataResourceSharingPolicyView(TemplateView):
    '''This view gets the publication policy markdown and displays this file.
    
    This file must be supplied in DATA_SHARING_FILE in localsettings.py
    The template will markup this file and display it as formatted HTML.
    If this file is not provided or is unavailable, an error will be displayed.
    '''
    
    template_name = 'data_sharing_policy.html'
    
    def get_context_data(self, **kwargs):
        '''This function provides the context which is passed to this view.
        
        It will check if the markdown file is available, download it and pass  it to the template.
        If there is no markdown file, then it will generate a no file presented note.'''
        context = super(DataResourceSharingPolicyView, self).get_context_data(**kwargs)
        request = urllib.request.Request(settings.DATA_SHARING_FILE)
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.URLError as e:
            if e.code == 404:
                data_sharing_policy = "Publication Policy File is not Available."
            else:
                #this is for a non-404 URLError.
                data_sharing_policy = "Publication Policy File is not Available."
        except ValueError:
            data_sharing_policy = "Publication Policy File is not Available."        
        else:
             #successful connection
             publication_policy = response.read()         
        context['data_sharing_policy'] = publication_policy
        context['data_sharing_policy_source'] = settings.DATA_SHARING_FILE
        return context

class FeedDetailView(TemplateView):
    '''This view redirects to a template describing RSS feeds.'''
    
    template_name = "feed_details.html"   
    
    def get_context_data(self, **kwargs):
        '''This function adds the google_calendar_id to the context.'''
        context = super(FeedDetailView, self).get_context_data(**kwargs)
        context['google_calendar_id'] = settings.GOOGLE_CALENDAR_ID
        context['wikipedia_username'] = settings.WIKIPEDIA_USERNAME
        return context 
        
class NewsView(TemplateView):
    '''This view parses the facebook feed and presents it as laboratory news.
    '''
    
    template_name = "lab_news.html"
    
    def get_context_data(self, **kwargs):
        '''This function adds milestones and posts to the context.'''
                                              
        context = super(NewsView, self).get_context_data(**kwargs)
        context['posts'] = facebook_status_request('/?fields=posts', 100)
        context['links'] = facebook_status_request('/?fields=links', 5)
        context['photos'] = facebook_status_request('/photos/?type=uploaded', 100)
#         milestones = facebook_status_request('milestones', 10)
#         for milestone in milestones['data']:
#             milestone['start_time_cleaned'] = dateutil.parser.parse(milestone['start_time'])
#         context['milestones'] = milestones
        return context 
        
class ContactView(ListView):
    '''This view provides lab-contact information.'''
    
    template_name = "contact.html"
    model = LabAddress  
   
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ContactView, self).get_context_data(**kwargs)
        context['twitter'] = settings.TWITTER_NAME
        context['google_plus'] = settings.GOOGLE_PLUS_ID
        context['facebook'] = settings.FACEBOOK_NAME
        context['lab_name'] = settings.LAB_NAME
        context['disqus_forum'] = settings.DISQUS_SHORTNAME
        context['fb_app_id'] = settings.FACEBOOK_APP_ID
        context['fb_admins'] = settings.FACEBOOK_ID
        context['analytics_tracking'] = settings.ANALYTICS_TRACKING
        context['analytics_root'] = settings.ANALYTICS_ROOT
        return context 

class LabLocationView(ListView):
    '''This view provides location information.
    
    Its passes the location_list parameter when the /location view is requested.
    '''
    
    template_name = "location.html"
    model = LabLocation  
    
class PostList(ListView):
    '''This class generates the view for posts and commentaries located at **/post**.
    '''
    model = Post
    template_name = "post_list.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PostList, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the commentaries
        context['commentaries'] = Commentary.objects.all()
        return context

class PostDetail(DetailView):
    '''This class generates the view for post-detail located at **/post/<slug>**.
    '''
    model = Post
    slug_field = "post_slug"
    slug_url_kwarg = "post_slug"      
    template_name = "post_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        request_url = str(context['post'].markdown_url)
        
        request = urllib.request.Request(request_url)
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.URLError as e:
            if e.code == 404:
                post_data = "Post is not Available."
            else:
                #this is for a non-404 URLError.
                post_data = "Post is not Available."
        except ValueError:
            post_data = "Post is not Available."        
        else:
             #successful connection
             post_data = response.read()         
        context['post_data'] = post_data
        return context
                
class PostCreate(PermissionRequiredMixin, CreateView):
    '''This view is for creating a new :class:`~commentary.models.Post`.
    
    It requires the permissions to create a new paper and is found at the url **/post/new**.'''
    
    permission_required = 'communication.create_post'
    model = Post
    fields = '__all__'
    template_name = "post_form.html"

class PostUpdate(PermissionRequiredMixin, UpdateView):
    '''This view is for updating a :class:`~commentary.models.Post`.
    
    It requires the permissions to update a post and is found at the url **/post/<slug>/edit**.'''
    
    permission_required = 'communication.update_post'
    slug_field = "post_slug"
    slug_url_kwarg = "post_slug"    
    model = Post
    fields = '__all__'
    template_name = 'post_form.html' 
    
class PostDelete(PermissionRequiredMixin, DeleteView):
    '''This view is for deleting a :class:`~commentary.models.Post`.
    
    It requires the permissions to delete a paper and is found at the url **/post/<slug>/delete**.'''
    
    permission_required = 'communication.delete_post'
    slug_field = "post_slug"
    slug_url_kwarg = "post_slug"      
    model = Post
    template_name = 'confirm_delete.html'
    template_object_name = 'object'
    success_url = reverse_lazy('post-list')                                               
